from langchain_core.tools import tool
from tavily import TavilyClient
import config

@tool
def web_search(query: str , search_depth: str = "basic") -> str:
    """Perform a web search using Tavily and return the results."""
    """"search_depth can advanced, basic, fast, ultra-fast , Note : advanced is the most comprehensive search (only use we really needed), while ultra-fast is the quickest but may provide less detailed results."""
    if not config.TAVILY_API_KEY:
        return "TAVILY_API_KEY is not set."

    client = TavilyClient(api_key=config.TAVILY_API_KEY)
    response = client.search(
        query=query,
        search_depth=search_depth
    )
    return str(response)
