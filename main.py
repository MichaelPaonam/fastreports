"""
FastReports - Main Entry Point
Automated Data Analysis Pipeline with IBM Bob Integration
"""

import sys
import argparse
from pathlib import Path
from src.utils.logger import get_logger
from src.orchestration.pipeline import DataAnalysisPipeline
from src.bob_integration.session_manager import get_bob_session_manager

logger = get_logger("main")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="FastReports - Automated Data Analysis Pipeline"
    )
    parser.add_argument(
        "data_path",
        nargs="?",
        default="data/layoffs/layoffs.csv",
        help="Path to the data file"
    )
    parser.add_argument(
        "--dataset-name",
        default="layoffs",
        help="Name of the dataset"
    )
    parser.add_argument(
        "--auto-clean",
        action="store_true",
        help="Automatically apply cleaning strategies"
    )
    parser.add_argument(
        "--no-viz",
        action="store_true",
        help="Skip visualization generation"
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 80)
    logger.info("FastReports - Automated Data Analysis Pipeline")
    logger.info("IBM Bob Integration Demonstration")
    logger.info("=" * 80)
    
    try:
        # Initialize Bob session
        bob_session = get_bob_session_manager()
        bob_session.start_session(
            args.dataset_name,
            "Complete data analysis pipeline execution"
        )
        
        # Log Bob interaction for pipeline planning
        bob_session.log_interaction(
            mode="Plan Mode",
            phase="initialization",
            prompt="Plan the complete data analysis pipeline execution",
            response="Pipeline phases: Ingestion → Profiling → Quality Check → Cleaning → Analysis → Visualization → Reporting",
            success=True,
            metadata={"dataset": args.dataset_name}
        )
        
        # Initialize and run pipeline
        pipeline = DataAnalysisPipeline()
        
        results = pipeline.run_pipeline(
            data_path=args.data_path,
            dataset_name=args.dataset_name,
            auto_clean=args.auto_clean,
            generate_visualizations=not args.no_viz
        )
        
        # Log Bob interactions for each phase
        for phase in pipeline.state['completed_phases']:
            bob_session.log_interaction(
                mode="Code Mode",
                phase=phase,
                prompt=f"Execute {phase} phase",
                response=f"{phase} completed successfully",
                success=True
            )
        
        # Print pipeline summary
        print("\n")
        print(pipeline.get_pipeline_summary())
        
        # Print Bob session summary
        print("\n")
        session_summary = bob_session.end_session()
        print(bob_session.get_session_summary())
        
        # Print key results
        print("\n")
        print("=" * 80)
        print("KEY RESULTS")
        print("=" * 80)
        
        if 'quality' in results:
            quality_score = results['quality'].get('quality_score', 0)
            print(f"Data Quality Score: {quality_score}/100")
        
        if 'eda' in results:
            findings = results['eda'].get('key_findings', [])
            print(f"\nKey Findings ({len(findings)}):")
            for i, finding in enumerate(findings[:5], 1):
                print(f"  {i}. {finding}")
        
        if 'visualizations' in results and not results['visualizations'].get('skipped'):
            viz_summary = results['visualizations'].get('summary', {})
            print(f"\nVisualizations Generated: {viz_summary.get('total_charts', 0)}")

        if results.get('report_path'):
            print(f"\nHTML Report: {results['report_path']}")
        
        print("\n" + "=" * 80)
        print("Pipeline execution completed successfully!")
        print("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}", exc_info=True)
        
        # Log failure with Bob
        if 'bob_session' in locals():
            bob_session.log_interaction(
                mode="Error",
                phase="execution",
                prompt="Pipeline execution",
                response=str(e),
                success=False
            )
            bob_session.end_session()
        
        return 1


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
