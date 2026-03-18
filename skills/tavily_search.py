"""Tavily web search skill."""

import os
import json
from typing import List, Optional, Dict, Any
from skills.base_search import BaseSearchTool, SearchResult

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None


class TavilySearchTool(BaseSearchTool):
    """
    Tavily search tool - AI-powered web search.
    
    Docs: https://github.com/tavily-ai/tavily-mcp
    Requires: TAVILY_API_KEY
    """
    
    name = "tavily_search"
    description = "Tavily AI-powered web search"
    
    def _get_api_key_env(self) -> str:
        return "TAVILY_API_KEY"
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        if TavilyClient is None:
            raise ImportError("tavily package not installed. Run: pip install tavily")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY is required")
        self.client = TavilyClient(api_key=self.api_key)
    
    def search(
        self, 
        query: str, 
        num_results: int = 5,
        search_depth: str = "basic",
        include_answer: bool = True,
        **kwargs
    ) -> List[SearchResult]:
        """
        Perform Tavily search.
        
        Args:
            query: Search query
            num_results: Number of results
            search_depth: "basic" or "advanced"
            include_answer: Include AI-generated answer
        """
        try:
            response = self.client.search(
                query=query,
                max_results=num_results,
                search_depth=search_depth,
                include_answer=include_answer,
                **kwargs
            )
            
            results = []
            for item in response.get("results", []):
                results.append(SearchResult(
                    title=item.get("title", ""),
                    link=item.get("url", ""),
                    snippet=item.get("content", ""),
                    score=item.get("score"),
                    raw_content=item.get("raw_content")
                ))
            
            # Add AI answer as first result if available
            if include_answer and response.get("answer"):
                results.insert(0, SearchResult(
                    title="AI Answer",
                    link="",
                    snippet=response["answer"],
                    is_ai_answer=True
                ))
            
            return results
            
        except Exception as e:
            print(f"Tavily search error: {e}")
            return []


def main():
    """Test the Tavily search tool."""
    tool = TavilySearchTool()
    results = tool.search("What is Model Context Protocol?", num_results=3)
    print(tool.search_to_json("What is Model Context Protocol?", num_results=3))


if __name__ == "__main__":
    main()
