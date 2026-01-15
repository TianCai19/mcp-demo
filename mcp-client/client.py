import asyncio
import os
import sys
import json
import requests
from typing import Optional, Any
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from dotenv import load_dotenv

load_dotenv()


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

        # Get OpenRouter API key
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")

        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "anthropic/claude-3.5-sonnet"  # Claude supports tools well via OpenRouter

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    def _convert_mcp_tool_to_openai(self, mcp_tool: Any) -> dict:
        """Convert MCP tool format to OpenAI tool format"""
        return {
            "type": "function",
            "function": {
                "name": mcp_tool.name,
                "description": mcp_tool.description,
                "parameters": mcp_tool.inputSchema
            }
        }

    async def _call_openrouter(self, messages: list, tools: list) -> Any:
        """Call OpenRouter API with OpenAI-compatible format"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 1000,
            "tools": tools if tools else None,
        }

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    async def process_query(self, query: str) -> str:
        """Process a query using OpenRouter and available tools"""
        messages = [{"role": "user", "content": query}]

        # Get tools from MCP server
        response = await self.session.list_tools()
        openai_tools = [self._convert_mcp_tool_to_openai(tool) for tool in response.tools]

        # Initial API call
        api_response = await self._call_openrouter(messages, openai_tools)

        final_text = []
        assistant_message = api_response["choices"][0]["message"]

        # Process response
        if "content" in assistant_message and assistant_message["content"]:
            final_text.append(assistant_message["content"])

        # Handle tool calls
        while "tool_calls" in assistant_message and assistant_message["tool_calls"]:
            # Add assistant message with tool calls
            messages.append(assistant_message)

            # Execute each tool call
            for tool_call in assistant_message["tool_calls"]:
                function_name = tool_call["function"]["name"]
                function_args = json.loads(tool_call["function"]["arguments"])

                final_text.append(f"\n[Calling tool {function_name} with args {function_args}]")

                # Execute tool via MCP
                result = await self.session.call_tool(function_name, function_args)

                # Add tool result message
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": str(result.content)
                })

            # Get next response
            api_response = await self._call_openrouter(messages, openai_tools)
            assistant_message = api_response["choices"][0]["message"]

            if "content" in assistant_message and assistant_message["content"]:
                final_text.append(assistant_message["content"])

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started! (Using Claude 3.5 Sonnet via OpenRouter)")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
