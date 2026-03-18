#!/usr/bin/env python3
"""
Simple test runner for search tool skills.
Run: python run_tests.py
"""

import sys
import os
import importlib.util
import traceback

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_test_file(test_path):
    """Run a single test file and return results."""
    print(f"\n{'='*60}")
    print(f"Running: {test_path}")
    print('='*60)
    
    try:
        spec = importlib.util.spec_from_file_location("test_module", test_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Look for run_tests() function
        if hasattr(module, 'run_tests'):
            result = module.run_tests()
            if result:
                print(f"✓ PASSED: {test_path}")
                return True
            else:
                print(f"✗ FAILED: {test_path}")
                return False
        else:
            print(f"⚠ No run_tests() function found in {test_path}")
            return None
    except Exception as e:
        print(f"✗ ERROR in {test_path}:")
        traceback.print_exc()
        return False


def main():
    """Run all test files in tests/ directory."""
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    
    if not os.path.exists(tests_dir):
        print("No tests directory found.")
        return
    
    test_files = sorted([
        os.path.join(tests_dir, f) 
        for f in os.listdir(tests_dir) 
        if f.endswith('.py') and not f.startswith('_')
    ])
    
    if not test_files:
        print("No test files found in tests/ directory.")
        return
    
    results = {'passed': 0, 'failed': 0, 'skipped': 0}
    
    for test_file in test_files:
        result = run_test_file(test_file)
        if result is True:
            results['passed'] += 1
        elif result is False:
            results['failed'] += 1
        else:
            results['skipped'] += 1
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    print(f"Passed:   {results['passed']}")
    print(f"Failed:   {results['failed']}")
    print(f"Skipped:  {results['skipped']}")
    print(f"Total:    {sum(results.values())}")
    
    return 0 if results['failed'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
