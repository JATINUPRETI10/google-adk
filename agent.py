from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from .tools.search_tools import search_web
from .tools.budget_tools import calculate_trip_budget
from .tools.time_tools import get_city_time


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

Keep responses simple, practical, and well-organized.
""",
    tools=[
        calculate_trip_budget,
        get_city_time,
        search_web
    ]
)