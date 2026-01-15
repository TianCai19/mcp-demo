# MCP Demo - Weather Server & Client

一个完整的 Model Context Protocol (MCP) 示例项目，包含 Server 和 Client 的实现。

**📚 文档站点**: https://mcp-demo-virid.vercel.app

## 项目概述

本项目展示了如何使用 MCP 构建一个天气服务系统：

- **MCP Server**: 提供天气查询工具（天气警报、天气预报）
- **MCP Client**: 连接到 Server 并通过 AI 模型调用工具获取天气信息

## 项目结构

```
mcp-demo/
├── weather/              # MCP Server
│   ├── weather.py                # 服务器实现
│   ├── weather_commented.py      # 带详细中文注释的版本
│   ├── CODE_EXPLAINED.md         # 代码逐行解析文档
│   ├── TRANSPORT_EXPLAINED.md    # transport="stdio" 详细解释
│   └── .venv/                    # 虚拟环境
│
├── mcp-client/           # MCP Client
│   ├── client.py         # 交互式客户端
│   ├── test_client.py    # 自动化测试脚本
│   ├── .env              # API 配置
│   └── .venv/            # 虚拟环境
│
├── README.md             # 项目说明
└── MCP_CLIENTS_SETUP.md  # 各客户端配置指南
```

## 功能特性

### MCP Server (weather)
提供两个工具：
- `get_alerts(state)` - 获取美国各州的天气警报
- `get_forecast(latitude, longitude)` - 获取指定位置的天气预报

### MCP Client
- 连接到 MCP Server
- 使用 OpenRouter API 调用 Claude 3.5 Sonnet
- 自动识别并调用合适的工具
- 支持交互式对话

## 环境要求

- Python 3.10+
- uv (Python 包管理器)
- OpenRouter API Key

## 安装步骤

### 1. 安装 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 设置 MCP Server

```bash
cd weather
uv venv
uv add "mcp[cli]" httpx
```

### 3. 设置 MCP Client

```bash
cd mcp-client
uv venv
uv add mcp anthropic python-dotenv requests
```

### 4. 配置 API Key

编辑 `mcp-client/.env` 文件：

```env
OPENROUTER_API_KEY=your-openrouter-api-key-here
```

获取 OpenRouter API Key: https://openrouter.ai/keys

## 使用方法

### 交互式运行

```bash
cd mcp-client
uv run python client.py ../weather/weather.py
```

启动后可以输入查询，例如：
```
Query: What are the weather alerts for California?
Query: What's the weather forecast for Sacramento?
Query: quit
```

### 自动化测试

```bash
cd mcp-client
uv run python test_client.py ../weather/weather.py
```

## 工作流程

```
用户输入查询
    ↓
Client 连接到 MCP Server
    ↓
获取可用工具列表 (get_alerts, get_forecast)
    ↓
发送查询 + 工具信息 到 AI (Claude 3.5 via OpenRouter)
    ↓
AI 决定是否需要调用工具
    ↓
如果需要工具：通过 MCP 调用 Server 的工具
    ↓
Server 调用 NWS API 获取数据
    ↓
返回结果给 AI
    ↓
AI 生成自然语言回复
    ↓
用户看到最终答案
```

## API 说明

### Server 工具

#### get_alerts
获取美国州的天气警报

**参数：**
- `state` (string): 两字母州代码，如 "CA", "NY"

**返回：** 天气警报列表，包括事件类型、影响区域、严重程度等

#### get_forecast
获取指定位置的天气预报

**参数：**
- `latitude` (number): 纬度
- `longitude` (number): 经度

**返回：** 未来5个时间段的天气预报

### 示例查询

```
# 天气警报
"What are the weather alerts for Texas?"
"Any weather alerts in New York?"

# 天气预报
"What's the weather forecast for Sacramento?"
"Get forecast for latitude 38.58, longitude -121.49"
```

## 技术栈

- **MCP SDK**: Model Context Protocol Python SDK
- **FastMCP**: 快速构建 MCP Server
- **OpenRouter**: 统一的 AI API 接口
- **Claude 3.5 Sonnet**: Anthropic 的 AI 模型
- **NWS API**: 美国国家气象局数据源

## 注意事项

1. **天气数据限制**: NWS API 仅支持美国地区
2. **API 费用**: OpenRouter 按使用量计费
3. **网络要求**: 需要能访问 api.weather.gov

## 故障排查

### Server 连接失败
- 检查 Server 路径是否正确
- 确保 `weather.py` 文件存在

### API 调用失败
- 验证 OpenRouter API Key 是否正确
- 检查网络连接
- 查看 API 余额是否充足

### 工具调用失败
- 确保使用美国州代码（如 CA, NY）
- 天气预报需要有效的经纬度坐标

## 扩展建议

- 添加更多天气相关工具
- 支持其他天气数据源
- 添加缓存机制
- 实现多 Server 连接
- 添加 Web UI

## 学习资源

### 代码解析文档

适合 Python 初学者的详细学习文档：

- **[weather/CODE_EXPLAINED.md](weather/CODE_EXPLAINED.md)** - 代码逐行解析
  - 每行代码的详细解释
  - 关键概念讲解（异步、装饰器、类型注解等）
  - 数据流图和常见问题

- **[weather/weather_commented.py](weather/weather_commented.py)** - 带详细中文注释的代码
  - 可以对照原始代码学习
  - 每个 Python 概念都有解释

- **[weather/TRANSPORT_EXPLAINED.md](weather/TRANSPORT_EXPLAINED.md)** - transport="stdio" 详解
  - 什么是 stdin/stdout
  - MCP 如何使用 stdio 通信
  - 进程间通信原理

### 配置指南

- **[MCP_CLIENTS_SETUP.md](MCP_CLIENTS_SETUP.md)** - 各客户端配置方法
  - Cherry Studio
  - Claude Desktop
  - VS Code Extensions (Cline, Continue)
  - Cursor

### 推荐学习路径

```
1. 阅读 README.md 了解项目概况
   ↓
2. 阅读 weather/CODE_EXPLAINED.md 理解代码
   ↓
3. 对照 weather_commented.py 学习代码实现
   ↓
4. 阅读 TRANSPORT_EXPLAINED.md 理解通信机制
   ↓
5. 运行项目并尝试修改代码
   ↓
6. 使用 MCP_CLIENTS_SETUP.md 配置其他客户端
```

## 参考资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [OpenRouter 文档](https://openrouter.ai/docs)
- [NWS API 文档](https://www.weather.gov/documentation/services-web-api)

## License

MIT
