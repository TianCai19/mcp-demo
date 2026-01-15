# weather.py 代码逐行解析

本文档详细解释 weather.py 的每一行代码，适合 Python 初学者阅读。

---

## 第一部分：导入模块 (第 1-4 行)

```python
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP
```

### 逐行解释：

**第 1 行：`from typing import Any`**
- **作用**：从 Python 的 `typing` 模块导入 `Any` 类型
- **解释**：
  - `typing` 是 Python 的类型提示模块
  - `Any` 表示"任何类型"，用于类型注解
  - 示例：`def func(x: Any)` 表示 x 可以是任何类型

**第 3 行：`import httpx`**
- **作用**：导入 httpx 库（一个现代的 HTTP 客户端）
- **解释**：
  - httpx 用于发送 HTTP 请求（类似 requests）
  - 支持异步操作，性能更好
  - 我们用它来调用天气 API

**第 4 行：`from mcp.server.fastmcp import FastMCP`**
- **作用**：从 MCP SDK 导入 FastMCP 类
- **解释**：
  - MCP = Model Context Protocol（模型上下文协议）
  - FastMCP 是一个快速构建 MCP Server 的工具类
  - 它简化了服务器的创建过程

---

## 第二部分：初始化服务器和常量 (第 6-11 行)

```python
# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"
```

### 逐行解释：

**第 7 行：`mcp = FastMCP("weather")`**
- **作用**：创建一个 MCP 服务器实例
- **解释**：
  - `"weather"` 是服务器的名称
  - `mcp` 是一个对象，我们可以用它来注册工具
  - 类比：这就像创建了一个"工具箱"，后续往里面添加工具

**第 10 行：`NWS_API_BASE = "https://api.weather.gov"`**
- **作用**：定义 API 基础地址常量
- **解释**：
  - NWS = National Weather Service（美国国家气象局）
  - 常量名使用大写是 Python 约定
  - 使用常量避免在代码中重复写 URL

**第 11 行：`USER_AGENT = "weather-app/1.0"`**
- **作用**：定义用户代理字符串
- **解释**：
  - User-Agent 告诉服务器是谁在请求
  - NWS API 要求必须有 User-Agent
  - 格式通常是：应用名/版本号

---

## 第三部分：API 请求函数 (第 14-23 行)

```python
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
```

### 详细解释：

**第 14 行：函数定义**
```python
async def make_nws_request(url: str) -> dict[str, Any] | None:
```
- **`async`**：表示这是一个异步函数
  - 异步函数可以并发执行，不阻塞程序
  - 必须使用 `await` 来调用异步函数
- **`url: str`**：参数类型注解，表示 url 是字符串类型
- **`-> dict[str, Any] | None`**：返回类型注解
  - 表示返回字典或 None
  - `dict[str, Any]` = 键是字符串，值可以是任何类型
  - `| None` = 或者返回 None

**第 15 行：文档字符串**
```python
"""Make a request to the NWS API with proper error handling."""
```
- 三引号字符串是 Python 的文档字符串（docstring）
- 用于解释函数的作用

**第 16 行：设置请求头**
```python
headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
```
- `headers` 是一个字典
- `User-Agent`：告诉服务器我们是谁
- `Accept`：告诉服务器我们想要什么格式的数据（GeoJSON）

**第 17 行：创建 HTTP 客户端**
```python
async with httpx.AsyncClient() as client:
```
- **`async with`**：异步上下文管理器
  - 自动处理资源的打开和关闭
  - 退出时自动关闭连接
- **`httpx.AsyncClient()`**：创建一个异步 HTTP 客户端
  - 用于发送异步 HTTP 请求

**第 19 行：发送 GET 请求**
```python
response = await client.get(url, headers=headers, timeout=30.0)
```
- **`await`**：等待异步操作完成
- **`client.get()`**：发送 HTTP GET 请求
- **`timeout=30.0`**：30 秒超时限制

**第 20 行：检查 HTTP 状态码**
```python
response.raise_for_status()
```
- 如果状态码不是 200（成功），抛出异常
- 例如：404（未找到）、500（服务器错误）

**第 21 行：解析 JSON**
```python
return response.json()
```
- 将响应的 JSON 数据转换为 Python 字典

**第 22-23 行：异常处理**
```python
except Exception:
    return None
```
- 捕获所有异常并返回 None
- 这样即使请求失败，程序也不会崩溃

---

## 第四部分：格式化警报信息 (第 26-35 行)

```python
def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions provided")}
"""
```

### 详细解释：

**第 26 行：函数定义**
```python
def format_alert(feature: dict) -> str:
```
- **注意**：这不是异步函数（没有 `async`）
- **`feature: dict`**：接收一个字典参数
- **`-> str`**：返回一个字符串

**第 28 行：提取属性**
```python
props = feature["properties"]
```
- 从字典中获取 "properties" 键的值
- 数据结构：
  ```python
  feature = {
      "properties": {
          "event": "Wind Advisory",
          "areaDesc": "Santa Clara Valley",
          ...
      }
  }
  ```

**第 29-35 行：f-string 格式化**
```python
return f"""
Event: {props.get("event", "Unknown")}
...
"""
```
- **`f"""..."""`**：f-string 多行字符串
  - `f` 前缀表示可以插入变量
  - `"""` 表示多行字符串
- **`props.get("event", "Unknown")`**：
  - 字典的 `get` 方法
  - 如果 "event" 不存在，返回 "Unknown"
  - 这比 `props["event"]` 更安全（不会报错）

---

## 第五部分：获取天气警报工具 (第 38-55 行)

```python
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)
```

### 详细解释：

**第 38 行：装饰器**
```python
@mcp.tool()
```
- **装饰器**：Python 的语法糖，用于修改函数
- **`mcp.tool()`**：将这个函数注册为 MCP 工具
- 效果：AI 客户端可以看到并调用这个工具

**第 39 行：异步函数定义**
```python
async def get_alerts(state: str) -> str:
```
- **`state: str`**：州代码参数（如 "CA"）
- **`-> str`**：返回字符串

**第 40-44 行：文档字符串**
```python
"""Get weather alerts for a US state.

Args:
    state: Two-letter US state code (e.g. CA, NY)
"""
```
- Google 风格的文档字符串
- 解释函数和参数的作用

**第 45 行：构建 URL**
```python
url = f"{NWS_API_BASE}/alerts/active/area/{state}"
```
- **f-string**：将变量插入字符串
- 结果示例：`https://api.weather.gov/alerts/active/area/CA`

**第 46 行：调用 API**
```python
data = await make_nws_request(url)
```
- **`await`**：等待异步函数返回
- `data` 可能是字典或 None

**第 48-49 行：错误检查**
```python
if not data or "features" not in data:
    return "Unable to fetch alerts or no alerts found."
```
- **`not data`**：检查 data 是否为 None
- **`"features" not in data`**：检查字典是否有 "features" 键
- **`or`**：两个条件满足一个即可

**第 51-52 行：空列表检查**
```python
if not data["features"]:
    return "No active alerts for this state."
```
- **`not data["features"]`**：检查列表是否为空
- 空列表在布尔上下文中为 False

**第 54 行：列表推导式**
```python
alerts = [format_alert(feature) for feature in data["features"]]
```
- **列表推导式**：简洁的创建列表方式
- 等价于：
  ```python
  alerts = []
  for feature in data["features"]:
      alerts.append(format_alert(feature))
  ```
- 对每个 feature 调用 format_alert 函数

**第 55 行：连接字符串**
```python
return "\n---\n".join(alerts)
```
- **`str.join()`**：将列表中的字符串连接成一个
- **`"\n---\n"`**：用换行和分隔符连接
- 示例：`["A", "B", "C"]` → `"A\n---\nB\n---\nC"`

---

## 第六部分：获取天气预报工具 (第 58-92 行)

```python
@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period["name"]}}:
Temperature: {period["temperature"]}°{period["temperatureUnit"]}
Wind: {period["windSpeed"]} {period["windDirection"]}
Forecast: {period["detailedForecast"]}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)
```

### 详细解释：

**第 58 行：装饰器**
```python
@mcp.tool()
```
- 将函数注册为 MCP 工具

**第 59 行：多个参数**
```python
async def get_forecast(latitude: float, longitude: float) -> str:
```
- **`latitude: float`**：纬度参数，浮点数类型
- **`longitude: float`**：经度参数，浮点数类型
- 示例调用：`get_forecast(38.58, -121.49)`

**第 67 行：第一次 API 调用**
```python
points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
```
- NWS API 需要先获取"点位"信息
- 示例：`https://api.weather.gov/points/38.58,-121.49`

**第 70-71 行：错误检查**
```python
if not points_data:
    return "Unable to fetch forecast data for this location."
```
- 检查第一次请求是否成功

**第 74 行：提取预报 URL**
```python
forecast_url = points_data["properties"]["forecast"]
```
- 从第一次响应中获取预报 URL
- NWS API 的两步查询流程

**第 77-78 行：第二次 API 调用**
```python
if not forecast_data:
    return "Unable to fetch detailed forecast."
```
- 检查第二次请求是否成功

**第 81 行：提取时间段**
```python
periods = forecast_data["properties"]["periods"]
```
- `periods` 是一个列表，包含多个时间段的数据
- 每个时段包含温度、风速等信息

**第 82-90 行：格式化预报**
```python
forecasts = []
for period in periods[:5]:  # Only show next 5 periods
    forecast = f"""
{period["name"]}:
...
"""
    forecasts.append(forecast)
```
- **`periods[:5]`**：列表切片，取前 5 个元素
- **`forecasts.append(forecast)`**：添加到列表
- 循环处理每个时间段

---

## 第七部分：主函数 (第 95-101 行)

```python
def main():
    # Initialize and run the server
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
```

### 详细解释：

**第 95 行：主函数定义**
```python
def main():
```
- **`main()`**：Python 的约定，程序的入口函数

**第 97 行：启动服务器**
```python
mcp.run(transport="stdio")
```
- **`transport="stdio"`**：使用标准输入输出通信
  - MCP Server 通过 stdin/stdout 与客户端通信
  - 这是进程间通信的一种方式

**第 100-101 行：条件执行**
```python
if __name__ == "__main__":
    main()
```
- **`__name__`**：Python 的特殊变量
  - 如果文件被直接运行：`__name__ == "__main__"`
  - 如果文件被导入：`__name__` 是文件名
- **作用**：只有在直接运行时才执行 main()
  - 防止被导入时自动执行

---

## 关键概念总结

### 1. 异步编程（Async）
```python
async def func():
    await something()
```
- `async`：定义异步函数
- `await`：等待异步操作完成
- 优势：可以并发处理多个请求

### 2. 类型注解
```python
def func(x: int) -> str:
```
- **`x: int`**：x 是整数类型
- **`-> str`**：返回字符串类型
- 好处：代码更清晰，IDE 可以提供更好的提示

### 3. 字典操作
```python
dict["key"]           # 访问（不存在会报错）
dict.get("key")       # 访问（不存在返回 None）
dict.get("key", default)  # 访问（不存在返回默认值）
```

### 4. 列表操作
```python
[1, 2, 3]            # 创建列表
list[:5]             # 切片，取前 5 个
[x for x in list]    # 列表推导式
"-".join(list)       # 连接字符串
```

### 5. 装饰器
```python
@mcp.tool()
def func():
    pass
```
- 相当于：`func = mcp.tool()(func)`
- 用于"装饰"或修改函数

### 6. 上下文管理器
```python
async with httpx.AsyncClient() as client:
    pass
```
- 自动处理资源的分配和释放
- 类似于 `try...finally`

---

## 数据流图

```
用户请求（如 "查询加州天气警报"）
    ↓
MCP Client 调用 get_alerts("CA")
    ↓
构建 URL: https://api.weather.gov/alerts/active/area/CA
    ↓
发送 HTTP GET 请求
    ↓
接收 JSON 响应
    ↓
解析数据并格式化
    ↓
返回格式化的字符串
    ↓
用户看到易读的天气警报信息
```

---

## 常见问题

### Q1: 为什么要用 `await`？
**A**: 异步函数需要用 `await` 调用，否则不会真正执行。

### Q2: `dict["key"]` 和 `dict.get("key")` 有什么区别？
**A**:
- `dict["key"]`：键不存在时会报错
- `dict.get("key")`：键不存在时返回 None

### Q3: 为什么用 f-string 而不是 + 连接字符串？
**A**: f-string 更清晰、更高效：
```python
# 好的方式
f"Hello, {name}"

# 不推荐
"Hello, " + name
```

### Q4: `|` 符号是什么意思？
**A**: 在类型注解中，`|` 表示"或"：
```python
dict[str, Any] | None  # 字典或 None
```

---

## 扩展建议

1. **添加缓存**：避免重复请求相同数据
2. **添加重试机制**：网络失败时自动重试
3. **支持更多地区**：扩展到全球天气 API
4. **添加日志**：记录请求和错误信息
5. **类型检查**：使用 mypy 进行静态类型检查
