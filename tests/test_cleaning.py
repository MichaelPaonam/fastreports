"""
Unit tests for the cleaning module.
"""
import pytest
import pandas as pd
import numpy as np
from src.cleaning.strategy_generator import StrategyGenerator
from src.cleaning.transformers import DataTransformer
from src.cleaning.validator import DataValidator


class TestStrategyGenerator:
    """Tests for StrategyGenerator class."""
    
    def test_generate_strategies_for_missing_values(self, sample_dataframe_with_issues):
        """Test strategy generation for missing values."""
        generator = StrategyGenerator()
        quality_report = {
            'issues': [
                {
                    'type': 'missing_values',
                    'column': 'value',
                    'severity': 'warning',
                    'details': {'missing_count': 1, 'missing_percentage': 16.67}
                }
            ]
        }
        
        strategies = generator.generate_strategies(sample_dataframe_with_issues, quality_report)
        
        assert len(strategies) > 0
        assert any(s['type'] == 'handle_missing' for s in strategies)
    
    def test_generate_strategies_for_outliers(self):
        """Test strategy generation for outliers."""
        generator = StrategyGenerator()
        df = pd.DataFrame({'value': [1, 2, 3, 4, 1000]})
        quality_report = {
            'issues': [
                {
                    'type': 'outliers',
                    'column': 'value',
                    'severity': 'warning',
                    'details': {'outlier_count': 1}
                }
            ]
        }
        
        strategies = generator.generate_strategies(df, quality_report)
        
        assert len(strategies) > 0
        assert any(s['type'] == 'handle_outliers' for s in strategies)
    
    def test_generate_strategies_for_duplicates(self, sample_dataframe_with_issues):
        """Test strategy generation for duplicates."""
        generator = StrategyGenerator()
        quality_report = {
            'issues': [
                {
                    'type': 'duplicates',
                    'severity': 'warning',
                    'details': {'duplicate_count': 1}
                }
            ]
        }
        
        strategies = generator.generate_strategies(sample_dataframe_with_issues, quality_report)
        
        assert len(strategies) > 0
        assert any(s['type'] == 'remove_duplicates' for s in strategies)


class TestDataTransformer:
    """Tests for DataTransformer class."""
    
    def test_handle_missing_values_mean(self):
        """Test missing value imputation with mean."""
        transformer = DataTransformer()
        df = pd.DataFrame({'value': [1.0, 2.0, np.nan, 4.0, 5.0]})
        
        result = transformer.handle_missing_values(df, 'value', method='mean')
        
        assert result['value'].isna().sum() == 0
        assert result['value'].iloc[2] == 3.0  # Mean of 1,2,4,5
    
    def test_handle_missing_values_median(self):
        """Test missing value imputation with median."""
        transformer = DataTransformer()
        df = pd.DataFrame({'value': [1.0, 2.0, np.nan, 4.0, 5.0]})
        
        result = transformer.handle_missing_values(df, 'value', method='median')
        
        assert result['value'].isna().sum() == 0
        assert result['value'].iloc[2] == 3.0  # Median of 1,2,4,5
    
    def test_handle_missing_values_mode(self):
        """Test missing value imputation with mode."""
        transformer = DataTransformer()
        df = pd.DataFrame({'category': ['A', 'B', None, 'A', 'B', 'A']})
        
        result = transformer.handle_missing_values(df, 'category', method='mode')
        
        assert result['category'].isna().sum() == 0
        assert result['category'].iloc[2] == 'A'  # Mode
    
    def test_remove_duplicates(self):
        """Test duplicate removal."""
        transformer = DataTransformer()
        df = pd.DataFrame({
            'id': [1, 2, 3, 2, 4],
            'value': ['a', 'b', 'c', 'b', 'd']
        })
        
        result = transformer.remove_duplicates(df)
        
        assert len(result) == 4
        assert result['id'].tolist() == [1, 2, 3, 4]
    
    def test_handle_outliers_cap(self):
        """Test outlier handling with capping."""
        transformer = DataTransformer()
        df = pd.DataFrame({'value': [1, 2, 3, 4, 1000]})
        
        result = transformer.handle_outliers(df, 'value', method='cap')
        
        assert result['value'].max() < 1000
        assert len(result) == 5  # No rows removed
    
    def test_handle_outliers_remove(self):
        """Test outlier handling with removal."""
        transformer = DataTransformer()
        df = pd.DataFrame({'value': [1, 2, 3, 4, 1000]})
        
        result = transformer.handle_outliers(df, 'value', method='remove')
        
        assert len(result) < 5  # Outlier row removed
        assert 1000 not in result['value'].values
    
    def test_standardize_dates(self):
        """Test date standardization."""
        transformer = DataTransformer()
        df = pd.DataFrame({
            'date': ['2024-01-01', '01/02/2024', '2024-03-01']
        })
        
        result = transformer.standardize_dates(df, 'date')
        
        assert pd.api.types.is_datetime64_any_dtype(result['date'])
    
    def test_normalize_strings(self):
        """Test string normalization."""
        transformer = DataTransformer()
        df = pd.DataFrame({
            'text': ['  Hello  ', 'WORLD', 'Test  123']
        })
        
        result = transformer.normalize_strings(df, 'text')
        
        assert result['text'].iloc[0] == 'hello'
        assert result['text'].iloc[1] == 'world'
        assert result['text'].iloc[2] == 'test 123'


class TestDataValidator:
    """Tests for DataValidator class."""
    
    def test_validate_row_count(self):
        """Test row count validation."""
        validator = DataValidator()
        original = pd.DataFrame({'a': [1, 2, 3]})
        cleaned = pd.DataFrame({'a': [1, 2, 3]})
        
        result = validator.validate(original, cleaned)
        
        assert result['valid'] is True
        assert 'row_count' in result['checks']
    
    def test_validate_column_preservation(self):
        """Test column preservation validation."""
        validator = DataValidator()
        original = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        cleaned = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        
        result = validator.validate(original, cleaned)
        
        assert result['valid'] is True
        assert result['checks']['columns_preserved'] is True
    
    def test_validate_missing_column(self):
        """Test validation fails when column is missing."""
        validator = DataValidator()
        original = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        cleaned = pd.DataFrame({'a': [1, 2, 3]})
        
        result = validator.validate(original, cleaned)
        
        assert result['valid'] is False
        assert result['checks']['columns_preserved'] is False
    
    def test_validate_data_types(self):
        """Test data type validation."""
        validator = DataValidator()
        original = pd.DataFrame({'a': [1, 2, 3]})
        cleaned = pd.DataFrame({'a': [1, 2, 3]})
        
        result = validator.validate(original, cleaned)
        
        assert 'data_types' in result['checks']

# Made with Bob
