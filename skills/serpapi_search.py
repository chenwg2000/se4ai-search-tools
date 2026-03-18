"""SerpAPI web search skill."""

import os
import json
from typing import List, Optional, Dict, Any
from skills.base_search import BaseSearchTool, SearchResult

try:
    from serpapi import GoogleSearch
except ImportError:
    GoogleSearch = None


class SerpAPISearchTool(BaseSearchTool):
    """
    SerpAPI search tool - Multi-engine web search (Google, Bing, Yahoo, etc.).
    
    Docs: https://github.com/serpapi/serpapi-mcp
    Requires: SERPAPI_API_KEY
    """
    
    name = "serpapi_search"
    description = "SerpAPI multi-engine web search"
    
    SUPPORTED_ENGINES = [
        "google", "bing", "yahoo", "duckduckgo", "yandex", 
        "baidu", "youtube", "ebay", "walmart"
    ]
    
    def _get_api_key_env(self) -> str:
        return "SERPAPI_API_KEY"
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        if GoogleSearch is None:
            raise ImportError("serpapi package not installed. Run: pip install google-search-results")
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY is required")
    
    def search(
        self, 
        query: str, 
        num_results: int = 5,
        engine: str = "google",
        location: Optional[str] = None,
        **kwargs
    ) -> List[SearchResult]:
        """
        Perform SerpAPI search.
        
        Args:
            query: Search query
            num_results: Number of results
            engine: Search engine (google, bing, yahoo, duckduckgo, etc.)
            location: Location for search (e.g., "Austin, Texas, United States")
        """
        try:
            params = {
                "q": query,
                "engine": engine,
                "api_key": self.api_key,
                "num": num_results
            }
            
            if location:
                params["location"] = location
            
            # Add any additional params
            params.update(kwargs)
            
            search_client = GoogleSearch(params)
            results_data = search_client.get_dict()
            
            if "error" in results_data:
                print(f"SerpAPI error: {results_data['error']}")
                return []
            
            results = []
            
            # Extract organic results
            organic_results = results_data.get("organic_results", [])
            for item in organic_results[:num_results]:
                results.append(SearchResult(
                    title=item.get("title", ""),
                    link=item.get("link", ""),
                    snippet=item.get("snippet", ""),
                    displayed_link=item.get("displayed_link"),
                    source=engine
                ))
            
            # Add answer box if available
            answer_box = results_data.get("answer_box")
            if answer_box:
                answer_text = answer_box.get("answer") or answer_box.get("snippet", "")
                if answer_text:
                    results.insert(0, SearchResult(
                        title="Answer Box",
                        link=answer_box.get("link", ""),
                        snippet=answer_text,
                        is_answer_box=True
                    ))
            
            return results
            
        except Exception as e:
            print(f"SerpAPI search error: {e}")
            return []
    
    def search_news(
        self, 
        query: str, 
        num_results: int = 5,
        **kwargs
    ) -> List[SearchResult]:
        """Search Google News."""
        return self.search(query, num_results, engine="google_news", **kwargs)
    
    def search_images(
        self, 
        query: str, 
        num_results: int = 5,
        **kwargs
    ) -> List[SearchResult]:
        """Search Google Images."""
        return self.search(query, num_results, engine="google_images", **kwargs)


def main():
    """Test the SerpAPI search tool."""
    tool = SerpAPISearchTool()
    
    # Test Google search
    results = tool.search("What is Model Context Protocol?", num_results=3)
    print("Google Search Results:")
    print(json.dumps([r.to_dict() for r in results], indent=2))
    
    # Test Bing search
    results = tool.search("MCP protocol AI", num_results=3, engine="bing")
    print("\nBing Search Results:")
    print(json.dumps([r.to_dict() for r in results], indent=2))


if __name__ == "__main__":
    main()
