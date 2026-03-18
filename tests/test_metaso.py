#!/usr/bin/env python3
"""Test file for Metaso search tool - saves results to files."""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.metaso_search import MetasoSearchTool

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")


def save_results(tool_name, query, results, scope=None):
    """Save search results to a JSON file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{tool_name}_{timestamp}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    data = {
        "tool": tool_name,
        "query": query,
        "scope": scope,
        "timestamp": datetime.now().isoformat(),
        "result_count": len(results),
        "results": [r.to_dict() for r in results]
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"    💾 Saved to: outputs/{filename}")
    return filepath


def test_metaso_search():
    """Test Metaso search with 3 different queries."""
    print("\n  Testing Metaso Search Tool")
    print("  " + "-" * 50)
    
    tool = MetasoSearchTool()
    
    if not tool.api_key:
        print("  ✗ METASO_API_KEY not set")
        return False
    
    print(f"  API Key: {tool.api_key[:30]}...")
    
    queries = [
        ("Chinese AI", "什么是MCP协议?", "webpage"),
        ("Academic Paper", "大语言模型 研究进展", "paper"),
        ("Document Search", "Python机器学习实践", "document"),
    ]
    
    all_passed = True
    saved_files = []
    
    for name, query, scope in queries:
        print(f"\n  Test: {name}")
        print(f"  Query: '{query}'")
        print(f"  Scope: {scope}")
        
        try:
            results = tool.search(query=query, num_results=3, scope=scope)
            
            if results and len(results) > 0:
                print(f"    ✓ Got {len(results)} results")
                r = results[0]
                print(f"    Title: {r.title[:70]}{'...' if len(r.title) > 70 else ''}")
                
                # Save results to file
                filepath = save_results("metaso", query, results, scope)
                saved_files.append(filepath)
            else:
                print(f"    ✗ No results")
                all_passed = False
        except Exception as e:
            print(f"    ✗ Error: {e}")
            all_passed = False
    
    if saved_files:
        print(f"\n  📁 Saved {len(saved_files)} result files to outputs/")
    
    return all_passed


def run_tests():
    """Run all Metaso tests."""
    print("\n" + "=" * 60)
    print("METASO SEARCH TESTS")
    print("=" * 60)
    
    try:
        passed = test_metaso_search()
    except Exception as e:
        print(f"\n  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        passed = False
    
    print("\n" + "-" * 60)
    print(f"Metaso Tests: {'✓ PASSED' if passed else '✗ FAILED'}")
    print("-" * 60)
    
    return passed


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
