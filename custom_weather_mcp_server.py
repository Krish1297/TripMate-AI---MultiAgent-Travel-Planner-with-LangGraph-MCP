from mcp.server.fastmcp import FastMCP

import os
import requests
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Weather MCP Server")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@mcp.tool()
def get_current_weather(location: str):
    
    response  = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": location,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
    )
    
    data = response.json()
    
    if response.status_code != 200:
        return data
    
    return {
        "location": data["name"],
        "temperature_in_celsius": data["main"]["temp"],
        "feels_like_in_celsius": data["main"]["feels_like"],
        "condition": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }
    
@mcp.tool()
def get_weather_forecast(location: str):
    url = "https://api.openweathermap.org/data/2.5/forecast/daily"
    params={
                "q": location,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric"
            }
    
    response = requests.get(
        url=url,
        params=params
    )
    
    data = response.json()
    
    if response.status_code != 200:
        return data
    
    forecast = []
    
    for item in data["list"][:3]:
        forecast.append({
            "datetime": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "weather": item["weather"][0]["description"],
            })
    
    
    return {
        "location": location,
        "forecast": forecast
    }
    

if __name__ == "__main__":
    mcp.run()