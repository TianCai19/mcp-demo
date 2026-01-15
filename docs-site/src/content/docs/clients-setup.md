---
title: 各客户端配置指南
description: 如何将 MCP Server 配置到各种客户端工具
---

# MCP Server 配置指南 - 各种客户端

本文档介绍如何将 `weather` MCP Server 配置到不同的 MCP 客户端工具。

## Server 信息

**Server 路径**: `/Users/zz/codes/cc/mcp-demo/weather/weather.py`
**启动命令**: `uv run weather.py` (需要在 weather 目录下)
**提供工具**:
- `get_alerts(state)` - 获取美国各州的天气警报
- `get_forecast(latitude, longitude)` - 获取天气预报

## 1. Cherry Studio

Cherry Studio 支持 MCP 协议，可以通过配置文件连接 MCP servers。

### 配置步骤

1. **打开 Cherry Studio 配置文件**

   Cherry Studio 的 MCP 配置文件通常位于：
   - macOS: `~/Library/Application Support/Cherry Studio/mcp.json`
   - Windows: `%APPDATA%/Cherry Studio/mcp.json`
   - Linux: `~/.config/Cherry Studio/mcp.json`

2. **添加 Server 配置**

   ```json
   {
     "mcpServers": {
       "weather": {
         "command": "uv",
         "args": [
           "--directory",
           "/Users/zz/codes/cc/mcp-demo/weather",
           "run",
           "weather.py"
         ]
       }
     }
   }
   ```

3. **重启 Cherry Studio**

4. **验证连接**
   - 启动后应该能看到 "weather" 连接器
   - 可以在对话中使用天气相关查询

### 使用示例

```
用户: 查询加州的天气警报
用户: What's the weather forecast for Sacramento? (38.58, -121.49)
```

## 2. Claude Desktop

### 配置文件位置
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

### 配置内容

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/zz/codes/cc/mcp-demo/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
```

## 3. Cline (VS Code Extension)

Cline 是一个 VS Code AI 助手扩展，支持 MCP。

### 配置步骤

1. 打开 VS Code 设置
2. 搜索 "Cline: MCP Servers"
3. 添加以下配置：

```json
{
  "cline.mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/zz/codes/cc/mcp-demo/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
```

## 4. Continue (VS Code Extension)

Continue 是另一个流行的 VS Code AI 助手。

### 配置文件位置
`~/.continue/config.json`

### 配置内容

```json
{
  "mcpServers": [
    {
      "name": "weather",
      "command": "uv",
      "args": [
        "--directory",
        "/Users/zz/codes/cc/mcp-demo/weather",
        "run",
        "weather.py"
      ]
    }
  ]
}
```

## 5. Cursor

Cursor 是一个 AI 代码编辑器，支持 MCP。

### 配置文件位置
`~/Library/Application Support/Cursor/User/globalStorage/mcp.json`

### 配置内容

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/zz/codes/cc/mcp-demo/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
```

## 6. 通用配置说明

### 命令格式

所有 MCP 客户端使用相同的配置格式：

```json
{
  "mcpServers": {
    "server-name": {
      "command": "启动命令",
      "args": ["命令参数数组"],
      "env": {
        "环境变量名": "环境变量值"
      }
    }
  }
}
```

### 重要提示

1. **绝对路径**: 始终使用绝对路径，不要使用相对路径
2. **uv 路径**: 如果命令找不到 uv，使用完整路径：
   ```bash
   which uv  # 获取 uv 的完整路径
   ```

3. **权限问题**: 确保 weather.py 有执行权限：
   ```bash
   chmod +x /Users/zz/codes/cc/mcp-demo/weather/weather.py
   ```

4. **环境变量**: 如果 Server 需要环境变量，添加 `env` 字段：
   ```json
   {
     "command": "uv",
     "args": ["--directory", "/path/to/weather", "run", "weather.py"],
     "env": {
       "API_KEY": "your-api-key"
     }
   }
   ```

## 7. 测试连接

配置完成后，在任何支持 MCP 的客户端中测试：

### 测试查询示例

```
# 英文查询（推荐）
"What are the current weather alerts for California?"
"Get the weather forecast for latitude 38.58, longitude -121.49"

# 中文查询
"加州有什么天气警报？"
"Sacramento 的天气预报如何？"
```

### 预期结果

- 客户端应该能够识别并调用 `get_alerts` 或 `get_forecast` 工具
- 返回来自美国国家气象局 (NWS) 的实时天气数据

## 8. 故障排查

### 问题：Server 未显示在客户端

**解决方案：**
1. 检查配置文件语法是否正确（JSON 格式）
2. 确认使用了绝对路径
3. 重启客户端应用
4. 检查客户端的日志文件

### 问题：工具调用失败

**解决方案：**
1. 手动测试 Server 是否能正常运行：
   ```bash
   cd /Users/zz/codes/cc/mcp-demo/weather
   uv run weather.py
   ```

2. 检查网络连接（需要访问 api.weather.gov）

3. 确认使用美国地区的数据（NWS API 仅支持美国）

### 问题：权限错误

**解决方案：**
```bash
# 确保 virtual environment 存在
cd /Users/zz/codes/cc/mcp-demo/weather
uv venv

# 测试运行
uv run weather.py
```

## 9. 多 Server 配置示例

如果需要同时连接多个 MCP servers：

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": ["--directory", "/Users/zz/codes/cc/mcp-demo/weather", "run", "weather.py"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token"
      }
    }
  }
}
```

## 10. 实用命令

```bash
# 获取当前路径（用于配置）
pwd

# 检查 uv 是否安装
which uv

# 测试 weather server
cd /Users/zz/codes/cc/mcp-demo/weather
uv run weather.py

# 查看客户端日志
tail -f ~/Library/Logs/Claude/mcp*.log  # Claude Desktop
tail -f ~/Library/Logs/Cherry\ Studio/mcp*.log  # Cherry Studio
```

## 更多资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [Cherry Studio GitHub](https://github.com/CherryHQ/cherry-studio)
- [Claude Desktop 下载](https://claude.ai/download)
- [MCP Servers 列表](https://github.com/modelcontextprotocol/servers)
