# Weather MCP Server

A real **Model Context Protocol (MCP)** server that provides weather forecasting capabilities with AI integration.

## 🌟 **MCP Features**

### **True MCP Protocol Implementation**
- ✅ **MCP Server**: Implements proper MCP protocol with JSON-RPC
- ✅ **Tool Registration**: Tools are properly registered with schemas
- ✅ **Async Support**: Full async/await support for concurrent operations
- ✅ **Error Handling**: Proper MCP error responses
- ✅ **Message Protocol**: JSON-RPC 2.0 message format

### **Available MCP Tools**

#### **`get_weather_forecast`**
- **Description**: Get weather forecast for a location and date
- **Input**: `{"location": "Karachi", "date": "today"}`

#### **`extract_location_date`**
- **Description**: Extract location and date from natural language using AI
- **Input**: `{"user_input": "What's the weather in Karachi today?"}`

#### **`generate_weather_response`**
- **Description**: Generate natural language weather response using AI
- **Input**: User input, location, date, weather description, temperature

#### **`process_weather_query`**
- **Description**: Complete weather query processing pipeline
- **Input**: `{"user_input": "What's the weather in Karachi today?"}`

## 🚀 **Usage**

### **Command Line Interface:**
```bash
uv run mcp_client.py
```

### **Web Interface (Streamlit):**
```bash
uv run streamlit run streamlit_app.py
```

Then open your browser to: http://localhost:8501

## 🔧 **Setup**

1. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

2. **Get API Keys:**
   - **OpenWeatherMap API**: [OpenWeatherMap](https://openweathermap.org/api)
   - **Together AI API**: [Together AI](https://together.ai)

3. **Create `.env` file:**
   ```
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   TOGETHER_API_KEY=your_together_ai_api_key_here
   ```

## 🔍 **Example**

### **Command Line:**
```
You: What's the weather in Karachi today?
🤖 The weather in Karachi today is sunny with a temperature of 28°C.

You: Will it rain in Lahore tomorrow?
🤖 Tomorrow in Lahore, expect partly cloudy conditions with a temperature of 25°C.
```

### **Web Interface:**
- Beautiful Streamlit UI with real-time weather queries
- Sidebar showing available MCP tools
- API status indicators
- Example queries and features list

## 🏗️ **Files**

- **`mcp_server.py`** - MCP server implementation
- **`mcp_client.py`** - MCP client for user interaction
- **`streamlit_app.py`** - Web interface (Streamlit)
- **`tools/`** - Core functionality modules

## 🎉 **Real MCP Project!**

✅ **True MCP Protocol Implementation**
✅ **Tool Registration and Discovery**
✅ **JSON-RPC Message Handling**
✅ **Async Support**
✅ **Extensible Architecture**

Follows official Model Context Protocol specification! # weather_mcp
