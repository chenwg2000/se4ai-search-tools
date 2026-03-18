"""Kimi built-in web search skill.

NOTE: This tool only works inside the Kimi CLI environment.
When running standalone, it will return empty results.
"""

import json
from typing import List, Optional
from skills.base_search import BaseSearchTool, SearchResult


class KimiWebSearchTool(BaseSearchTool):
    """
    Kimi built-in web search tool.
    
    STATUS: ⚠️ Only available in Kimi CLI environment
    
    This is a wrapper around Kimi's built-in SearchWeb tool.
    When running outside Kimi CLI, it returns empty results.
    """
    
    name = "kimi_web_search"
    description = "Kimi built-in web search (Kimi CLI only)"
    
    def _get_api_key_env(self) -> str:
        return ""  # No API key needed
    
    def __init__(self, api_key: Optional[str] = None):
        pass  # No initialization needed
    
    def search(
        self, 
        query: str, 
        num_results: int = 5,
        **kwargs
    ) -> List[SearchResult]:
        """
        Perform web search using Kimi's built-in tool.
        
        NOTE: Only works inside Kimi CLI environment.
        """
        try:
            # Try to import Kimi's SearchWeb tool
            from kimi_cli.tools import SearchWeb
            
            results_data = SearchWeb(
                query=query,
                limit=num_results
            )
            
            results = []
            for item in results_data:
                results.append(SearchResult(
                    title=item.get("title", ""),
                    link=item.get("url", ""),
                    snippet=item.get("summary", ""),
                    source=item.get("source", "web")
                ))
            
            return results
            
        except ImportError:
            print("⚠️  Kimi SearchWeb tool only available in Kimi CLI environment")
            print(f"   Query would be: '{query}'")
            return []
        except Exception as e:
            print(f"   Search error: {e}")
            return []


def main():
    """Test the Kimi web search tool."""
    tool = KimiWebSearchTool()
    results = tool.search("What is Model Context Protocol?", num_results=3)
    print(json.dumps([r.to_dict() for r in results], indent=2))


if __name__ == "__main__":
    main()
