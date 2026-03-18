"""Baidu web search skill - uses official HTTP API."""

import os
import json
import requests
from typing import List, Optional, Dict, Any
from skills.base_search import BaseSearchTool, SearchResult


class BaiduSearchTool(BaseSearchTool):
    """
    Baidu search tool - Chinese web search via official API.
    
    Docs: https://cloud.baidu.com/doc/qianfan-api/s/Wmbq4z7e5
    Endpoint: POST https://qianfan.baidubce.com/v2/ai_search/web_search
    Requires: BAIDU_API_KEY (from Baidu Qianfan/AppBuilder)
    """
    
    name = "baidu_search"
    description = "Baidu Chinese web search (official API)"
    
    def _get_api_key_env(self) -> str:
        return "BAIDU_API_KEY"
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.base_url = "https://qianfan.baidubce.com/v2"
    
    def search(
        self, 
        query: str, 
        num_results: int = 5,
        search_source: str = "baidu_search_v2",
        **kwargs
    ) -> List[SearchResult]:
        """
        Perform Baidu search via official HTTP API.
        
        Args:
            query: Search query (can be Chinese or English)
            num_results: Number of results (top_k)
            search_source: Search source type
        """
        if not self.api_key:
            print("Error: BAIDU_API_KEY not set")
            return []
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [
                    {
                        "content": query,
                        "role": "user"
                    }
                ],
                "search_source": search_source,
                "resource_type_filter": [
                    {
                        "type": "web",
                        "top_k": num_results
                    }
                ]
            }
            
            response = requests.post(
                f"{self.base_url}/ai_search/web_search",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Baidu API error: {response.status_code} - {response.text[:200]}")
                return []
            
            data = response.json()
            results = []
            
            # Parse Baidu search results from response
            # Response has: {"request_id": "...", "references": [...]}
            
            references = data.get("references", [])
            
            for ref in references[:num_results]:
                results.append(SearchResult(
                    title=ref.get("title", ""),
                    link=ref.get("url", ""),
                    snippet=ref.get("snippet", ref.get("content", "")),
                    source="baidu",
                    date=ref.get("date"),
                    website=ref.get("website"),
                    authority_score=ref.get("authority_score")
                ))
            
            return results
            
        except Exception as e:
            print(f"Baidu search error: {e}")
            import traceback
            traceback.print_exc()
            return []


def main():
    """Test the Baidu search tool."""
    tool = BaiduSearchTool()
    results = tool.search("什么是Model Context Protocol?", num_results=3)
    print(json.dumps([r.to_dict() for r in results], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
