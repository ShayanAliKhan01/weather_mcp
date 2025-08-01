import streamlit as st
import json
import asyncio
import subprocess
import sys
import threading
import time
from typing import Optional

class MCPClient:
    def __init__(self):
        self.process = None
        self.request_id = 0

    def start(self):
        self.process = subprocess.Popen(
            [sys.executable, "mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1
        )

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

    def send(self, method, params=None):
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

    def initialize(self):
        return self.send("initialize")

    def list_tools(self):
        return self.send("tools/list")

    def call_tool(self, name, arguments):
        return self.send("tools/call", {"name": name, "arguments": arguments})

def init_mcp_client():
    if 'mcp_client' not in st.session_state:
        client = MCPClient()
        try:
            client.start()
            client.initialize()
            st.session_state.mcp_client = client
            st.session_state.mcp_ready = True
        except Exception as e:
            st.error(f"Failed to start MCP server: {e}")
            st.session_state.mcp_ready = False

def main():
    st.set_page_config(
        page_title="Weather MCP Assistant",
        page_icon="🌤️",
        layout="wide"
    )

    st.title("🌤️ Weather MCP Assistant")
    st.markdown("A real **Model Context Protocol (MCP)** weather application with AI integration")

    # Initialize MCP client
    init_mcp_client()

    if not st.session_state.get('mcp_ready', False):
        st.error("❌ MCP server not ready. Please check your API keys in `.env` file.")
        st.info("Make sure you have:")
        st.info("- OPENWEATHER_API_KEY")
        st.info("- TOGETHER_API_KEY")
        return

    # Sidebar
    with st.sidebar:
        st.header("🔧 MCP Tools")
        try:
            tools = st.session_state.mcp_client.list_tools()
            for tool in tools:
                st.write(f"• **{tool['name']}**: {tool['description']}")
        except Exception as e:
            st.error(f"Error listing tools: {e}")

        st.header("💡 Examples")
        st.markdown("""
        Try these queries:
        - What's the weather in Karachi today?
        - Will it rain in Lahore tomorrow?
        - What's the weather in Islamabad on Friday?
        - How's the weather in Mecca today?
        """)

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("🌤️ Ask About Weather")
        
        # Chat input
        user_input = st.text_input(
            "Enter your weather question:",
            placeholder="What's the weather in Karachi today?",
            key="user_input"
        )

        if st.button("🔍 Get Weather", type="primary"):
            if user_input.strip():
                with st.spinner("🤖 Processing your request..."):
                    try:
                        result = st.session_state.mcp_client.call_tool(
                            "process_weather_query", 
                            {"user_input": user_input}
                        )
                        
                        response_text = result["content"][0]["text"]
                        
                        if "Error:" in response_text:
                            st.error(response_text)
                        else:
                            st.success("✅ Weather information retrieved!")
                            st.info(f"**Response:** {response_text}")
                            
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

    with col2:
        st.header("📊 Quick Stats")
        
        # Weather API status
        try:
            test_result = st.session_state.mcp_client.call_tool(
                "get_weather_forecast", 
                {"location": "London", "date": "today"}
            )
            st.success("✅ Weather API: Connected")
        except:
            st.error("❌ Weather API: Error")

        # AI API status
        try:
            test_result = st.session_state.mcp_client.call_tool(
                "extract_location_date", 
                {"user_input": "What's the weather in Paris today?"}
            )
            st.success("✅ AI API: Connected")
        except:
            st.error("❌ AI API: Error")

        st.header("🎯 Features")
        st.markdown("""
        ✅ **Real MCP Protocol**
        ✅ **AI-Powered Extraction**
        ✅ **Natural Language Responses**
        ✅ **5-Day Weather Forecasts**
        ✅ **City Name Corrections**
        ✅ **Flexible Date Parsing**
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with <strong>Model Context Protocol (MCP)</strong> | 
        Powered by <strong>OpenWeatherMap</strong> & <strong>Together AI</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 