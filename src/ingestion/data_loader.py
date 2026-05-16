"""
Data Loader Module
Safely loads data from various formats and creates working copies.
"""

import shutil
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd
from src.ingestion.file_detector import FileDetector
from src.utils.logger import get_logger
from src.utils.config_loader import get_config, get_processed_data_dir

logger = get_logger("ingestion.data_loader")


class DataLoader:
    """Loads data and creates safe working copies."""
    
    def __init__(self):
        self.logger = logger
        self.detector = FileDetector()
        self.config = get_config()
    
    def load_data(self, file_path: str, dataset_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Load data from file and create working copy.
        
        Args:
            file_path: Path to source file
            dataset_name: Optional name for dataset (defaults to filename)
            
        Returns:
            Dictionary with loaded data and metadata
        """
        self.logger.info(f"Loading data from: {file_path}")
        
        # Detect file format
        file_info = self.detector.detect_file_format(file_path)
        
        if not file_info.get('supported', False):
            raise ValueError(f"Unsupported file format: {file_info.get('extension')}")
        
        # Determine dataset name
        if dataset_name is None:
            dataset_name = Path(file_path).stem
        
        # Create working directory
        working_dir = self._create_working_directory(dataset_name)
        
        # Copy original file
        copied_file = self._copy_original_file(file_path, working_dir)
        
        # Load data into DataFrame
        df = self._load_dataframe(copied_file, file_info)
        
        # Generate metadata
        metadata = self._generate_metadata(file_path, copied_file, df, file_info)
        
        # Save metadata
        metadata_path = working_dir / "metadata.json"
        self._save_metadata(metadata, metadata_path)
        
        self.logger.info(f"Data loaded successfully: {len(df)} rows, {len(df.columns)} columns")
        
        return {
            'dataframe': df,
            'metadata': metadata,
            'working_dir': str(working_dir),
            'dataset_name': dataset_name
        }
    
    def _create_working_directory(self, dataset_name: str) -> Path:
        """Create working directory for dataset."""
        processed_dir = get_processed_data_dir()
        working_dir = processed_dir / dataset_name
        working_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.debug(f"Working directory: {working_dir}")
        return working_dir
    
    def _copy_original_file(self, source_path: str, working_dir: Path) -> Path:
        """
        Copy original file to working directory.
        
        Args:
            source_path: Source file path
            working_dir: Working directory
            
        Returns:
            Path to copied file
        """
        source = Path(source_path)
        destination = working_dir / f"raw_copy{source.suffix}"
        
        # Copy file
        shutil.copy2(source, destination)
        
        # Verify copy
        if not destination.exists():
            raise IOError(f"Failed to copy file to {destination}")
        
        # Verify file integrity
        source_hash = self._calculate_file_hash(source)
        dest_hash = self._calculate_file_hash(destination)
        
        if source_hash != dest_hash:
            raise IOError("File copy integrity check failed")
        
        self.logger.info(f"File copied successfully to: {destination}")
        return destination
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _load_dataframe(self, file_path: Path, file_info: Dict[str, Any]) -> pd.DataFrame:
        """
        Load data into pandas DataFrame with robust encoding handling.
        
        Args:
            file_path: Path to file
            file_info: File information from detector
            
        Returns:
            Loaded DataFrame
        """
        format_type = file_info.get('format_type')
        
        try:
            if format_type == 'csv':
                # Try multiple encodings in order of preference
                detected_encoding = file_info.get('encoding', 'utf-8')
                encodings_to_try = [
                    detected_encoding,
                    'utf-8',
                    'latin-1',
                    'iso-8859-1',
                    'cp1252',
                    'utf-16'
                ]
                
                # Remove duplicates while preserving order
                encodings_to_try = list(dict.fromkeys(encodings_to_try))
                
                last_error = None
                for encoding in encodings_to_try:
                    try:
                        self.logger.debug(f"Attempting to read CSV with encoding: {encoding}")
                        df = pd.read_csv(
                            file_path,
                            encoding=encoding,
                            delimiter=file_info.get('delimiter', ','),
                            encoding_errors='strict'
                        )
                        self.logger.info(f"Successfully loaded CSV with encoding: {encoding}")
                        return df
                    except (UnicodeDecodeError, UnicodeError) as e:
                        last_error = e
                        self.logger.debug(f"Failed with encoding {encoding}: {e}")
                        continue
                
                # If all encodings fail, raise the last error
                if last_error:
                    raise last_error
                    
            elif format_type == 'excel':
                # Load first sheet by default
                sheet_name = file_info.get('default_sheet', 0)
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            elif format_type == 'json':
                # Try multiple encodings for JSON as well
                detected_encoding = file_info.get('encoding', 'utf-8')
                encodings_to_try = [detected_encoding, 'utf-8', 'latin-1', 'iso-8859-1']
                encodings_to_try = list(dict.fromkeys(encodings_to_try))
                
                last_error = None
                for encoding in encodings_to_try:
                    try:
                        df = pd.read_json(file_path, encoding=encoding)
                        self.logger.info(f"Successfully loaded JSON with encoding: {encoding}")
                        return df
                    except (UnicodeDecodeError, UnicodeError) as e:
                        last_error = e
                        continue
                
                if last_error:
                    raise last_error
                    
            elif format_type == 'parquet':
                df = pd.read_parquet(file_path)
            else:
                raise ValueError(f"Unsupported format type: {format_type}")
            
            self.logger.debug(f"DataFrame loaded: {df.shape}")
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading DataFrame: {e}")
            raise
    
    def _generate_metadata(
        self,
        source_path: str,
        copied_path: Path,
        df: pd.DataFrame,
        file_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive metadata."""
        metadata = {
            'source': {
                'original_path': str(Path(source_path).absolute()),
                'original_name': Path(source_path).name,
                'original_size_mb': file_info.get('size_mb', 0),
                'file_hash': self._calculate_file_hash(Path(source_path))
            },
            'working_copy': {
                'path': str(copied_path),
                'created_at': datetime.now().isoformat()
            },
            'format': {
                'type': file_info.get('format_type'),
                'extension': file_info.get('extension'),
                'encoding': file_info.get('encoding'),
                'delimiter': file_info.get('delimiter')
            },
            'data': {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': list(df.columns),
                'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
                'memory_usage_mb': round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
            },
            'quality': {
                'missing_values': df.isnull().sum().to_dict(),
                'duplicate_rows': int(df.duplicated().sum()),
                'total_cells': df.size,
                'missing_cells': int(df.isnull().sum().sum())
            },
            'timestamps': {
                'loaded_at': datetime.now().isoformat()
            }
        }
        
        return metadata
    
    def _save_metadata(self, metadata: Dict[str, Any], metadata_path: Path):
        """Save metadata to JSON file."""
        try:
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, default=str)
            self.logger.debug(f"Metadata saved to: {metadata_path}")
        except Exception as e:
            self.logger.error(f"Error saving metadata: {e}")
    
    def load_multiple_files(self, directory_path: str) -> Dict[str, Dict[str, Any]]:
        """
        Load all supported files from a directory.
        
        Args:
            directory_path: Path to directory
            
        Returns:
            Dictionary mapping dataset names to loaded data
        """
        self.logger.info(f"Loading multiple files from: {directory_path}")
        
        # Detect all files
        files = self.detector.detect_directory(directory_path)
        
        loaded_datasets = {}
        for file_info in files:
            try:
                dataset_name = Path(file_info['name']).stem
                result = self.load_data(file_info['path'], dataset_name)
                loaded_datasets[dataset_name] = result
            except Exception as e:
                self.logger.error(f"Error loading {file_info['name']}: {e}")
        
        self.logger.info(f"Loaded {len(loaded_datasets)} datasets")
        return loaded_datasets
    
    def save_dataframe(self, df: pd.DataFrame, output_path: str, format_type: str = 'csv'):
        """
        Save DataFrame to file.
        
        Args:
            df: DataFrame to save
            output_path: Output file path
            format_type: Output format (csv, excel, json, parquet)
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if format_type == 'csv':
                df.to_csv(output_file, index=False)
            elif format_type == 'excel':
                df.to_excel(output_file, index=False)
            elif format_type == 'json':
                df.to_json(output_file, orient='records', indent=2)
            elif format_type == 'parquet':
                df.to_parquet(output_file, index=False)
            else:
                raise ValueError(f"Unsupported output format: {format_type}")
            
            self.logger.info(f"DataFrame saved to: {output_file}")
        except Exception as e:
            self.logger.error(f"Error saving DataFrame: {e}")
            raise


# Example usage
if __name__ == "__main__":
    loader = DataLoader()
    
    # Test loading a single file
    try:
        result = loader.load_data("data/layoffs/layoffs.csv", "layoffs")
        print(f"\nLoaded dataset: {result['dataset_name']}")
        print(f"Shape: {result['dataframe'].shape}")
        print(f"Working directory: {result['working_dir']}")
        print("\nFirst few rows:")
        print(result['dataframe'].head())
    except Exception as e:
        print(f"Error: {e}")

# Made with Bob
