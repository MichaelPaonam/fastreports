"""
Pytest configuration and shared fixtures for FastReports tests.
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path
import pytest
import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_csv_file(temp_dir):
    """Create a sample CSV file for testing."""
    file_path = os.path.join(temp_dir, "test_data.csv")
    df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 40, 45],
        'salary': [50000, 60000, 70000, 80000, 90000],
        'department': ['HR', 'IT', 'Finance', 'IT', 'HR']
    })
    df.to_csv(file_path, index=False)
    return file_path


@pytest.fixture
def sample_excel_file(temp_dir):
    """Create a sample Excel file for testing."""
    file_path = os.path.join(temp_dir, "test_data.xlsx")
    df = pd.DataFrame({
        'product': ['A', 'B', 'C', 'D', 'E'],
        'quantity': [10, 20, 30, 40, 50],
        'price': [100.0, 200.0, 300.0, 400.0, 500.0],
        'date': pd.date_range('2024-01-01', periods=5)
    })
    df.to_excel(file_path, index=False)
    return file_path


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'numeric_col': np.random.randn(100),
        'categorical_col': np.random.choice(['A', 'B', 'C'], 100),
        'missing_col': [np.nan if i % 5 == 0 else i for i in range(100)],
        'outlier_col': [1000 if i == 50 else i for i in range(100)],
        'date_col': pd.date_range('2024-01-01', periods=100)
    })


@pytest.fixture
def sample_dataframe_with_issues():
    """Create a DataFrame with various data quality issues."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 5],  # Duplicate
        'value': [10, None, 30, 40, 1000, 50],  # Missing and outlier
        'category': ['A', 'B', 'C', 'D', 'E', 'F'],
        'date': ['2024-01-01', '2024-02-01', 'invalid', '2024-04-01', '2024-05-01', '2024-06-01']
    })


@pytest.fixture
def mock_config():
    """Create a mock configuration dictionary."""
    return {
        'data': {
            'input_dir': 'data/',
            'output_dir': 'output/',
            'processed_dir': 'processed_data/'
        },
        'profiling': {
            'outlier_method': 'iqr',
            'outlier_threshold': 1.5
        },
        'cleaning': {
            'auto_clean': False,
            'missing_threshold': 0.5
        },
        'visualization': {
            'max_charts': 10,
            'chart_height': 400,
            'chart_width': 600
        }
    }


@pytest.fixture
def mock_bob_session():
    """Create a mock Bob session for testing."""
    from src.bob_integration.session_manager import BobSessionManager
    session = BobSessionManager()
    session.start_session("test_session")
    yield session
    # Cleanup
    if hasattr(session, 'session_file') and os.path.exists(session.session_file):
        os.remove(session.session_file)

# Made with Bob
