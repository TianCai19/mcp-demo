"""
MCP Weather Server - 详细的中文注释版本

这是一个 MCP (Model Context Protocol) 服务器，提供天气查询功能。
包括两个工具：
1. get_alerts - 获取美国各州的天气警报
2. get_forecast - 获取指定位置的天气预报
"""

# ============================================================================
# 第一部分：导入所需的模块
# ============================================================================

# 从 typing 模块导入 Any 类型
# typing 是 Python 的类型提示模块，Any 表示任何类型
from typing import Any

# 导入 httpx 库，用于发送 HTTP 请求
# httpx 是一个现代化的 HTTP 客户端，支持异步操作
import httpx

# 从 MCP SDK 导入 FastMCP 类
# FastMCP 是快速构建 MCP 服务器的工具类
from mcp.server.fastmcp import FastMCP


# ============================================================================
# 第二部分：初始化服务器和定义常量
# ============================================================================

# 创建一个 MCP 服务器实例，命名为 "weather"
# mcp 是一个对象，我们可以用它来注册工具
mcp = FastMCP("weather")

# 定义常量：美国国家气象局 API 的基础地址
# 常量名使用大写是 Python 的约定
NWS_API_BASE = "https://api.weather.gov"

# 定义常量：用户代理字符串
# NWS API 要求请求必须包含 User-Agent
USER_AGENT = "weather-app/1.0"


# ============================================================================
# 第三部分：辅助函数 - 发送 API 请求
# ============================================================================

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """
    向 NWS API 发送请求的辅助函数

    参数:
        url: 请求的 URL 地址

    返回:
        成功时返回字典（解析后的 JSON 数据）
        失败时返回 None
    """
    # 设置 HTTP 请求头
    headers = {
        "User-Agent": USER_AGENT,              # 告诉服务器我们是谁
        "Accept": "application/geo+json"       # 告诉服务器我们想要 GeoJSON 格式
    }

    # 创建异步 HTTP 客户端
    # async with 确保使用完后自动关闭连接
    async with httpx.AsyncClient() as client:
        try:
            # 发送 GET 请求
            # await 等待异步操作完成
            # timeout=30.0 表示 30 秒超时
            response = await client.get(url, headers=headers, timeout=30.0)

            # 检查 HTTP 状态码
            # 如果不是 200（成功），会抛出异常
            response.raise_for_status()

            # 解析 JSON 响应并返回
            return response.json()

        except Exception:
            # 捕获所有异常，返回 None
            # 这样即使请求失败，程序也不会崩溃
            return None


# ============================================================================
# 第四部分：辅助函数 - 格式化天气警报
# ============================================================================

def format_alert(feature: dict) -> str:
    """
    将天气警报数据格式化为易读的字符串

    参数:
        feature: 包含天气警报信息的字典

    返回:
        格式化后的字符串
    """
    # 从字典中获取 "properties" 键的值
    # feature 的结构类似：{"properties": {"event": "...", "areaDesc": "..."}}
    props = feature["properties"]

    # 使用 f-string 格式化输出
    # props.get("event", "Unknown") 表示：获取 "event"，如果不存在则返回 "Unknown"
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions provided")}
"""


# ============================================================================
# 第五部分：MCP 工具 1 - 获取天气警报
# ============================================================================

@mcp.tool()  # 装饰器：将此函数注册为 MCP 工具
async def get_alerts(state: str) -> str:
    """
    获取美国州的天气警报

    参数:
        state: 两字母的美国州代码（如 CA, NY, TX）

    返回:
        格式化的天气警报信息字符串
    """
    # 使用 f-string 构建完整的 API URL
    # 例如：https://api.weather.gov/alerts/active/area/CA
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"

    # 调用辅助函数发送 API 请求
    # await 等待异步函数返回结果
    data = await make_nws_request(url)

    # 检查数据是否有效
    # not data: data 是 None
    # "features" not in data: 字典中没有 "features" 键
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    # 检查是否有警报（features 列表是否为空）
    if not data["features"]:
        return "No active alerts for this state."

    # 使用列表推导式格式化所有警报
    # 相当于：[format_alert(feature) for feature in data["features"]]
    alerts = [format_alert(feature) for feature in data["features"]]

    # 用 "\n---\n" 连接所有警报字符串
    return "\n---\n".join(alerts)


# ============================================================================
# 第六部分：MCP 工具 2 - 获取天气预报
# ============================================================================

@mcp.tool()  # 装饰器：将此函数注册为 MCP 工具
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    获取指定位置的天气预报

    参数:
        latitude: 纬度（如 38.58）
        longitude: 经度（如 -121.49）

    返回:
        格式化的天气预报字符串
    """
    # 步骤 1: 获取"点位"信息
    # NWS API 需要两步查询：先获取点位，再获取预报
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    # 检查点位数据是否有效
    if not points_data:
        return "Unable to fetch forecast data for this location."

    # 步骤 2: 从点位响应中提取预报 URL
    forecast_url = points_data["properties"]["forecast"]

    # 步骤 3: 使用预报 URL 获取实际预报数据
    forecast_data = await make_nws_request(forecast_url)

    # 检查预报数据是否有效
    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # 步骤 4: 提取时间段数据并格式化
    # periods 是一个列表，包含多个时间段的预报
    periods = forecast_data["properties"]["periods"]

    # 创建空列表用于存储格式化的预报
    forecasts = []

    # 遍历前 5 个时间段
    # periods[:5] 是列表切片，表示取前 5 个元素
    for period in periods[:5]:
        # 格式化单个时间段的预报
        forecast = f"""
{period["name"]}:
Temperature: {period["temperature"]}°{period["temperatureUnit"]}
Wind: {period["windSpeed"]} {period["windDirection"]}
Forecast: {period["detailedForecast"]}
"""
        # 添加到列表
        forecasts.append(forecast)

    # 连接所有预报并返回
    return "\n---\n".join(forecasts)


# ============================================================================
# 第七部分：主函数 - 启动服务器
# ============================================================================

def main():
    """
    主函数：启动 MCP 服务器

    transport="stdio" 表示使用标准输入/输出通信
    这是 MCP 服务器与客户端通信的方式
    """
    # 启动服务器
    mcp.run(transport="stdio")


# ============================================================================
# 第八部分：程序入口
# ============================================================================

# 这是一个 Python 的惯用写法
# __name__ 是一个特殊变量
# - 当文件被直接运行时，__name__ 的值是 "__main__"
# - 当文件被导入时，__name__ 是文件名（如 "weather"）
# 这样可以确保只有在直接运行时才执行 main()
if __name__ == "__main__":
    main()


# ============================================================================
# 代码说明总结
# ============================================================================
#
# 【异步编程】
# - async def: 定义异步函数，可以并发执行
# - await: 等待异步操作完成
# - 优势：同时处理多个请求，提高效率
#
# 【类型注解】
# - url: str 表示 url 是字符串类型
# - -> dict[str, Any] | None 表示返回字典或 None
# - 好处：代码更清晰，IDE 可以提供更好的提示
#
# 【装饰器】
# - @mcp.tool() 是一个装饰器
# - 它将下面的函数注册为 MCP 工具
# - 让 AI 客户端可以发现并调用这个函数
#
# 【字典操作】
# - dict["key"]: 访问字典的值，键不存在时会报错
# - dict.get("key"): 访问字典的值，键不存在时返回 None
# - dict.get("key", default): 访问字典的值，键不存在时返回默认值
#
# 【列表操作】
# - list[:5]: 列表切片，取前 5 个元素
# - [x for x in list]: 列表推导式，简洁的创建列表方式
# - "-".join(list): 用 "-" 连接列表中的字符串
#
# 【上下文管理器】
# - async with ... as ...: 自动管理资源的打开和关闭
# - 确保即使发生异常，资源也会被正确释放
#
# 【f-string】
# - f"{variable}" 是格式化字符串的方式
# - 可以直接在字符串中插入变量的值
# - 比使用 + 或 % 更清晰、更高效
