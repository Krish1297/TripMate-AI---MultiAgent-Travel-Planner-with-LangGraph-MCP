import os
import asyncio
from pathlib import Path
import sys

import certifi
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient


os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


PROJECT_DIR = Path(__file__).resolve().parent
WEATHER_SERVER_PATH = PROJECT_DIR / "custom_weather_mcp_server.py"

llm = ChatGroq(
                model ="openai/gpt-oss-120b",
                api_key=os.getenv("GROQ_API_KEY"),
                max_tokens=2048
                )

client = MultiServerMCPClient(
    {
        "tavily": {
            "transport": "streamable_http",
            "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}",
        },

        "aviationstack": {
            "transport": "stdio",
            "command": "uvx",
            "args": [
                "aviationstack-mcp"
            ],
            "env": {
                "AVIATION_STACK_API_KEY": AVIATIONSTACK_API_KEY
            }
        },

        "weather": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [
                str(WEATHER_SERVER_PATH)
            ],
            "env": {
                "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY
            }
        },


    }
)


# ====================================
# Diagnostic function
# ====================================

async def get_all_tools():

    tools = await client.get_tools()
    print("Available MCP tools:")

    for tool in tools:
        print(f"{tool.name}")


# ====================================
# Tavily and Aviation tool
# ====================================

search_tool = None
aviation_tool = {}


async def initialize_mcp():
    global search_tool, aviation_tool

    if search_tool is not None and aviation_tool is not None:
        return

    tools = await client.get_tools()
    print("Available MCP tools:")

    for tool in tools:
        print(f"{tool.name}")

    search_tool = next(
        (tool for tool in tools if tool.name == "tavily_search"), None)
    aviation_tool = {
        tool.name: tool for tool in tools if tool.name != "tavily_search"}


async def tavily_mcp_search(query):
    await initialize_mcp()
    result = await search_tool.ainvoke({
        "query": query
    })
    print("MCP Search Result:")
    print(result)
    return result


async def aviation_mcp_call(tool_name, tool_args):
    tools = await client.get_tools()

    tool = next((tool for tool in tools if tool.name == tool_name))

    result = await tool.ainvoke(tool_args or {})

    return result

# ============================
# Weather tools
# ============================

weather_tool = None
forecast_tool = None

async def initialize_weather_tools():
    global weather_tool, forecast_tool
    
    if weather_tool is not None and forecast_tool is not None:
        return
    
    tools = await client.get_tools()
    
    weather_tool = next((tool for tool in tools if tool.name == "get_current_weather"))
    forecast_tool = next((tool for tool in tools if tool.name == "get_weather_forecast"))
     
     
async def weather_mcp_search(location: str):
    await initialize_weather_tools()
    result = await weather_tool.ainvoke({ "location": location })
    print("MCP Weather Result:")
    print(result)
    return result

async def weather_mcp_forecast(location: str):
    await initialize_weather_tools()
    result = await forecast_tool.ainvoke({ "location": location })
    print("MCP Weather Forecast Result:")
    print(result)
    return result


# ============================
# Destination Extractor
# ============================

def extract_destination(query: str) -> str:
    
    prompt = f"""
    Extract the destination city or country from the query.

    query: {query}
    
    Return only destination name
    """
    
    response = llm.invoke(prompt)
    
    return response.content.strip()