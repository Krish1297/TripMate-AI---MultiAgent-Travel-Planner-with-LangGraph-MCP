# ✈️ TripMate AI — A Multi-Agent Travel Planner with LangGraph, MCP 

AI travel planner that turns a natural-language trip request into a practical travel plan with flight, hotel and itinerary suggestions. The project uses a multi-agent workflow built with LangGraph, LangChain, MCP and FastAPI.

## Why this project?

We usally plan a trip by looking different websites, tools, and spreadsheets. This project brings everything into one experience by combining:

- flight-search agent,
- hotel-research agent,
- weather agent
- itinerary-planning agent, and
- final response agent,

All agents are coordinated through LangGraph.

## Features
- Flight research using AviationStack through a local MCP server
- Hotel research using Tavily through a remote MCP server
- Current weather and forecast information using a custom local MCP server
- Multi-agent orchestration with LangGraph
- Structured, weather-aware travel itinerary generation
- FastAPI backend with a simple web interface
- Conversation state persistence using PostgreSQL
- LLM-powered responses with Groq

## Tech Stack
- Python 3.10+
- FastAPI
- Jinja2 + HTML/CSS/JavaScript frontend
- LangGraph
- LangChain
- Model Context Protocol (MCP)
- Groq LLMs
- PostgreSQL
- Tavily API
- AviationStack API
- OpenWeather API

## Project Structure

```text
.
├── app.py                # FastAPI app entry point
├── backend.py            # LangGraph travel workflow
├── requirements.txt      # Python dependencies
├── mcp_client.py                  # MCP client configuration and tool integration
├── custom_weather_mcp_server.py   # Custom local Weather MCP server
├── static/               # Static frontend assets
├── templates/            # HTML templates
└── tools/                # Flight and web search integrations
```

## Prerequisites

Before running the project locally, make sure you have:

- Python 3.10 or newer installed
- PostgreSQL running and accessible
- API keys for:
  - Groq
  - Tavily
  - AviationStack
  - OpenWeather

## Environment Variables

Create a .env file in the project root with the following variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/travel_db
GROQ_API_KEY=your_groq_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
DEFAULT_ORIGIN_IATA=<Origin International Airport 3 letter abbreviation>
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the App

Start the FastAPI server:

```bash
python app.py
```

Then open your browser at:

```text
http://127.0.0.1:8000/
```

## API Endpoints

- GET /health - Health check
- POST /api/travel - Submit a travel request

Example request:

```bash
curl -X POST http://127.0.0.1:8000/api/travel \
  -H "Content-Type: application/json" \
  -d '{"message":"Plan a 3-day trip to Tokyo with a budget of $1200"}'
```

## How the Workflow Works
1. User submits a travel request in natural language.
2. Flight agent retrieves flight-related information using AviationStack MCP.
3. Hotel agent researches accommodation using Tavily remote MCP.
4. Weather agent retrieves current weather and forecast using custom local MCP.
5. Itinerary agent generates a practical, weather-aware travel itinerary.
6. Final agent combines the results into a structured travel response.