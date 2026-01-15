---
title: Transport 详解
description: 深入理解 transport="stdio" 的工作原理
---

# Transport = "stdio" 详细解释

## 问题：什么是 `transport="stdio"`？

在 `mcp.run(transport="stdio")` 中，`transport` 指定了 **MCP Server 与 Client 之间的通信方式**。

---

## 1. 基本概念

### Transport（传输层）
Transport 就像是一条"管道"，负责在两个程序之间传递消息。

```
┌─────────────┐              transport              ┌─────────────┐
│             │  ──────────────────────────────────>  │             │
│  MCP Client │        (传输消息的通道)               │  MCP Server │
│             │  <──────────────────────────────────  │             │
└─────────────┘                                      └─────────────┘
```

### stdio（标准输入/输出）
`stdio` 是 **Standard Input/Output** 的缩写：
- **stdin**（标准输入）：键盘输入的数据流
- **stdout**（标准输出）：显示到屏幕的数据流
- **stderr**（标准错误）：显示错误信息的数据流

---

## 2. 为什么使用 stdio 作为 Transport？

### 传统方式 vs MCP 方式

**传统程序：**
```
用户 → 输入 → 程序处理 → 输出 → 用户看到结果
```

**MCP Server：**
```
Client → JSON 消息 → Server 处理 → JSON 响应 → Client
        ↓
    通过 stdin/stdout 传递
```

### 关键区别

| 方面 | 传统程序 | MCP Server (stdio transport) |
|------|----------|------------------------------|
| 输入来源 | 用户键盘 | Client 程序 |
| 输出去向 | 用户屏幕 | Client 程序 |
| 数据格式 | 任意文本 | JSON 格式的消息 |
| 通信对象 | 人类 | 另一个程序 |

---

## 3. 工作原理详解

### 进程模型

```
┌─────────────────────────────────────────────────────┐
│                  操作系统                           │
│                                                     │
│  ┌──────────────┐          ┌──────────────┐       │
│  │  Client 进程  │          │  Server 进程  │       │
│  │              │          │              │       │
│  │  Python 脚本  │          │  weather.py  │       │
│  │              │          │              │       │
│  └──────┬───────┘          └──────┬───────┘       │
│         │                         │               │
│         │ stdout                  │ stdin         │
│         ├────────────────────────>│               │
│         │    JSON 消息            │               │
│         │                         │               │
│         │                         │               │
│         │ stdin                   │ stdout        │
│         │<────────────────────────┤               │
│         │    JSON 响应            │               │
│         │                         │               │
│  └──────┴───────┘          └──────┴───────┘       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 数据流向示例

**1. Client 发送请求：**
```python
# Client 代码
await session.call_tool("get_alerts", {"state": "CA"})
```

**2. 转换为 JSON 并写入 Server 的 stdin：**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_alerts",
    "arguments": {"state": "CA"}
  },
  "id": 1
}
```

**3. Server 从 stdin 读取并处理：**
```python
# weather.py 内部（MCP 框架处理）
# 读取 stdin → 解析 JSON → 调用 get_alerts("CA")
```

**4. Server 将结果写入 Client 的 stdin：**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{"type": "text", "text": "Weather alerts..."}]
  },
  "id": 1
}
```

---

## 4. 代码层面的理解

### Server 端（weather.py）

```python
# 这行代码启动 stdio transport
mcp.run(transport="stdio")
```

**实际发生了什么：**

```python
# FastMCP 内部的简化版本
def run(transport="stdio"):
    if transport == "stdio":
        # 1. 打开 stdin 和 stdout
        input_stream = sys.stdin    # 标准输入
        output_stream = sys.stdout  # 标准输出

        # 2. 持续读取和写入消息
        while True:
            # 从 stdin 读取 Client 发送的 JSON
            request = read_json_from_stdin()

            # 处理请求（调用工具）
            response = process_request(request)

            # 将响应写入 stdout（发送给 Client）
            write_json_to_stdout(response)
```

### Client 端（client.py）

```python
# Client 启动 Server 并建立 stdio 连接
server_params = StdioServerParameters(
    command="python",           # 用 python 启动
    args=["weather.py"],        # 运行 weather.py
)

# 建立 stdio 通信
stdio_transport = await stdio_client(server_params)
# ↑ 这会：
# 1. 启动 weather.py 作为子进程
# 2. 将 Client 的 stdout 连接到 Server 的 stdin
# 3. 将 Server 的 stdout 连接到 Client 的 stdin
```

---

## 5. 为什么要用 stdio？

### 优点

✅ **简单通用**
- 所有编程语言都支持 stdin/stdout
- 不需要额外的网络配置

✅ **安全**
- 不需要开放网络端口
- 通信仅限于本地

✅ **可靠**
- 操作系统保证数据顺序
- 不会丢失消息

✅ **进程隔离**
- Server 崩溃不会影响 Client
- 每个工具运行在独立进程

### 对比其他 Transport 方式

| Transport | 说明 | 优点 | 缺点 |
|-----------|------|------|------|
| **stdio** | 标准输入/输出 | 简单、安全 | 只能本地通信 |
| **SSE** | Server-Sent Events | 支持远程 | 需要网络 |
| **WebSocket** | 双向实时通信 | 实时性好 | 配置复杂 |

---

## 6. 实际演示

### 模拟 stdio 通信

创建一个简单的示例来理解：

```python
# server.py (模拟 MCP Server)
import sys
import json

def main():
    # 持续从 stdin 读取
    for line in sys.stdin:
        # 解析 JSON 消息
        message = json.loads(line)
        print(f"[Server] 收到: {message}", file=sys.stderr)

        # 处理消息
        if message.get("action") == "hello":
            response = {"status": "ok", "message": "Hello!"}
        else:
            response = {"status": "error", "message": "Unknown action"}

        # 将响应写入 stdout
        print(json.dumps(response))
        sys.stdout.flush()  # 立即发送

if __name__ == "__main__":
    main()
```

```python
# client.py (模拟 MCP Client)
import subprocess
import json

def main():
    # 启动 server.py 子进程
    process = subprocess.Popen(
        ["python", "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    # 发送消息到 server 的 stdin
    request = {"action": "hello"}
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()

    # 从 server 的 stdout 读取响应
    response_line = process.stdout.readline()
    response = json.loads(response_line)

    print(f"[Client] 收到响应: {response}")

    process.terminate()

if __name__ == "__main__":
    main()
```

**运行结果：**
```bash
$ python client.py
[Server] 收到: {'action': 'hello'}
[Client] 收到响应: {'status': 'ok', 'message': 'Hello!'}
```

---

## 7. 重要注意事项

### ⚠️ 不要在 MCP Server 中使用 print()

```python
# ❌ 错误示例
@mcp.tool()
def get_weather():
    print("正在获取天气...")  # 这会破坏 MCP 通信！
    return "晴天"

# ✅ 正确示例
import logging
logging.basicConfig(level=logging.INFO)

@mcp.tool()
def get_weather():
    logging.info("正在获取天气...")  # 使用 logging
    return "晴天"
```

**为什么？**
- `print()` 输出到 stdout
- MCP 也使用 stdout 传输 JSON
- 混在一起会导致解析错误

**正确的输出方式：**
- 正常消息 → `logging.info()`（输出到 stderr）
- 错误消息 → `logging.error()`

---

## 8. 类比理解

### MCP stdio 就像电话对话

```
Client (打电话者)              Server (接电话者)
    │                                    │
    │ 说话 (写入 stdout)                  │
    ├───────────────────────────────────>│
    │                              (听到 stdin)
    │                                    │
    │                              思考并回复
    │                                    │
    │                              说话 (写入 stdout)
    │<───────────────────────────────────│
    │ (听到 stdin)                        │
```

### 与传统程序对比

**传统脚本：**
```bash
$ python script.py
Hello World!  # 输出到屏幕，给人看
```

**MCP Server：**
```bash
$ python weather.py
# 没有输出！输出是 JSON，给程序看
```

---

## 9. 技术细节

### JSON-RPC 协议

MCP 使用 JSON-RPC 2.0 协议格式：

```json
// 请求消息
{
  "jsonrpc": "2.0",           // 协议版本
  "method": "tools/call",     // 要调用的方法
  "params": {                 // 参数
    "name": "get_alerts",
    "arguments": {"state": "CA"}
  },
  "id": 1                     // 请求 ID（用于匹配响应）
}

// 响应消息
{
  "jsonrpc": "2.0",
  "result": {                 // 结果数据
    "content": [...]
  },
  "id": 1                     // 对应请求的 ID
}
```

### 进程间通信（IPC）

stdio 是一种 IPC（进程间通信）方式：

```
┌─────────────────────────────────────────────────┐
│               IPC 类型对比                      │
├─────────────┬─────────────┬────────────────────┤
│    类型     │   范围      │     MCP 用途        │
├─────────────┼─────────────┼────────────────────┤
│ stdio       │ 本地进程    │ ✅ Server 通信      │
│ socket      │ 本地/网络   │ SSE transport       │
│ 共享内存    │ 本地        │ （MCP 不常用）       │
│ 消息队列    │ 本地/网络   │ （MCP 不常用）       │
└─────────────┴─────────────┴────────────────────┘
```

---

## 10. 总结

### transport="stdio" 的含义

```python
mcp.run(transport="stdio")
```

这行代码的意思是：

> "启动 MCP Server，使用标准输入/输出与 Client 进行 JSON-RPC 通信"

### 核心要点

1. **stdio 是通信管道**
   - Client 的 stdout → Server 的 stdin
   - Server 的 stdout → Client 的 stdin

2. **数据格式是 JSON**
   - 不是给人看的文本
   - 是程序之间交换的结构化数据

3. **适合本地工具**
   - 简单、安全、可靠
   - 不需要网络配置

4. **避免使用 print()**
   - 会干扰 JSON 通信
   - 使用 logging 代替

### 学习建议

```
1. 理解进程和子进程的概念
2. 学习 stdin/stdout/stderr 的区别
3. 了解 JSON-RPC 协议
4. 尝试编写简单的 IPC 示例
5. 查看 MCP 源码了解实现细节
```

---

## 扩展阅读

- **MCP 规范**: https://modelcontextprotocol.io/basics/
- **JSON-RPC 2.0**: https://www.jsonrpc.org/specification
- **Python subprocess 模块**: https://docs.python.org/3/library/subprocess.html
- **进程间通信**: https://en.wikipedia.org/wiki/Inter-process_communication
