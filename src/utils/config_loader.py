"""
Configuration Loader for FastReports
Loads and provides access to application configuration from config.yaml
"""

import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from src.utils.logger import get_logger

logger = get_logger("config")


class ConfigLoader:
    """Singleton configuration loader."""
    
    _instance: Optional['ConfigLoader'] = None
    _config: Optional[Dict[str, Any]] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self._load_config()
    
    def _load_config(self):
        """Load configuration from config.yaml."""
        config_path = Path("config.yaml")
        
        if not config_path.exists():
            logger.warning(f"Config file not found at {config_path}, using defaults")
            self._config = self._get_default_config()
            return
        
        try:
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self._config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'directories': {
                'data': 'data',
                'processed_data': 'processed_data',
                'output': 'output',
                'reports': 'output/reports',
                'logs': 'output/logs'
            },
            'processing': {
                'chunk_size': 10000,
                'max_file_size_mb': 1000
            },
            'quality': {
                'missing_value_threshold': 0.5,
                'outlier_std_threshold': 3
            },
            'logging': {
                'level': 'INFO'
            }
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to config value (e.g., 'directories.data')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self._config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration dictionary."""
        if self._config is None:
            return {}
        return self._config.copy()
    
    def reload(self):
        """Reload configuration from file."""
        self._config = None
        self._load_config()


def get_config() -> ConfigLoader:
    """Get configuration loader instance."""
    return ConfigLoader()


# Convenience functions for common config values
def get_data_dir() -> Path:
    """Get data directory path."""
    return Path(get_config().get('directories.data', 'data'))


def get_processed_data_dir() -> Path:
    """Get processed data directory path."""
    return Path(get_config().get('directories.processed_data', 'processed_data'))


def get_output_dir() -> Path:
    """Get output directory path."""
    return Path(get_config().get('directories.output', 'output'))


def get_reports_dir() -> Path:
    """Get reports directory path."""
    return Path(get_config().get('directories.reports', 'output/reports'))


def get_logs_dir() -> Path:
    """Get logs directory path."""
    return Path(get_config().get('directories.logs', 'output/logs'))


# Example usage
if __name__ == "__main__":
    config = get_config()
    
    print("Data directory:", config.get('directories.data'))
    print("Chunk size:", config.get('processing.chunk_size'))
    print("Missing value threshold:", config.get('quality.missing_value_threshold'))
    print("Non-existent key:", config.get('non.existent.key', 'default_value'))

# Made with Bob
