import json
import asyncio
import os
from dotenv import load_dotenv
from tools.weather import get_weather_forecast
from tools.llm_extractor import extract_location_date
from tools.llm_responder import generate_weather_response

load_dotenv()

class WeatherMCPServer:
    def __init__(self):
        self.initialized = False
        self.tools = {
            "get_weather_forecast": {
                "description": "Get weather forecast for location and date",
                "inputSchema": {
                    "type": "object",
                    "properties": {"location": {"type": "string"}, "date": {"type": "string"}},
                    "required": ["location", "date"]
                }
            },
            "extract_location_date": {
                "description": "Extract location and date from natural language",
                "inputSchema": {
                    "type": "object",
                    "properties": {"user_input": {"type": "string"}},
                    "required": ["user_input"]
                }
            },
            "process_weather_query": {
                "description": "Complete weather query processing",
                "inputSchema": {
                    "type": "object",
                    "properties": {"user_input": {"type": "string"}},
                    "required": ["user_input"]
                }
            }
        }
    
    async def initialize(self, params):
        if not os.getenv("OPENWEATHER_API_KEY") or not os.getenv("TOGETHER_API_KEY"):
            raise Exception("Missing API keys")
        self.initialized = True
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "weather-mcp-server", "version": "1.0.0"}
        }
    
    async def list_tools(self):
        return [{"name": k, "description": v["description"], "inputSchema": v["inputSchema"]} 
                for k, v in self.tools.items()]
    
    async def call_tool(self, name, arguments):
        if not self.initialized:
            raise Exception("Server not initialized")
        
        if name == "get_weather_forecast":
            result = get_weather_forecast(arguments["location"], arguments["date"])
            return {"content": [{"type": "text", "text": str(result)}]}
        
        elif name == "extract_location_date":
            result = extract_location_date(arguments["user_input"])
            return {"content": [{"type": "text", "text": str(result)}]}
        
        elif name == "process_weather_query":
            user_input = arguments["user_input"]
            
            extracted = extract_location_date(user_input)
            if not extracted:
                return {"content": [{"type": "text", "text": "Error: Could not extract location and date"}]}
            
            if isinstance(extracted, str):
                import re
                try:
                    match = re.search(r'{\s*"location"\s*:\s*".+?",\s*"date"\s*:\s*".+?"\s*}', extracted)
                    if match:
                        extracted = json.loads(match.group(0))
                except:
                    return {"content": [{"type": "text", "text": "Error: Could not parse extracted data"}]}
            
            if not isinstance(extracted, dict) or "location" not in extracted or "date" not in extracted:
                return {"content": [{"type": "text", "text": "Error: Invalid extracted data"}]}
            
            weather = get_weather_forecast(extracted["location"], extracted["date"])
            if not weather:
                return {"content": [{"type": "text", "text": "Error: Could not fetch weather data"}]}
            
            response = generate_weather_response(
                user_input, extracted["location"], extracted["date"],
                weather["description"], weather["temperature"]
            )
            
            return {"content": [{"type": "text", "text": response}]}
        
        else:
            raise Exception(f"Tool '{name}' not found")

async def main():
    server = WeatherMCPServer()

    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, input)
            if not line.strip():
                continue

            message = json.loads(line)
            method = message.get("method")
            params = message.get("params", {})
            request_id = message.get("id")

            try:
                if method == "initialize":
                    result = await server.initialize(params)
                elif method == "tools/list":
                    result = await server.list_tools()
                elif method == "tools/call":
                    result = await server.call_tool(params["name"], params.get("arguments", {}))
                else:
                    raise Exception(f"Unknown method: {method}")

                response = {"jsonrpc": "2.0", "id": request_id, "result": result}

            except Exception as e:
                response = {"jsonrpc": "2.0", "id": request_id, "error": {"code": -1, "message": str(e)}}

            print(json.dumps(response))

        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 