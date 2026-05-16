"""
Unit tests for the profiling module.
"""
import pytest
import pandas as pd
import numpy as np
from src.profiling.profiler import DataProfiler
from src.profiling.quality_checker import QualityChecker


class TestDataProfiler:
    """Tests for DataProfiler class."""
    
    def test_profile_basic_dataframe(self, sample_dataframe):
        """Test basic profiling of a DataFrame."""
        profiler = DataProfiler()
        profile = profiler.profile_dataframe(sample_dataframe, "test_dataset")
        
        assert 'overview' in profile
        assert 'columns' in profile
        assert profile['overview']['total_rows'] == 100
        assert profile['overview']['total_columns'] == 5
    
    def test_profile_column_types(self, sample_dataframe):
        """Test column type detection."""
        profiler = DataProfiler()
        profile = profiler.profile_dataframe(sample_dataframe)
        
        columns = profile['columns']
        assert 'numeric_col' in columns
        assert 'categorical_col' in columns
    
    def test_profile_missing_values(self, sample_dataframe):
        """Test missing value detection."""
        profiler = DataProfiler()
        profile = profiler.profile_dataframe(sample_dataframe)
        
        missing_info = profile['missing_values']
        assert 'missing_col' in missing_info
        assert missing_info['missing_col']['count'] == 20
    
    def test_profile_statistics(self, sample_dataframe):
        """Test statistical calculations."""
        profiler = DataProfiler()
        profile = profiler.profile_dataframe(sample_dataframe)
        
        numeric_col = profile['columns']['numeric_col']
        assert 'mean' in numeric_col or 'statistics' in numeric_col
    
    def test_profile_unique_values(self, sample_dataframe):
        """Test unique value counting."""
        profiler = DataProfiler()
        profile = profiler.profile_dataframe(sample_dataframe)
        
        categorical_col = profile['columns']['categorical_col']
        assert 'unique_count' in categorical_col or 'unique' in categorical_col


class TestQualityChecker:
    """Tests for QualityChecker class."""
    
    def test_check_quality_basic(self, sample_dataframe):
        """Test basic quality checking."""
        checker = QualityChecker()
        report = checker.check_quality(sample_dataframe)
        
        assert 'overall_score' in report
        assert 'issues' in report
        assert 'summary' in report
        assert 0 <= report['overall_score'] <= 100
    
    def test_detect_missing_values(self, sample_dataframe_with_issues):
        """Test missing value detection."""
        checker = QualityChecker()
        report = checker.check_quality(sample_dataframe_with_issues)
        
        issues = report['issues']
        missing_issues = [i for i in issues if i['type'] == 'missing_values']
        assert len(missing_issues) > 0
    
    def test_detect_duplicates(self, sample_dataframe_with_issues):
        """Test duplicate detection."""
        checker = QualityChecker()
        report = checker.check_quality(sample_dataframe_with_issues)
        
        issues = report['issues']
        duplicate_issues = [i for i in issues if i['type'] == 'duplicates']
        assert len(duplicate_issues) > 0
    
    def test_detect_outliers(self, sample_dataframe):
        """Test outlier detection."""
        checker = QualityChecker()
        report = checker.check_quality(sample_dataframe)
        
        issues = report['issues']
        outlier_issues = [i for i in issues if i['type'] == 'outliers']
        # Should detect outlier in outlier_col
        assert len(outlier_issues) > 0
    
    def test_quality_score_calculation(self, sample_dataframe):
        """Test quality score calculation."""
        checker = QualityChecker()
        report = checker.check_quality(sample_dataframe)
        
        score = report['overall_score']
        assert isinstance(score, (int, float))
        assert 0 <= score <= 100
    
    def test_issue_severity_levels(self, sample_dataframe_with_issues):
        """Test issue severity classification."""
        checker = QualityChecker()
        report = checker.check_quality(sample_dataframe_with_issues)
        
        issues = report['issues']
        for issue in issues:
            assert 'severity' in issue
            assert issue['severity'] in ['critical', 'warning', 'info']
    
    def test_empty_dataframe(self):
        """Test quality check on empty DataFrame."""
        checker = QualityChecker()
        df = pd.DataFrame()
        report = checker.check_quality(df)
        
        assert report['overall_score'] == 0
        assert len(report['issues']) > 0
    
    def test_perfect_quality_dataframe(self):
        """Test quality check on perfect DataFrame."""
        checker = QualityChecker()
        df = pd.DataFrame({
            'col1': [1, 2, 3, 4, 5],
            'col2': ['a', 'b', 'c', 'd', 'e'],
            'col3': [10.0, 20.0, 30.0, 40.0, 50.0]
        })
        report = checker.check_quality(df)
        
        # Should have high quality score
        assert report['overall_score'] >= 80

# Made with Bob
