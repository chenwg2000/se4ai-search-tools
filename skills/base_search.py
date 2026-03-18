"""Base class for web search tools."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import json
import os


class SearchResult:
    """Represents a single search result."""
    
    def __init__(self, title: str, link: str, snippet: str, **extra):
        self.title = title
        self.link = link
        self.snippet = snippet
        self.extra = extra
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "link": self.link,
            "snippet": self.snippet,
            **self.extra
        }
    
    def __repr__(self):
        return f"SearchResult(title={self.title[:50]}..., link={self.link})"


class BaseSearchTool(ABC):
    """Abstract base class for web search tools."""
    
    name: str = "base_search"
    description: str = "Base search tool"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv(self._get_api_key_env())
    
    @abstractmethod
    def _get_api_key_env(self) -> str:
        """Return the environment variable name for API key."""
        pass
    
    @abstractmethod
    def search(self, query: str, num_results: int = 5, **kwargs) -> List[SearchResult]:
        """
        Perform a web search.
        
        Args:
            query: The search query string
            num_results: Number of results to return (default: 5)
            **kwargs: Additional search parameters
            
        Returns:
            List of SearchResult objects
        """
        pass
    
    def search_to_json(self, query: str, num_results: int = 5, **kwargs) -> str:
        """Perform search and return results as JSON string."""
        results = self.search(query, num_results, **kwargs)
        return json.dumps([r.to_dict() for r in results], ensure_ascii=False, indent=2)
