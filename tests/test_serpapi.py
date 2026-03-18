#!/usr/bin/env python3
"""Test file for SerpAPI search tool - saves results to files."""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.serpapi_search import SerpAPISearchTool

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")


def save_results(tool_name, query, results, engine=None, location=None):
    """Save search results to a JSON file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{tool_name}_{timestamp}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    data = {
        "tool": tool_name,
        "query": query,
        "engine": engine,
        "location": location,
        "timestamp": datetime.now().isoformat(),
        "result_count": len(results),
        "results": [r.to_dict() for r in results]
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"    💾 Saved to: outputs/{filename}")
    return filepath


def test_serpapi_search():
    """Test SerpAPI search with 3 different queries."""
    print("\n  Testing SerpAPI Search Tool")
    print("  " + "-" * 50)
    
    tool = SerpAPISearchTool()
    print(f"  API Key: {tool.api_key[:20]}...")
    
    queries = [
        ("Google Search", "What is Model Context Protocol?", "google", None),
        ("Bing Search", "Anthropic MCP documentation", "bing", None),
        ("Location-based", "weather today", "google", "New York, United States"),
    ]
    
    all_passed = True
    saved_files = []
    
    for name, query, engine, location in queries:
        print(f"\n  Test: {name}")
        print(f"  Query: '{query}'")
        print(f"  Engine: {engine}")
        if location:
            print(f"  Location: {location}")
        
        kwargs = {"query": query, "num_results": 3, "engine": engine}
        if location:
            kwargs["location"] = location
        
        results = tool.search(**kwargs)
        
        if results and len(results) > 0:
            print(f"    ✓ Got {len(results)} results")
            r = results[0]
            print(f"    Title: {r.title[:70]}{'...' if len(r.title) > 70 else ''}")
            
            # Save results to file
            filepath = save_results("serpapi", query, results, engine, location)
            saved_files.append(filepath)
        else:
            print(f"    ✗ No results")
            all_passed = False
    
    if saved_files:
        print(f"\n  📁 Saved {len(saved_files)} result files to outputs/")
    
    return all_passed


def run_tests():
    """Run all SerpAPI tests."""
    print("\n" + "=" * 60)
    print("SERPAPI SEARCH TESTS")
    print("=" * 60)
    
    try:
        passed = test_serpapi_search()
    except Exception as e:
        print(f"\n  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        passed = False
    
    print("\n" + "-" * 60)
    print(f"SerpAPI Tests: {'✓ PASSED' if passed else '✗ FAILED'}")
    print("-" * 60)
    
    return passed


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
