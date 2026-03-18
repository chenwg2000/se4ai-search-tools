"""Metaso web search skill - uses official HTTP API."""

import os
import json
import requests
from typing import List, Optional, Dict, Any
from skills.base_search import BaseSearchTool, SearchResult


class MetasoSearchTool(BaseSearchTool):
    """
    Metaso (秘塔) AI search tool - Chinese AI search engine.
    
    Docs: https://metaso.cn (API docs in console)
    Endpoint: POST https://metaso.cn/api/v1/search
    Requires: METASO_API_KEY (format: mk-xxxxxxxx)
    """
    
    name = "metaso_search"
    description = "Metaso AI Chinese search (official API)"
    
    def _get_api_key_env(self) -> str:
        return "METASO_API_KEY"
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.base_url = os.getenv("METASO_BASE_URL", "https://metaso.cn/api/v1")
    
    def search(
        self, 
        query: str, 
        num_results: int = 10,
        scope: str = "webpage",
        include_summary: bool = False,
        **kwargs
    ) -> List[SearchResult]:
        """
        Perform Metaso search via official HTTP API.
        
        Args:
            query: Search query
            num_results: Number of results (size)
            scope: Search scope - webpage, document, paper, image, video, podcast
            include_summary: Include AI summary
        """
        if not self.api_key:
            print("Error: METASO_API_KEY not set")
            return []
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            payload = {
                "q": query,
                "scope": scope,
                "size": str(num_results),
                "includeSummary": include_summary,
                "includeRawContent": False
            }
            
            response = requests.post(
                f"{self.base_url}/search",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code != 200:
                print(f"Metaso API error: {response.status_code} - {response.text[:200]}")
                return []
            
            data = response.json()
            results = []
            
            # Parse Metaso response format
            # Response has: {"credits": 3, "searchParameters": {...}, "webpages": [...]}
            
            webpages = data.get("webpages", [])
            
            for item in webpages[:num_results]:
                results.append(SearchResult(
                    title=item.get("title", ""),
                    link=item.get("link", ""),
                    snippet=item.get("snippet", ""),
                    source="metaso",
                    score=item.get("score"),
                    position=item.get("position"),
                    date=item.get("date")
                ))
            
            return results
            
        except Exception as e:
            print(f"Metaso search error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def read_webpage(self, url: str, format: str = "markdown") -> str:
        """
        Read webpage content using Metaso reader API.
        
        Args:
            url: Webpage URL
            format: Output format - markdown or json
        """
        if not self.api_key:
            return "Error: METASO_API_KEY not set"
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            payload = {
                "url": url,
                "format": format
            }
            
            response = requests.post(
                f"{self.base_url}/reader",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                return f"Error: {response.status_code} - {response.text[:200]}"
            
            data = response.json()
            return data.get("content", json.dumps(data, ensure_ascii=False))
            
        except Exception as e:
            return f"Error reading webpage: {e}"


def main():
    """Test the Metaso search tool."""
    tool = MetasoSearchTool()
    results = tool.search("什么是MCP协议?", num_results=3)
    print(json.dumps([r.to_dict() for r in results], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
