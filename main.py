"""
FastReports - Main Entry Point
Automated Data Analysis Pipeline with IBM Bob Integration
"""

import sys
from pathlib import Path
from src.utils.logger import get_logger, log_phase_start, log_phase_end
from src.ingestion.data_loader import DataLoader
from src.profiling.profiler import DataProfiler
from src.profiling.quality_checker import QualityChecker

logger = get_logger("main")


def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("FastReports - Automated Data Analysis Pipeline")
    logger.info("=" * 80)
    
    try:
        # Phase 1: Data Ingestion
        log_phase_start(logger, "Data Ingestion")
        
        loader = DataLoader()
        
        # Load layoffs dataset as example
        layoffs_result = loader.load_data("data/layoffs/layoffs.csv", "layoffs")
        df = layoffs_result['dataframe']
        
        logger.info(f"Loaded dataset: {layoffs_result['dataset_name']}")
        logger.info(f"Shape: {df.shape}")
        logger.info(f"Working directory: {layoffs_result['working_dir']}")
        
        log_phase_end(logger, "Data Ingestion", success=True)
        
        # Phase 2: Data Profiling
        log_phase_start(logger, "Data Profiling")
        
        profiler = DataProfiler()
        profile = profiler.profile_dataframe(df, "layoffs")
        
        # Print summary
        summary = profiler.generate_summary_report(profile)
        print(summary)
        logger.info("Profile generated successfully")
        
        log_phase_end(logger, "Data Profiling", success=True)
        
        # Phase 3: Quality Checking
        log_phase_start(logger, "Quality Checking")
        
        checker = QualityChecker()
        quality_result = checker.check_quality(df, "layoffs")
        
        # Print quality report
        quality_report = checker.generate_report(quality_result)
        print(quality_report)
        logger.info(f"Quality score: {quality_result['quality_score']}/100")
        
        log_phase_end(logger, "Quality Checking", success=True)
        
        logger.info("=" * 80)
        logger.info("Pipeline execution completed successfully!")
        logger.info("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
