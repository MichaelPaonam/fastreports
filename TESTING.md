# FastReports Testing Guide

## Overview

This document describes the testing strategy and implementation for the FastReports project.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_ingestion.py        # Unit tests for data ingestion
├── test_profiling.py        # Unit tests for data profiling
├── test_cleaning.py         # Unit tests for data cleaning
├── test_integration.py      # Integration tests for full pipeline
└── __init__.py
```

## Test Categories

### 1. Unit Tests

Unit tests verify individual components in isolation:

- **test_ingestion.py**: Tests for file detection and data loading
- **test_profiling.py**: Tests for data profiling and quality checking
- **test_cleaning.py**: Tests for data cleaning and transformation

### 2. Integration Tests

Integration tests verify the complete pipeline:

- **test_integration.py**: End-to-end pipeline tests with various datasets

## Running Tests

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
# Using pytest directly
pytest tests/ -v

# Using the test runner script
python run_tests.py all
```

### Run Specific Test Categories

```bash
# Unit tests only
python run_tests.py unit

# Integration tests only
python run_tests.py integration

# Specific test file
pytest tests/test_ingestion.py -v

# Specific test class
pytest tests/test_ingestion.py::TestFileDetector -v

# Specific test function
pytest tests/test_ingestion.py::TestFileDetector::test_detect_csv_format -v
```

### Run with Coverage

```bash
pytest tests/ --cov=src --cov-report=html --cov-report=term
```

## Test Fixtures

### Shared Fixtures (conftest.py)

- **temp_dir**: Temporary directory for test files
- **sample_csv_file**: Sample CSV file with clean data
- **sample_excel_file**: Sample Excel file with clean data
- **sample_dataframe**: Sample DataFrame for testing
- **sample_dataframe_with_issues**: DataFrame with quality issues
- **mock_config**: Mock configuration dictionary
- **mock_bob_session**: Mock Bob session for testing

## Test Coverage

### Current Coverage Areas

1. **Data Ingestion** (test_ingestion.py)
   - File format detection (CSV, Excel, unknown)
   - Data loading from various formats
   - Metadata generation
   - Error handling for missing files
   - Data integrity verification

2. **Data Profiling** (test_profiling.py)
   - Basic DataFrame profiling
   - Column type detection
   - Missing value detection
   - Statistical calculations
   - Unique value counting
   - Quality checking
   - Issue detection (missing, duplicates, outliers)
   - Quality score calculation
   - Severity classification

3. **Data Cleaning** (test_cleaning.py)
   - Strategy generation for various issues
   - Missing value imputation (mean, median, mode)
   - Duplicate removal
   - Outlier handling (cap, remove)
   - Date standardization
   - String normalization
   - Data validation

4. **Integration** (test_integration.py)
   - Full pipeline with CSV files
   - Full pipeline with Excel files
   - Pipeline with quality issues
   - Error handling
   - State persistence
   - Bob session integration
   - End-to-end scenarios (layoffs, soccer, survey)
   - Performance tests

## Writing New Tests

### Test Naming Convention

- Test files: `test_<module_name>.py`
- Test classes: `Test<ClassName>`
- Test functions: `test_<functionality>`

### Example Test

```python
def test_example_functionality(sample_dataframe):
    """Test description."""
    # Arrange
    component = MyComponent()
    
    # Act
    result = component.process(sample_dataframe)
    
    # Assert
    assert result is not None
    assert len(result) > 0
```

### Using Fixtures

```python
def test_with_fixture(sample_csv_file, temp_dir):
    """Test using fixtures."""
    loader = DataLoader()
    df, metadata = loader.load_data(sample_csv_file)
    
    assert df is not None
    assert metadata['format'] == 'csv'
```

## Test Markers

Tests can be marked for selective execution:

```python
@pytest.mark.unit
def test_unit_functionality():
    """Unit test."""
    pass

@pytest.mark.integration
def test_integration_scenario():
    """Integration test."""
    pass

@pytest.mark.slow
def test_slow_operation():
    """Slow test."""
    pass
```

Run marked tests:

```bash
pytest -m unit          # Run only unit tests
pytest -m integration   # Run only integration tests
pytest -m "not slow"    # Skip slow tests
```

## Continuous Integration

### GitHub Actions (Example)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest tests/ -v --cov=src
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure `src/` is in Python path
   - Check that `__init__.py` files exist

2. **Fixture Not Found**
   - Verify fixture is defined in `conftest.py`
   - Check fixture scope (function, class, module, session)

3. **Test Failures**
   - Check test data and expectations
   - Verify module implementations match test assumptions
   - Review error messages and stack traces

### Debug Mode

Run tests with verbose output and no capture:

```bash
pytest tests/ -vv -s
```

## Best Practices

1. **Test Independence**: Each test should be independent and not rely on others
2. **Clear Assertions**: Use descriptive assertion messages
3. **Arrange-Act-Assert**: Follow the AAA pattern
4. **Mock External Dependencies**: Use mocks for external services
5. **Test Edge Cases**: Include tests for boundary conditions
6. **Keep Tests Fast**: Unit tests should run quickly
7. **Meaningful Names**: Use descriptive test names
8. **Documentation**: Add docstrings to test functions

## Performance Benchmarks

Expected test execution times:

- Unit tests: < 5 seconds total
- Integration tests: < 30 seconds total
- Full test suite: < 1 minute

## Future Enhancements

- [ ] Add performance benchmarking tests
- [ ] Implement mutation testing
- [ ] Add property-based testing with Hypothesis
- [ ] Create visual regression tests for charts
- [ ] Add load testing for large datasets
- [ ] Implement contract testing for Bob integration

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)

---

**Last Updated**: 2024-05-16