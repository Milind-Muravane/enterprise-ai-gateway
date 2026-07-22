"""
Tavily Search Client

Retrieves current information from the web.
"""

from tavily import TavilyClient
from src.config import settings
from src.schemas import (SearchResult,WebSearchResult,)

class TavilySearch:
    def __init__(self):
        self.client = TavilyClient(api_key= settings.tavily_api_key)

    def search(self,query: str, max_results : int = 3,)-> WebSearchResult:
        response  = self.client.search(query = query, max_results = max_results)

        results = []

        for item in response.get("results", []):
            results.append(
                SearchResult(title = item.get("title", ""),
                url = item.get("url",""),
                content = item.get("content", "")
                
                )
            )

        return WebSearchResult(query = query,results = results)