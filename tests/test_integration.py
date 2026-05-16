"""
Integration tests for the FastReports pipeline.
"""
import os
import pytest
import pandas as pd
from src.orchestration.pipeline import DataAnalysisPipeline
from src.bob_integration.session_manager import BobSessionManager


class TestPipelineIntegration:
    """Integration tests for the complete pipeline."""
    
    def test_full_pipeline_csv(self, sample_csv_file, temp_dir):
        """Test complete pipeline with CSV file."""
        # Initialize pipeline
        pipeline = DataAnalysisPipeline()
        
        # Run pipeline
        results = pipeline.run_pipeline(
            data_path=sample_csv_file,
            dataset_name='test_csv',
            auto_clean=True,
            generate_visualizations=False
        )
        
        # Verify results
        assert results is not None
        assert 'ingestion' in results
        assert 'profiling' in results
        assert results['ingestion']['success'] is True
        assert results['profiling']['success'] is True
    
    def test_full_pipeline_excel(self, sample_excel_file, temp_dir):
        """Test complete pipeline with Excel file."""
        pipeline = DataAnalysisPipeline()
        
        results = pipeline.run_pipeline(
            data_path=sample_excel_file,
            dataset_name='test_excel',
            auto_clean=True,
            generate_visualizations=False
        )
        
        assert results is not None
        assert results['ingestion']['success'] is True
        assert results['profiling']['success'] is True
    
    def test_pipeline_with_quality_issues(self, sample_dataframe_with_issues, temp_dir):
        """Test pipeline with data quality issues."""
        # Save DataFrame to CSV
        file_path = os.path.join(temp_dir, 'issues.csv')
        sample_dataframe_with_issues.to_csv(file_path, index=False)
        
        pipeline = DataAnalysisPipeline()
        results = pipeline.run_pipeline(
            data_path=file_path,
            dataset_name='test_issues',
            auto_clean=True,
            generate_visualizations=False
        )
        
        # Should detect quality issues
        assert results['profiling']['success'] is True
        quality_report = results.get('quality', {}).get('report', {})
        assert 'issues' in quality_report or 'overall_score' in quality_report
    
    def test_pipeline_error_handling(self, temp_dir):
        """Test pipeline error handling with invalid file."""
        pipeline = DataAnalysisPipeline()
        
        with pytest.raises(Exception):
            pipeline.run_pipeline(
                data_path='nonexistent.csv',
                dataset_name='test_error',
                auto_clean=False,
                generate_visualizations=False
            )
    
    def test_pipeline_state_persistence(self, sample_csv_file, temp_dir):
        """Test that pipeline maintains state across phases."""
        pipeline = DataAnalysisPipeline()
        
        results = pipeline.run_pipeline(
            data_path=sample_csv_file,
            dataset_name='test_state',
            auto_clean=True,
            generate_visualizations=False
        )
        
        # Verify data flows through phases
        assert 'ingestion' in results
        assert 'profiling' in results
        assert pipeline.state['completed_phases'] is not None


class TestEndToEndScenarios:
    """End-to-end scenario tests."""
    
    def test_layoffs_dataset_scenario(self, temp_dir):
        """Test with layoffs-like dataset."""
        # Create sample layoffs data
        df = pd.DataFrame({
            'company': ['TechCorp', 'DataInc', 'AILabs', 'CloudCo', 'DevOps'],
            'total_laid_off': [100, 50, 200, 75, 30],
            'percentage_laid_off': [10.0, 5.0, 20.0, 7.5, 3.0],
            'date': pd.date_range('2024-01-01', periods=5),
            'industry': ['Tech', 'Data', 'AI', 'Cloud', 'DevOps'],
            'stage': ['Series B', 'Series A', 'IPO', 'Series C', 'Seed']
        })
        
        file_path = os.path.join(temp_dir, 'layoffs.csv')
        df.to_csv(file_path, index=False)
        
        pipeline = DataAnalysisPipeline()
        results = pipeline.run_pipeline(
            data_path=file_path,
            dataset_name='layoffs',
            auto_clean=True,
            generate_visualizations=False
        )
        
        assert results['ingestion']['success'] is True
    
    def test_soccer_dataset_scenario(self, temp_dir):
        """Test with soccer-like dataset."""
        # Create sample soccer data
        df = pd.DataFrame({
            'team': ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
            'matches_played': [10, 10, 10, 10, 10],
            'wins': [7, 5, 4, 3, 1],
            'draws': [2, 3, 4, 5, 6],
            'losses': [1, 2, 2, 2, 3],
            'goals_for': [25, 20, 18, 15, 10],
            'goals_against': [10, 15, 16, 18, 25],
            'points': [23, 18, 16, 14, 9]
        })
        
        file_path = os.path.join(temp_dir, 'soccer.csv')
        df.to_csv(file_path, index=False)
        
        pipeline = DataAnalysisPipeline()
        results = pipeline.run_pipeline(
            data_path=file_path,
            dataset_name='soccer',
            auto_clean=True,
            generate_visualizations=False
        )
        
        assert results['ingestion']['success'] is True


class TestPipelinePerformance:
    """Performance tests for the pipeline."""
    
    def test_large_dataset_performance(self, temp_dir):
        """Test pipeline performance with larger dataset."""
        # Create larger dataset
        df = pd.DataFrame({
            'id': range(1000),
            'value1': [i * 2 for i in range(1000)],
            'value2': [i * 3 for i in range(1000)],
            'category': [f'Cat{i % 10}' for i in range(1000)]
        })
        
        file_path = os.path.join(temp_dir, 'large.csv')
        df.to_csv(file_path, index=False)
        
        import time
        start_time = time.time()
        
        pipeline = DataAnalysisPipeline()
        results = pipeline.run_pipeline(
            data_path=file_path,
            dataset_name='large',
            auto_clean=True,
            generate_visualizations=False
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete in reasonable time (< 30 seconds)
        assert execution_time < 30
        assert results['ingestion']['success'] is True

# Made with Bob
