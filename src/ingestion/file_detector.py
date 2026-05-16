"""
File Format Detection Module
Auto-detects file formats, delimiters, and encoding for various data files.
"""

import os
import chardet
from pathlib import Path
from typing import Dict, Any, Optional, List
import pandas as pd
from src.utils.logger import get_logger

logger = get_logger("ingestion.file_detector")


class FileDetector:
    """Detects file format and characteristics."""
    
    SUPPORTED_FORMATS = ['.csv', '.xlsx', '.xls', '.json', '.parquet', '.tsv', '.txt']
    
    def __init__(self):
        self.logger = logger
    
    def detect_file_format(self, file_path: str) -> Dict[str, Any]:
        """
        Detect file format and characteristics.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file metadata
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        self.logger.info(f"Detecting format for: {file_path}")
        
        # Get basic file info
        file_info = {
            'path': str(path.absolute()),
            'name': path.name,
            'extension': path.suffix.lower(),
            'size_bytes': path.stat().st_size,
            'size_mb': round(path.stat().st_size / (1024 * 1024), 2)
        }
        
        # Check if format is supported
        if file_info['extension'] not in self.SUPPORTED_FORMATS:
            self.logger.warning(f"Unsupported file format: {file_info['extension']}")
            file_info['supported'] = False
            return file_info
        
        file_info['supported'] = True
        
        # Detect specific characteristics based on format
        if file_info['extension'] in ['.csv', '.tsv', '.txt']:
            file_info.update(self._detect_csv_characteristics(path))
        elif file_info['extension'] in ['.xlsx', '.xls']:
            file_info.update(self._detect_excel_characteristics(path))
        elif file_info['extension'] == '.json':
            file_info.update(self._detect_json_characteristics(path))
        elif file_info['extension'] == '.parquet':
            file_info.update(self._detect_parquet_characteristics(path))
        
        self.logger.info(f"Format detected: {file_info.get('format_type', 'unknown')}")
        return file_info
    
    def _detect_encoding(self, file_path: Path, sample_size: int = 10000) -> str:
        """
        Detect file encoding.
        
        Args:
            file_path: Path to file
            sample_size: Number of bytes to sample
            
        Returns:
            Detected encoding
        """
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(sample_size)
            
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']
            
            self.logger.debug(f"Encoding detected: {encoding} (confidence: {confidence:.2f})")
            
            # Default to utf-8 if confidence is low
            if confidence < 0.7:
                self.logger.warning(f"Low encoding confidence, defaulting to utf-8")
                return 'utf-8'
            
            return encoding or 'utf-8'
        except Exception as e:
            self.logger.error(f"Error detecting encoding: {e}")
            return 'utf-8'
    
    def _detect_csv_delimiter(self, file_path: Path, encoding: str) -> str:
        """
        Detect CSV delimiter.
        
        Args:
            file_path: Path to CSV file
            encoding: File encoding
            
        Returns:
            Detected delimiter
        """
        try:
            # Read first few lines
            with open(file_path, 'r', encoding=encoding) as f:
                sample = ''.join([f.readline() for _ in range(5)])
            
            # Try common delimiters
            delimiters = [',', '\t', ';', '|', ' ']
            delimiter_counts = {}
            
            for delimiter in delimiters:
                count = sample.count(delimiter)
                if count > 0:
                    delimiter_counts[delimiter] = count
            
            if not delimiter_counts:
                return ','
            
            # Return most common delimiter
            detected_delimiter = max(delimiter_counts.items(), key=lambda x: x[1])[0]
            
            # Map tab to readable name
            delimiter_name = 'tab' if detected_delimiter == '\t' else detected_delimiter
            self.logger.debug(f"Delimiter detected: {delimiter_name}")
            
            return detected_delimiter
        except Exception as e:
            self.logger.error(f"Error detecting delimiter: {e}")
            return ','
    
    def _detect_csv_characteristics(self, file_path: Path) -> Dict[str, Any]:
        """Detect CSV file characteristics."""
        encoding = self._detect_encoding(file_path)
        delimiter = self._detect_csv_delimiter(file_path, encoding)
        
        try:
            # Try to read first few rows to get column info
            df_sample = pd.read_csv(
                file_path,
                encoding=encoding,
                delimiter=delimiter,
                nrows=5
            )
            
            return {
                'format_type': 'csv',
                'encoding': encoding,
                'delimiter': delimiter,
                'columns': list(df_sample.columns),
                'column_count': len(df_sample.columns),
                'has_header': True,
                'sample_rows': len(df_sample)
            }
        except Exception as e:
            self.logger.error(f"Error reading CSV sample: {e}")
            return {
                'format_type': 'csv',
                'encoding': encoding,
                'delimiter': delimiter,
                'error': str(e)
            }
    
    def _detect_excel_characteristics(self, file_path: Path) -> Dict[str, Any]:
        """Detect Excel file characteristics."""
        try:
            # Get sheet names
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            
            # Read first sheet sample
            df_sample = pd.read_excel(file_path, sheet_name=sheet_names[0], nrows=5)
            
            return {
                'format_type': 'excel',
                'sheet_names': sheet_names,
                'sheet_count': len(sheet_names),
                'default_sheet': sheet_names[0],
                'columns': list(df_sample.columns),
                'column_count': len(df_sample.columns),
                'sample_rows': len(df_sample)
            }
        except Exception as e:
            self.logger.error(f"Error reading Excel file: {e}")
            return {
                'format_type': 'excel',
                'error': str(e)
            }
    
    def _detect_json_characteristics(self, file_path: Path) -> Dict[str, Any]:
        """Detect JSON file characteristics."""
        encoding = self._detect_encoding(file_path)
        
        try:
            # Try to read as JSON
            with open(file_path, 'r', encoding=encoding) as f:
                import json
                data = json.load(f)
            
            # Determine structure
            if isinstance(data, list):
                structure = 'array'
                record_count = len(data)
                sample = data[0] if data else {}
            elif isinstance(data, dict):
                structure = 'object'
                record_count = 1
                sample = data
            else:
                structure = 'unknown'
                record_count = 0
                sample = {}
            
            return {
                'format_type': 'json',
                'encoding': encoding,
                'structure': structure,
                'record_count': record_count,
                'keys': list(sample.keys()) if isinstance(sample, dict) else []
            }
        except Exception as e:
            self.logger.error(f"Error reading JSON file: {e}")
            return {
                'format_type': 'json',
                'encoding': encoding,
                'error': str(e)
            }
    
    def _detect_parquet_characteristics(self, file_path: Path) -> Dict[str, Any]:
        """Detect Parquet file characteristics."""
        try:
            df_sample = pd.read_parquet(file_path)
            
            return {
                'format_type': 'parquet',
                'columns': list(df_sample.columns),
                'column_count': len(df_sample.columns),
                'row_count': len(df_sample),
                'dtypes': {col: str(dtype) for col, dtype in df_sample.dtypes.items()}
            }
        except Exception as e:
            self.logger.error(f"Error reading Parquet file: {e}")
            return {
                'format_type': 'parquet',
                'error': str(e)
            }
    
    def detect_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """
        Detect all supported files in a directory.
        
        Args:
            directory_path: Path to directory
            
        Returns:
            List of file information dictionaries
        """
        path = Path(directory_path)
        
        if not path.exists() or not path.is_dir():
            raise ValueError(f"Invalid directory: {directory_path}")
        
        self.logger.info(f"Scanning directory: {directory_path}")
        
        detected_files = []
        for file_path in path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                try:
                    file_info = self.detect_file_format(str(file_path))
                    detected_files.append(file_info)
                except Exception as e:
                    self.logger.error(f"Error detecting {file_path}: {e}")
        
        self.logger.info(f"Found {len(detected_files)} supported files")
        return detected_files


# Example usage
if __name__ == "__main__":
    detector = FileDetector()
    
    # Test with layoffs dataset
    try:
        info = detector.detect_file_format("data/layoffs/layoffs.csv")
        print("\nLayoffs CSV Info:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test directory detection
    try:
        files = detector.detect_directory("data")
        print(f"\nFound {len(files)} files in data directory")
    except Exception as e:
        print(f"Error: {e}")

# Made with Bob
