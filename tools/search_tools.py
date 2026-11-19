
import os
from tavily import TavilyClient


def search_web(query: str) -> str:
    """Search the web for travel information using Tavily."""

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return "Tavily API key is missing."

    client = TavilyClient(api_key=api_key)

    response = client.search(
        query=query,
        max_results=5
    )

    results = []

    for item in response.get("results", []):
        results.append(
            f"Title: {item.get('title')}\n"
            f"Content: {item.get('content')}\n"
            f"URL: {item.get('url')}"
        )

    return "\n\n".join(results)
