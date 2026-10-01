import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError(
        "TAVILY_API_KEY not found in .env file."
    )

tavily_client = TavilyClient(
    api_key=TAVILY_API_KEY
)


def web_search(query: str):
    """
    Search the web using Tavily.

    Args:
        query: User's research query.

    Returns:
        List of search results containing title, URL,
        and relevant content.
    """

    try:
        response = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=True
        )

        results = response.get("results", [])

        formatted_results = []

        for result in results:
            formatted_results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", "")
            })

        return formatted_results

    except Exception as e:
        return [
            {
                "title": "Search Error",
                "url": "",
                "content": str(e)
            }
        ]