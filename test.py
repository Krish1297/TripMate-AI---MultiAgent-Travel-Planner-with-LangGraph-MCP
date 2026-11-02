import asyncio
# from mcp_client_test import get_all_tools,get_tavily_search_tool,tavily_mcp_search
from mcp_client import get_all_tools


if __name__ == "__main__":
    query = "Find the best travel destinations in Paris for a 3-day trip in September."
    # asyncio.run(tavily_mcp_search(query))
    asyncio.run(get_all_tools())
