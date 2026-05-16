"""
FastReports Logging Infrastructure
Centralized logging configuration with file rotation and structured output.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime
from typing import Optional


class FastReportsLogger:
    """Centralized logger for FastReports application."""
    
    _instance: Optional['FastReportsLogger'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._setup_logging()
            FastReportsLogger._initialized = True
    
    def _setup_logging(self):
        """Setup logging configuration."""
        # Create logs directory if it doesn't exist
        log_dir = Path("output/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"fastreports_{timestamp}.log"
        
        # Configure root logger
        self.logger = logging.getLogger("fastreports")
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Console handler (INFO and above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        # File handler with rotation (DEBUG and above)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10485760,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        self.logger.info("=" * 80)
        self.logger.info("FastReports Logger Initialized")
        self.logger.info(f"Log file: {log_file}")
        self.logger.info("=" * 80)
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a logger instance for a specific module.
        
        Args:
            name: Name of the module (e.g., 'ingestion', 'profiling')
            
        Returns:
            Logger instance
        """
        return logging.getLogger(f"fastreports.{name}")


def get_logger(name: str) -> logging.Logger:
    """
    Convenience function to get a logger instance.
    
    Args:
        name: Name of the module
        
    Returns:
        Logger instance
    """
    logger_manager = FastReportsLogger()
    return logger_manager.get_logger(name)


def log_phase_start(logger: logging.Logger, phase_name: str):
    """Log the start of a pipeline phase."""
    logger.info("=" * 80)
    logger.info(f"PHASE START: {phase_name}")
    logger.info("=" * 80)


def log_phase_end(logger: logging.Logger, phase_name: str, success: bool = True):
    """Log the end of a pipeline phase."""
    status = "SUCCESS" if success else "FAILED"
    logger.info("=" * 80)
    logger.info(f"PHASE END: {phase_name} - {status}")
    logger.info("=" * 80)


def log_checkpoint(logger: logging.Logger, checkpoint_name: str, data: dict):
    """Log checkpoint information."""
    logger.info("-" * 80)
    logger.info(f"CHECKPOINT: {checkpoint_name}")
    for key, value in data.items():
        logger.info(f"  {key}: {value}")
    logger.info("-" * 80)


def log_data_operation(logger: logging.Logger, operation: str, details: dict):
    """Log data operations with details."""
    logger.debug(f"Data Operation: {operation}")
    for key, value in details.items():
        logger.debug(f"  {key}: {value}")


def log_error_with_context(logger: logging.Logger, error: Exception, context: dict):
    """Log errors with contextual information."""
    logger.error(f"Error occurred: {type(error).__name__}: {str(error)}")
    logger.error("Context:")
    for key, value in context.items():
        logger.error(f"  {key}: {value}")
    logger.exception("Full traceback:")


# Example usage
if __name__ == "__main__":
    # Test the logger
    logger = get_logger("test")
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    log_phase_start(logger, "Test Phase")
    log_checkpoint(logger, "Test Checkpoint", {
        "rows_processed": 1000,
        "errors_found": 5,
        "status": "ready"
    })
    log_phase_end(logger, "Test Phase", success=True)

# Made with Bob
