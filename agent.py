
import os

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from .tools.search_tools import search_web
from .tools.budget_tools import calculate_trip_budget
from .tools.time_tools import get_city_time
from .tools.database_tools import save_itinerary, get_itineraries

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
    StreamableHTTPConnectionParams
)
from mcp import StdioServerParameters


# ----------------------------------
# 1. Filesystem MCP Server (Local)
# ----------------------------------

filesystem_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-filesystem",
                "D:\\google adk\\mcp_workspace"
            ],
        ),
    ),
)


# ----------------------------------
# 2. GitHub MCP Server (Remote)
# ----------------------------------

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found in environment variables")

github_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://api.githubcopilot.com/mcp/",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}"
        }
    )
)


# ----------------------------------
# 3. TripMate AI Agent
# ----------------------------------

root_agent = Agent(
    model=LiteLlm(
        model="openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"
    ),
    name="tripmate",
    description="A basic AI travel planning assistant.",

    instruction="""
You are TripMate, a helpful AI travel planning assistant.

Your responsibilities:
- Help users explore travel destinations and tourist attractions.
- Suggest places to visit based on their interests.
- Create simple day-wise travel itineraries.
- Provide estimated travel budgets using the budget calculator.
- Provide local time using the city time tool.
- Use web search to find up-to-date information about destinations, attractions, transportation, and travel-related updates.
- When using web search, summarize the findings clearly and include relevant source links.
- If information is uncertain or unavailable, tell the user instead of making assumptions.

- Save a user's travel itinerary when they explicitly ask you to save it.
- Use the save_itinerary tool to store the destination, trip duration, and itinerary.
- Confirm when an itinerary has been saved successfully.
- Retrieve previously saved itineraries when users ask about their travel plans.
- Use get_itineraries to search the database by destination.
- Present the retrieved itinerary clearly. If no record exists, tell the user.

- Keep responses simple, practical, and well-organized.

- You can use filesystem MCP tools to create, read, list, and manage files inside the permitted workspace.
- When users ask you to create or read files, use the appropriate filesystem MCP tool.
- Never claim a file operation succeeded unless the tool confirms it.

- You can use GitHub MCP tools to inspect repositories, branches, commits, issues, and files.
- When users ask about GitHub repositories, use the appropriate GitHub MCP tools.
- Never claim a GitHub operation succeeded unless the tool confirms it.
""",

    tools=[
        calculate_trip_budget,
        get_city_time,
        search_web,
        save_itinerary,
        get_itineraries,
        filesystem_toolset,
        github_toolset
    ]
)

