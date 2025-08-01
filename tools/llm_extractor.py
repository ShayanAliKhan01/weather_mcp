import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

def extract_location_date(user_prompt):
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        print("❌ TOGETHER_API_KEY not found.")
        return None

    prompt = f"""
You are a weather assistant.
Extract only the location and date from the user's question and return them in **pure JSON** format like:
{{ "location": "CityName", "date": "today/tomorrow/2024-07-30" }}

Examples:
- User: What's the weather in Lahore today?
  -> {{ "location": "Lahore", "date": "today" }}
- User: Will it rain in Islamabad on Friday?
  -> {{ "location": "Islamabad", "date": "Friday" }}

Now extract from:
User: "{user_prompt}"
"""

    payload = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0.3,
        "top_p": 0.9
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
                print("❌ Rate limit exceeded.")
                return None
            
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                print("❌ Unexpected response format.")
                return None
                
        except Exception as e:
            if attempt < 2:
                time.sleep(1)
                continue
            print(f"❌ API call failed: {e}")
            return None
    
    return None
