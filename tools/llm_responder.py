import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

def generate_weather_response(user_input, location, date, description, temperature):
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        print("❌ TOGETHER_API_KEY not found.")
        return "❌ Error: API key not configured."

    prompt = f"""
You are a helpful weather assistant.

The user asked: "{user_input}"
Real-time weather data:
- Location: {location}
- Date: {date}
- Description: {description}
- Temperature: {temperature}°C

Now write a friendly and helpful response to the user in natural language.
"""

    payload = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,
        "temperature": 0.6
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    for attempt in range(3):
        try:
            response = requests.post("https://api.together.xyz/v1/chat/completions", 
                                  headers=headers, json=payload)
            
            if response.status_code == 429:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                return "❌ Rate limit exceeded."
            
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"].strip()
            else:
                return "❌ Error: Unexpected response format."
                
        except Exception as e:
            if attempt < 2:
                time.sleep(1)
                continue
            print(f"❌ API call failed: {e}")
            return "❌ Error: Could not generate response."
    
    return "❌ Error: Could not generate response."
