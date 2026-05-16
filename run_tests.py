#!/usr/bin/env python3
"""
Test runner script for FastReports.
Runs all tests and generates a summary report.
"""
import sys
import subprocess
import os
from pathlib import Path


def check_pytest_installed():
    """Check if pytest is installed."""
    try:
        import pytest
        return True
    except ImportError:
        return False


def install_pytest():
    """Install pytest if not available."""
    print("Installing pytest...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest"])


def run_unit_tests():
    """Run unit tests."""
    print("\n" + "="*70)
    print("RUNNING UNIT TESTS")
    print("="*70 + "\n")
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_ingestion.py", 
         "tests/test_profiling.py", "tests/test_cleaning.py", "-v"],
        cwd=Path(__file__).parent
    )
    return result.returncode


def run_integration_tests():
    """Run integration tests."""
    print("\n" + "="*70)
    print("RUNNING INTEGRATION TESTS")
    print("="*70 + "\n")
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_integration.py", "-v"],
        cwd=Path(__file__).parent
    )
    return result.returncode


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("RUNNING ALL TESTS")
    print("="*70 + "\n")
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        cwd=Path(__file__).parent
    )
    return result.returncode


def main():
    """Main test runner."""
    print("FastReports Test Suite")
    print("="*70)
    
    # Check pytest
    if not check_pytest_installed():
        print("pytest not found. Installing...")
        try:
            install_pytest()
        except Exception as e:
            print(f"Error installing pytest: {e}")
            print("Please install pytest manually: pip install pytest")
            return 1
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        if test_type == "unit":
            return run_unit_tests()
        elif test_type == "integration":
            return run_integration_tests()
        elif test_type == "all":
            return run_all_tests()
        else:
            print(f"Unknown test type: {test_type}")
            print("Usage: python run_tests.py [unit|integration|all]")
            return 1
    else:
        # Run all tests by default
        return run_all_tests()


if __name__ == "__main__":
    exit_code = main()
    
    print("\n" + "="*70)
    if exit_code == 0:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("="*70 + "\n")
    
    sys.exit(exit_code)

# Made with Bob
