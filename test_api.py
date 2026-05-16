"""
Quick API Test Script
Tests the FastReports API endpoints
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        data = response.json()
        print(f"✓ Root endpoint working")
        print(f"  Version: {data.get('version')}")
        return True
    except Exception as e:
        print(f"✗ Root endpoint failed: {e}")
        return False

def test_datasets():
    """Test datasets listing"""
    print("\nTesting datasets endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/datasets")
        assert response.status_code == 200
        data = response.json()
        datasets = data.get('datasets', [])
        print(f"✓ Datasets endpoint working")
        print(f"  Found {len(datasets)} datasets")
        for ds in datasets[:3]:
            print(f"    - {ds['name']}: {ds['path']}")
        return datasets
    except Exception as e:
        print(f"✗ Datasets endpoint failed: {e}")
        return []

def test_load_data(dataset_path):
    """Test data loading"""
    print(f"\nTesting data loading for: {dataset_path}")
    try:
        response = requests.get(
            f"{BASE_URL}/api/data",
            params={"path": dataset_path, "limit": 10}
        )
        assert response.status_code == 200
        data = response.json()
        print(f"✓ Data loading working")
        print(f"  Total rows: {data.get('total_rows')}")
        print(f"  Returned rows: {data.get('returned_rows')}")
        print(f"  Columns: {len(data.get('columns', []))}")
        print(f"  Quality score: {data.get('stats', {}).get('quality_score')}")
        return True
    except Exception as e:
        print(f"✗ Data loading failed: {e}")
        return False

def test_query():
    """Test SQL query execution"""
    print("\nTesting SQL query endpoint...")
    try:
        # Simple test query
        query_data = {
            "query": "SELECT * FROM temp_data LIMIT 5",
            "data": [
                {"id": 1, "name": "Test 1", "value": 100},
                {"id": 2, "name": "Test 2", "value": 200},
                {"id": 3, "name": "Test 3", "value": 300}
            ]
        }
        
        response = requests.post(
            f"{BASE_URL}/api/query",
            json=query_data
        )
        assert response.status_code == 200
        data = response.json()
        print(f"✓ Query execution working")
        print(f"  Returned rows: {data.get('rows')}")
        print(f"  Success: {data.get('success')}")
        return True
    except Exception as e:
        print(f"✗ Query execution failed: {e}")
        return False

def test_profile(dataset_path):
    """Test dataset profiling"""
    print(f"\nTesting profiling for: {dataset_path}")
    try:
        response = requests.get(
            f"{BASE_URL}/api/profile",
            params={"path": dataset_path}
        )
        assert response.status_code == 200
        data = response.json()
        print(f"✓ Profiling working")
        shape = data.get('shape', {})
        print(f"  Shape: {shape.get('rows')} rows × {shape.get('columns')} columns")
        print(f"  Quality score: {data.get('quality_score')}")
        return True
    except Exception as e:
        print(f"✗ Profiling failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("FastReports API Test Suite")
    print("=" * 60)
    
    # Check if server is running
    print("\nChecking if API server is running...")
    try:
        requests.get(f"{BASE_URL}/", timeout=2)
        print("✓ API server is running")
    except requests.exceptions.ConnectionError:
        print("✗ API server is not running!")
        print("\nPlease start the API server first:")
        print("  ./start_server.sh  (Linux/macOS)")
        print("  start_server.bat   (Windows)")
        sys.exit(1)
    
    # Run tests
    results = []
    
    # Test 1: Root endpoint
    results.append(("Root", test_root()))
    
    # Test 2: List datasets
    datasets = test_datasets()
    results.append(("Datasets", len(datasets) > 0))
    
    # Test 3: Load data (if datasets available)
    if datasets:
        dataset_path = datasets[0]['path']
        results.append(("Load Data", test_load_data(dataset_path)))
        results.append(("Profile", test_profile(dataset_path)))
    
    # Test 4: Query execution
    results.append(("Query", test_query()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
