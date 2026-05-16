"""
Unit tests for the ingestion module.
"""
import os
import pytest
import pandas as pd
from src.ingestion.file_detector import FileDetector
from src.ingestion.data_loader import DataLoader


class TestFileDetector:
    """Tests for FileDetector class."""
    
    def test_detect_csv_format(self, sample_csv_file):
        """Test CSV file format detection."""
        detector = FileDetector()
        result = detector.detect_file_format(sample_csv_file)
        
        assert result['extension'] == '.csv'
        assert 'size_bytes' in result
        assert result['size_bytes'] > 0
        assert 'encoding' in result
    
    def test_detect_excel_format(self, sample_excel_file):
        """Test Excel file format detection."""
        detector = FileDetector()
        result = detector.detect_file_format(sample_excel_file)
        
        assert result['extension'] == '.xlsx'
        assert 'size_bytes' in result
        assert result['size_bytes'] > 0
    
    def test_detect_nonexistent_file(self):
        """Test detection of non-existent file."""
        detector = FileDetector()
        
        with pytest.raises(FileNotFoundError):
            detector.detect_file_format('nonexistent.csv')
    
    def test_detect_unsupported_format(self, temp_dir):
        """Test detection of unsupported file format."""
        file_path = os.path.join(temp_dir, 'test.txt')
        with open(file_path, 'w') as f:
            f.write('test content')
        
        detector = FileDetector()
        result = detector.detect_file_format(file_path)
        
        # Should still detect but mark as unsupported
        assert result['extension'] == '.txt'


class TestDataLoader:
    """Tests for DataLoader class."""
    
    def test_load_csv_file(self, sample_csv_file):
        """Test loading CSV file."""
        loader = DataLoader()
        result = loader.load_data(sample_csv_file)
        
        assert 'dataframe' in result
        assert 'metadata' in result
        
        df = result['dataframe']
        metadata = result['metadata']
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert 'name' in df.columns
        assert 'age' in df.columns
        assert metadata['data']['rows'] == 5
        assert metadata['data']['columns'] == 5
    
    def test_load_excel_file(self, sample_excel_file):
        """Test loading Excel file."""
        loader = DataLoader()
        result = loader.load_data(sample_excel_file)
        
        assert 'dataframe' in result
        assert 'metadata' in result
        
        df = result['dataframe']
        metadata = result['metadata']
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert 'product' in df.columns
        assert 'quantity' in df.columns
    
    def test_load_nonexistent_file(self):
        """Test loading non-existent file."""
        loader = DataLoader()
        
        with pytest.raises(FileNotFoundError):
            loader.load_data('nonexistent.csv')
    
    def test_metadata_generation(self, sample_csv_file):
        """Test metadata generation."""
        loader = DataLoader()
        result = loader.load_data(sample_csv_file)
        
        metadata = result['metadata']
        
        assert 'source' in metadata
        assert 'data' in metadata
        assert 'timestamps' in metadata
        assert metadata['data']['rows'] == 5
        assert metadata['data']['columns'] == 5
        assert isinstance(metadata['data']['column_names'], list)
    
    def test_data_integrity(self, sample_csv_file):
        """Test that loaded data matches source."""
        loader = DataLoader()
        result = loader.load_data(sample_csv_file)
        
        df = result['dataframe']
        
        # Load directly with pandas for comparison
        df_direct = pd.read_csv(sample_csv_file)
        
        assert df.shape == df_direct.shape
        assert list(df.columns) == list(df_direct.columns)
        assert df['age'].sum() == df_direct['age'].sum()

# Made with Bob
