#!/usr/bin/env python3
"""Test file for Baidu search tool - saves results to files."""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.baidu_search import BaiduSearchTool

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")


def save_results(tool_name, query, results):
    """Save search results to a JSON file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{tool_name}_{timestamp}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    data = {
        "tool": tool_name,
        "query": query,
        "timestamp": datetime.now().isoformat(),
        "result_count": len(results),
        "results": [r.to_dict() for r in results]
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"    💾 Saved to: outputs/{filename}")
    return filepath


def test_baidu_search():
    """Test Baidu search with 3 different queries."""
    print("\n  Testing Baidu Search Tool")
    print("  " + "-" * 50)
    
    tool = BaiduSearchTool()
    
    if not tool.api_key:
        print("  ✗ BAIDU_API_KEY not set")
        return False
    
    print(f"  API Key: {tool.api_key[:30]}...")
    
    queries = [
        ("Chinese Technology", "什么是Model Context Protocol?"),
        ("Mixed Language", "Python programming 教程"),
        ("Chinese Events", "人工智能最新发展"),
    ]
    
    all_passed = True
    saved_files = []
    
    for name, query in queries:
        print(f"\n  Test: {name}")
        print(f"  Query: '{query}'")
        
        try:
            results = tool.search(query=query, num_results=3)
            
            if results and len(results) > 0:
                print(f"    ✓ Got {len(results)} results")
                r = results[0]
                print(f"    Title: {r.title[:70]}{'...' if len(r.title) > 70 else ''}")
                
                # Save results to file
                filepath = save_results("baidu", query, results)
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
    """Run all Baidu tests."""
    print("\n" + "=" * 60)
    print("BAIDU SEARCH TESTS")
    print("=" * 60)
    
    try:
        passed = test_baidu_search()
    except Exception as e:
        print(f"\n  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        passed = False
    
    print("\n" + "-" * 60)
    print(f"Baidu Tests: {'✓ PASSED' if passed else '✗ FAILED'}")
    print("-" * 60)
    
    return passed


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
