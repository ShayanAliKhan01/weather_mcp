import json
import asyncio
import subprocess
import sys

class MCPClient:
    def __init__(self):
        self.process = None
        self.request_id = 0

    async def start(self):
        self.process = subprocess.Popen(
            [sys.executable, "mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        print("🚀 Started MCP server")

    async def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

    async def send(self, method, params=None):
        self.request_id += 1
        message = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }

        message_str = json.dumps(message) + "\n"
        self.process.stdin.write(message_str)
        self.process.stdin.flush()

        response_line = self.process.stdout.readline()
        response = json.loads(response_line.strip())

        if "error" in response:
            raise Exception(f"Server error: {response['error']['message']}")

        return response["result"]

    async def initialize(self):
        return await self.send("initialize")

    async def list_tools(self):
        return await self.send("tools/list")

    async def call_tool(self, name, arguments):
        return await self.send("tools/call", {"name": name, "arguments": arguments})

async def main():
    client = MCPClient()

    try:
        await client.start()

        init_result = await client.initialize()
        print(f"✅ Server: {init_result['serverInfo']['name']} v{init_result['serverInfo']['version']}")

        tools = await client.list_tools()
        print(f"🔧 Tools ({len(tools)}):")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
        print()

        print("🧠 Weather MCP Client Ready!")
        print("💡 Try: 'What's the weather in Karachi today?'")
        print("📝 Type 'exit' to quit\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ["exit", "quit"]:
                    print("👋 Goodbye!")
                    break

                if not user_input:
                    continue

                print("🤖 Processing...")

                result = await client.call_tool("process_weather_query", {"user_input": user_input})

                if "Error:" in result["content"][0]["text"]:
                    print(f"❌ {result['content'][0]['text']}")
                else:
                    print("🤖", result["content"][0]["text"])

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    finally:
        await client.stop()

if __name__ == "__main__":
    asyncio.run(main()) 