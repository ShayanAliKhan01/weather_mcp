import requests
import datetime
import dateparser
import os
from dotenv import load_dotenv

load_dotenv()

CITY_FIXES = {
    "karchi": "Karachi", "lahor": "Lahore", "islamabd": "Islamabad",
    "madina": "Medina", "makah": "Mecca", "makka": "Mecca", 
    "makkah": "Mecca", "mecca": "Mecca"
}

DAYS = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6}

def get_next_weekday(day_name):
    day_name = day_name.lower()
    if day_name not in DAYS:
        return None
    
    target_day = DAYS[day_name]
    today = datetime.date.today()
    days_ahead = target_day - today.weekday()
    
    if days_ahead <= 0:
        days_ahead += 7
    
    return today + datetime.timedelta(days=days_ahead)

def get_weather_forecast(location, date_text):
    location = location.strip().title()
    location = CITY_FIXES.get(location.lower(), location)

    day_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    if date_text.lower() in day_names:
        target_date = get_next_weekday(date_text)
    else:
        parsed_date = dateparser.parse(date_text)
        if not parsed_date:
            print("❌ Couldn't parse date.")
            return None
        target_date = parsed_date.date()

    today = datetime.date.today()
    max_date = today + datetime.timedelta(days=4)
    if target_date > max_date:
        print(f"❌ Forecast only available for next 5 days (up to {max_date.strftime('%Y-%m-%d')})")
        return None

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("❌ OPENWEATHER_API_KEY not found.")
        return None

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except:
        print("❌ Error fetching weather data.")
        return None

    forecast_list = data.get("list", [])
    for entry in forecast_list:
        dt_txt = entry["dt_txt"]
        entry_date = datetime.datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S").date()
        
        if entry_date == target_date:
            return {
                "description": entry["weather"][0]["description"].capitalize(),
                "temperature": entry["main"]["temp"]
            }
    
    print("❌ Forecast not available for that date.")
    return None
