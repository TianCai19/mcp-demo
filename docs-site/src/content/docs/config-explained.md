---
title: 配置格式详解
description: MCP 配置 JSON 格式的详细解释
---

# MCP 配置 JSON 格式详解

## 问题：为什么配置要这样写？

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

---

## 1. 理解配置的本质

### 配置 = 如何启动 Server 程序

这个 JSON 配置实际上是在告诉 MCP 客户端：

> "要启动 weather server，请在终端中运行这个命令"

```
MCP 客户端读取配置
        ↓
理解：需要启动一个程序
        ↓
执行：uv --directory /path/to/weather run weather.py
        ↓
建立与该程序的通信
```

---

## 2. 逐层解析

### 第一层：mcpServers（服务器列表）

```json
{
  "mcpServers": {
    "server1": {...},
    "server2": {...}
  }
}
```

- **作用**：定义所有要连接的 MCP servers
- **类型**：对象（字典）
- **每个 key**：server 的名称（你自己定义的）

---

### 第二层：server 名称

```json
{
  "mcpServers": {
    "weather": {     // ← 这是 server 名称
      "command": "uv",
      ...
    }
  }
}
```

- **`"weather"`**：server 的标识符
- 你可以用任何名称：`"my-weather"`, `"天气服务"`, `"server1"`
- 在客户端中会显示这个名称

---

### 第三层：command（启动命令）

```json
{
  "command": "uv"
}
```

**这是什么？**
- `command` 是要在终端执行的**命令名称**
- 就像你在终端输入的第一个词

**示例对比：**

| 终端命令 | JSON 中的 command |
|----------|-------------------|
| `python script.py` | `"command": "python"` |
| `node script.js` | `"command": "node"` |
| `uv run script.py` | `"command": "uv"` |
| `npx server` | `"command": "npx"` |

**为什么是 `uv`？**
- 因为我们的 server 是用 `uv run weather.py` 启动的
- `uv` 是命令名称

---

### 第四层：args（命令参数）

```json
{
  "args": [
    "--directory",
    "/Users/zz/codes/cc/mcp-demo/weather",
    "run",
    "weather.py"
  ]
}
```

**这是什么？**
- `args` 是传递给 `command` 的**参数列表**
- 每个元素都是一个独立的参数

**还原成终端命令：**
```bash
$ uv --directory /Users/zz/codes/cc/mcp-demo/weather run weather.py
│  │            │                                    │   │
│  │            └──────────────┬────────────────────┘   └─ 文件名
│  │                           └─ 其他参数
│  └─────────── 这些都是 args ────┘
└─ command
```

---

## 3. 参数详细分解

### 参数 1: `--directory`

```json
"--directory"
```

**作用**：告诉 uv 在哪个目录下运行

**为什么需要？**
- 我们的 `weather.py` 在 `/Users/zz/codes/cc/mcp-demo/weather` 目录
- 需要在那个目录下运行，才能找到 `.venv` 和依赖

**等价命令：**
```bash
# 使用 --directory 参数
uv --directory /Users/zz/codes/cc/mcp-demo/weather run weather.py

# 等价于先 cd 再运行
cd /Users/zz/codes/cc/mcp-demo/weather
uv run weather.py
```

---

### 参数 2: 目录路径

```json
"/Users/zz/codes/cc/mcp-demo/weather"
```

**作用**：指定目录的绝对路径

**为什么用绝对路径？**
- MCP 客户端可能从任何目录启动
- 绝对路径确保无论在哪里都能找到文件

**绝对路径 vs 相对路径：**
```json
// ✅ 好：绝对路径
"/Users/zz/codes/cc/mcp-demo/weather"

// ❌ 差：相对路径（可能找不到）
"../weather"

// ❌ 差：波浪线展开（某些客户端不支持）
"~/codes/cc/mcp-demo/weather"
```

---

### 参数 3: `run`

```json
"run"
```

**作用**：uv 的子命令，用于运行 Python 脚本

**uv 的常用命令：**
| 命令 | 作用 |
|------|------|
| `uv run script.py` | 运行脚本 |
| `uv add package` | 添加依赖 |
| `uv venv` | 创建虚拟环境 |
| `uv sync` | 同步依赖 |

---

### 参数 4: `weather.py`

```json
"weather.py"
```

**作用**：要运行的 Python 文件

**这是 server 的入口文件**
- 包含 MCP server 的代码
- 当这个文件运行时，server 就启动了

---

## 4. 完整执行流程

### 客户端启动时发生了什么？

```
1. 读取配置文件
   {
     "command": "uv",
     "args": ["--directory", "/path", "run", "weather.py"]
   }

2. 构建完整命令
   uv --directory /path run weather.py

3. 启动子进程
   ┌─────────────────────────────────┐
   │  Client 程序                     │
   │                                 │
   │  启动子进程 → uv run weather.py │
   │                                 │
   └─────────────────────────────────┘

4. 建立 stdio 通信
   Client.stdout → Server.stdin
   Server.stdout → Client.stdin

5. Server 准备就绪
   开始接收和响应 JSON-RPC 消息
```

---

## 5. 其他配置示例

### 示例 1：直接使用 Python

**如果不用 uv：**
```json
{
  "command": "python",
  "args": ["/Users/zz/codes/cc/mcp-demo/weather/weather.py"]
}
```

**等价命令：**
```bash
python /Users/zz/codes/cc/mcp-demo/weather/weather.py
```

**问题：**
- 需要在系统 PATH 中有 python
- 依赖需要在系统环境中安装

---

### 示例 2：使用 npx（Node.js）

```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
}
```

**等价命令：**
```bash
npx -y @modelcontextprotocol/server-filesystem /allowed/path
```

**参数说明：**
- `-y`：自动确认（不需要提示）
- `@modelcontextprotocol/server-filesystem`：npm 包名
- `/allowed/path`：传递给 server 的参数

---

### 示例 3：带环境变量的配置

```json
{
  "command": "node",
  "args": ["/path/to/server.js"],
  "env": {
    "API_KEY": "your-api-key",
    "DEBUG": "true"
  }
}
```

**等价命令：**
```bash
API_KEY=your-api-key DEBUG=true node /path/to/server.js
```

---

### 示例 4：全局安装的命令

```json
{
  "command": "mcp-server-git",
  "args": []
}
```

**适用于：**
- 使用 `pip install --global` 全局安装的 server
- 或在系统 PATH 中的命令

---

## 6. 为什么使用 uv 而不是直接用 python？

### 问题：直接用 python

```json
{
  "command": "python",
  "args": ["weather.py"]
}
```

**可能遇到的问题：**

1. **依赖问题**
   - `weather.py` 需要 `mcp` 和 `httpx` 包
   - 系统的 python 可能没有安装这些包

2. **版本问题**
   - 系统 python 版本可能太旧
   - 需要 Python 3.10+

3. **虚拟环境问题**
   - 需要激活正确的虚拟环境

### 解决方案：使用 uv

```json
{
  "command": "uv",
  "args": ["--directory", "/path/to/weather", "run", "weather.py"]
}
```

**优势：**

✅ **自动管理依赖**
- uv 会使用项目的 `.venv`
- 自动使用正确的 Python 版本

✅ **跨平台**
- macOS、Linux、Windows 都能工作

✅ **隔离性**
- 不会污染系统 Python 环境
- 每个项目有独立的依赖

---

## 7. 调试配置问题

### 问题 1：Command not found

**错误：** `Failed to start process: uv: command not found`

**原因：** `uv` 不在系统 PATH 中

**解决：** 使用完整路径
```json
{
  "command": "/opt/homebrew/bin/uv",  // uv 的完整路径
  "args": [...]
}
```

**如何找到完整路径：**
```bash
which uv
# 输出：/opt/homebrew/bin/uv
```

---

### 问题 2：File not found

**错误：** `No such file or directory: weather.py`

**原因：** 使用了相对路径

**解决：** 使用绝对路径
```json
{
  "args": [
    "--directory",
    "/Users/zz/codes/cc/mcp-demo/weather",  // 绝对路径
    "run",
    "weather.py"
  ]
}
```

---

### 问题 3：如何验证配置？

**方法 1：手动运行命令**
```bash
# 从配置中提取命令并手动运行
uv --directory /Users/zz/codes/cc/mcp-demo/weather run weather.py
```

如果这个命令能正常启动 server，配置就是正确的。

**方法 2：检查客户端日志**
```bash
# Claude Desktop
tail -f ~/Library/Logs/Claude/mcp*.log

# Cherry Studio
tail -f ~/Library/Logs/Cherry\ Studio/mcp*.log
```

---

## 8. 配置格式规范

### 标准格式

```json
{
  "mcpServers": {
    "server-name": {
      "command": "可执行文件或命令",
      "args": ["参数1", "参数2", ...],
      "env": {
        "环境变量名": "环境变量值"
      }
    }
  }
}
```

### 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `mcpServers` | object | ✅ | 顶层容器 |
| `command` | string | ✅ | 要执行的命令 |
| `args` | array | ✅ | 命令参数列表 |
| `env` | object | ❌ | 环境变量（可选） |

---

## 9. 实用技巧

### 技巧 1：获取当前路径

```bash
# 在 server 目录下运行
pwd
# 输出：/Users/zz/codes/cc/mcp-demo/weather
# 直接复制到配置中使用
```

### 技巧 2：测试命令

```bash
# 先在终端手动测试命令
uv --directory /Users/zz/codes/cc/mcp-demo/weather run weather.py

# 确认能正常启动后，再写入配置
```

### 技巧 3：简化配置（使用全局安装）

如果不想每次都指定路径，可以全局安装：
```bash
# 全局安装 server
pip install mcp-server-weather --global

# 配置就简单了
{
  "command": "mcp-server-weather",
  "args": []
}
```

---

## 10. 总结

### 配置的本质

```json
{
  "command": "uv",
  "args": ["--directory", "/path", "run", "weather.py"]
}
```

**这句话的意思是：**

> "在终端中执行：`uv --directory /path run weather.py`"

### 关键要点

1. **`command`** = 要执行的程序（如 `uv`, `python`, `node`）
2. **`args`** = 传递给程序的参数列表
3. **`--directory`** = 指定工作目录（uv 特有）
4. **使用绝对路径** = 避免路径找不到的问题

### 学习建议

```
1. 理解"配置就是启动命令"的概念
   ↓
2. 在终端手动运行命令，理解每个部分
   ↓
3. 将命令拆分成 command + args
   ↓
4. 写入 JSON 配置文件
   ↓
5. 重启客户端验证配置
```

---

## 扩展阅读

- [MCP 配置规范](https://modelcontextprotocol.io/basics/#servers)
- [uv 命令文档](https://docs.astral.sh/uv/)
- [子进程管理](https://docs.python.org/3/library/subprocess.html)
