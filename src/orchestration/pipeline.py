"""
Pipeline Orchestration Module
Coordinates the entire data analysis pipeline
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import pandas as pd
from datetime import datetime
from src.utils.logger import get_logger, log_phase_start, log_phase_end
from src.ingestion.data_loader import DataLoader
from src.profiling.profiler import DataProfiler
from src.profiling.quality_checker import QualityChecker
from src.cleaning.strategy_generator import StrategyGenerator
from src.cleaning.transformers import DataTransformer
from src.cleaning.validator import DataValidator
from src.analysis.statistics import StatisticalAnalyzer
from src.analysis.eda import EDAReportGenerator
from src.visualization.chart_generator import ChartGenerator
from src.visualization.plotly_charts import PlotlyChartBuilder
from src.visualization.recommender import VisualizationRecommender

logger = get_logger(__name__)


class DataAnalysisPipeline:
    """Orchestrates the complete data analysis pipeline."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the pipeline.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.state = {
            'current_phase': None,
            'completed_phases': [],
            'failed_phases': [],
            'start_time': None,
            'end_time': None
        }
        
        # Initialize components
        self.data_loader = DataLoader()
        self.profiler = DataProfiler()
        self.quality_checker = QualityChecker()
        self.strategy_generator = StrategyGenerator()
        self.transformer = DataTransformer()
        self.validator = DataValidator()
        self.statistical_analyzer = StatisticalAnalyzer()
        self.eda_generator = EDAReportGenerator()
        self.chart_generator = ChartGenerator()
        self.plotly_builder = PlotlyChartBuilder()
        self.viz_recommender = VisualizationRecommender()
        
        # Pipeline results
        self.results = {}
    
    def run_pipeline(
        self,
        data_path: str,
        dataset_name: str,
        auto_clean: bool = False,
        generate_visualizations: bool = True
    ) -> Dict[str, Any]:
        """
        Run the complete data analysis pipeline.
        
        Args:
            data_path: Path to the data file
            dataset_name: Name of the dataset
            auto_clean: Whether to automatically apply cleaning strategies
            generate_visualizations: Whether to generate visualizations
        
        Returns:
            Dictionary containing all pipeline results
        """
        logger.info("=" * 80)
        logger.info(f"Starting Data Analysis Pipeline for: {dataset_name}")
        logger.info("=" * 80)
        
        self.state['start_time'] = datetime.now()
        
        try:
            # Phase 1: Data Ingestion
            ingestion_result = self._run_ingestion_phase(data_path, dataset_name)
            df = ingestion_result['dataframe']
            
            # Phase 2: Data Profiling
            profiling_result = self._run_profiling_phase(df, dataset_name)
            
            # Phase 3: Quality Checking
            quality_result = self._run_quality_checking_phase(df, dataset_name)
            
            # Phase 4: Data Cleaning (if auto_clean or user approves)
            if auto_clean or self._should_clean_data(quality_result):
                cleaning_result = self._run_cleaning_phase(
                    df,
                    dataset_name,
                    quality_result
                )
                df = cleaning_result['cleaned_dataframe']
            else:
                cleaning_result = {'skipped': True, 'reason': 'User declined or not needed'}
            
            # Phase 5: Statistical Analysis
            stats_result = self._run_statistical_analysis_phase(df, dataset_name)
            
            # Phase 6: EDA Report Generation
            eda_result = self._run_eda_phase(df, dataset_name)
            
            # Phase 7: Visualization (if enabled)
            if generate_visualizations:
                viz_result = self._run_visualization_phase(df, dataset_name)
            else:
                viz_result = {'skipped': True, 'reason': 'Visualization disabled'}
            
            # Compile final results
            self.results = {
                'dataset_name': dataset_name,
                'ingestion': ingestion_result,
                'profiling': profiling_result,
                'quality': quality_result,
                'cleaning': cleaning_result,
                'statistics': stats_result,
                'eda': eda_result,
                'visualizations': viz_result,
                'pipeline_state': self.state
            }
            
            self.state['end_time'] = datetime.now()
            duration = (self.state['end_time'] - self.state['start_time']).total_seconds()
            
            logger.info("=" * 80)
            logger.info(f"Pipeline completed successfully in {duration:.2f} seconds")
            logger.info(f"Completed phases: {len(self.state['completed_phases'])}")
            logger.info("=" * 80)
            
            return self.results
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            self.state['end_time'] = datetime.now()
            raise
    
    def _run_ingestion_phase(
        self,
        data_path: str,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Run data ingestion phase."""
        log_phase_start(logger, "Data Ingestion")
        self.state['current_phase'] = 'ingestion'
        
        try:
            result = self.data_loader.load_data(data_path, dataset_name)
            
            logger.info(f"Loaded dataset: {dataset_name}")
            logger.info(f"Shape: {result['dataframe'].shape}")
            logger.info(f"Working directory: {result['working_dir']}")
            
            self.state['completed_phases'].append('ingestion')
            log_phase_end(logger, "Data Ingestion", success=True)
            
            return result
            
        except Exception as e:
            self.state['failed_phases'].append('ingestion')
            log_phase_end(logger, "Data Ingestion", success=False)
            raise
    
    def _run_profiling_phase(
        self,
        df: pd.DataFrame,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Run data profiling phase."""
        log_phase_start(logger, "Data Profiling")
        self.state['current_phase'] = 'profiling'
        
        try:
            profile = self.profiler.profile_dataframe(df, dataset_name)
            
            # Generate and log summary
            summary = self.profiler.generate_summary_report(profile)
            logger.info("Profile Summary:")
            for line in summary.split('\n')[:10]:  # First 10 lines
                logger.info(line)
            
            self.state['completed_phases'].append('profiling')
            log_phase_end(logger, "Data Profiling", success=True)
            
            return profile
            
        except Exception as e:
            self.state['failed_phases'].append('profiling')
            log_phase_end(logger, "Data Profiling", success=False)
            raise
    
    def _run_quality_checking_phase(
        self,
        df: pd.DataFrame,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Run quality checking phase."""
        log_phase_start(logger, "Quality Checking")
        self.state['current_phase'] = 'quality_checking'
        
        try:
            quality_result = self.quality_checker.check_quality(df, dataset_name)
            
            # Generate and log report
            report = self.quality_checker.generate_report(quality_result)
            logger.info("Quality Report:")
            for line in report.split('\n')[:15]:  # First 15 lines
                logger.info(line)
            
            logger.info(f"Quality Score: {quality_result['quality_score']}/100")
            
            self.state['completed_phases'].append('quality_checking')
            log_phase_end(logger, "Quality Checking", success=True)
            
            return quality_result
            
        except Exception as e:
            self.state['failed_phases'].append('quality_checking')
            log_phase_end(logger, "Quality Checking", success=False)
            raise
    
    def _should_clean_data(self, quality_result: Dict[str, Any]) -> bool:
        """Determine if data cleaning is needed."""
        quality_score = quality_result.get('quality_score', 100)
        critical_issues = quality_result.get('critical_issues', [])
        
        # Clean if quality score is below 80 or there are critical issues
        return quality_score < 80 or len(critical_issues) > 0
    
    def _run_cleaning_phase(
        self,
        df: pd.DataFrame,
        dataset_name: str,
        quality_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run data cleaning phase."""
        log_phase_start(logger, "Data Cleaning")
        self.state['current_phase'] = 'cleaning'
        
        try:
            # Generate cleaning strategies
            strategies = self.strategy_generator.generate_strategies(
                df,
                quality_result
            )
            
            logger.info(f"Generated {len(strategies)} cleaning strategies")
            
            # Apply transformations
            cleaned_df = self.transformer.apply_strategies(df, strategies)
            
            # Validate cleaned data
            validation_result = self.validator.validate_cleaned_data(
                df,
                cleaned_df,
                dataset_name,
                allow_row_reduction=True
            )
            
            validation_report = self.validator.generate_validation_report(validation_result)
            logger.info("Validation Report:")
            for line in validation_report.split('\n')[:10]:
                logger.info(line)
            
            result = {
                'strategies_applied': strategies,
                'cleaned_dataframe': cleaned_df,
                'validation': validation_result,
                'original_shape': df.shape,
                'cleaned_shape': cleaned_df.shape
            }
            
            self.state['completed_phases'].append('cleaning')
            log_phase_end(logger, "Data Cleaning", success=True)
            
            return result
            
        except Exception as e:
            self.state['failed_phases'].append('cleaning')
            log_phase_end(logger, "Data Cleaning", success=False)
            raise
    
    def _run_statistical_analysis_phase(
        self,
        df: pd.DataFrame,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Run statistical analysis phase."""
        log_phase_start(logger, "Statistical Analysis")
        self.state['current_phase'] = 'statistical_analysis'
        
        try:
            stats_result = self.statistical_analyzer.analyze_dataset(
                df,
                dataset_name
            )
            
            # Generate insights
            insights = self.statistical_analyzer.generate_insights(stats_result)
            logger.info("Key Insights:")
            for insight in insights[:5]:
                logger.info(f"  - {insight}")
            
            stats_result['insights'] = insights
            
            self.state['completed_phases'].append('statistical_analysis')
            log_phase_end(logger, "Statistical Analysis", success=True)
            
            return stats_result
            
        except Exception as e:
            self.state['failed_phases'].append('statistical_analysis')
            log_phase_end(logger, "Statistical Analysis", success=False)
            raise
    
    def _run_eda_phase(
        self,
        df: pd.DataFrame,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Run EDA report generation phase."""
        log_phase_start(logger, "EDA Report Generation")
        self.state['current_phase'] = 'eda'
        
        try:
            eda_report = self.eda_generator.generate_eda_report(
                df,
                dataset_name
            )
            
            # Generate text report
            text_report = self.eda_generator.generate_text_report(eda_report)
            logger.info("EDA Report Preview:")
            for line in text_report.split('\n')[:20]:
                logger.info(line)
            
            eda_report['text_report'] = text_report
            
            self.state['completed_phases'].append('eda')
            log_phase_end(logger, "EDA Report Generation", success=True)
            
            return eda_report
            
        except Exception as e:
            self.state['failed_phases'].append('eda')
            log_phase_end(logger, "EDA Report Generation", success=False)
            raise
    
    def _run_visualization_phase(
        self,
        df: pd.DataFrame,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Run visualization generation phase."""
        log_phase_start(logger, "Visualization Generation")
        self.state['current_phase'] = 'visualization'
        
        try:
            # Get recommendations
            recommendations = self.viz_recommender.recommend_visualizations(
                df,
                dataset_name,
                max_recommendations=15
            )
            
            logger.info(f"Generated {len(recommendations)} visualization recommendations")
            
            # Generate chart specifications
            chart_specs = self.chart_generator.generate_charts_for_dataset(
                df,
                dataset_name,
                max_charts=20
            )
            
            logger.info(f"Generated {len(chart_specs)} chart specifications")
            
            # Build Plotly figures (limit to avoid memory issues)
            figures = []
            for spec in chart_specs[:10]:  # Limit to 10 charts
                try:
                    fig = self.plotly_builder.build_chart(spec)
                    figures.append({
                        'spec': spec,
                        'figure': fig
                    })
                except Exception as e:
                    logger.warning(f"Failed to build chart {spec['title']}: {e}")
            
            logger.info(f"Built {len(figures)} Plotly figures")
            
            result = {
                'recommendations': recommendations,
                'chart_specs': chart_specs,
                'figures': figures,
                'summary': self.chart_generator.get_chart_summary(chart_specs)
            }
            
            self.state['completed_phases'].append('visualization')
            log_phase_end(logger, "Visualization Generation", success=True)
            
            return result
            
        except Exception as e:
            self.state['failed_phases'].append('visualization')
            log_phase_end(logger, "Visualization Generation", success=False)
            raise
    
    def get_pipeline_summary(self) -> str:
        """Generate a summary of the pipeline execution."""
        lines = []
        lines.append("=" * 80)
        lines.append("PIPELINE EXECUTION SUMMARY")
        lines.append("=" * 80)
        lines.append("")
        
        if self.state['start_time'] and self.state['end_time']:
            duration = (self.state['end_time'] - self.state['start_time']).total_seconds()
            lines.append(f"Duration: {duration:.2f} seconds")
        
        lines.append(f"Completed Phases: {len(self.state['completed_phases'])}")
        for phase in self.state['completed_phases']:
            lines.append(f"  ✓ {phase}")
        
        if self.state['failed_phases']:
            lines.append(f"\nFailed Phases: {len(self.state['failed_phases'])}")
            for phase in self.state['failed_phases']:
                lines.append(f"  ✗ {phase}")
        
        lines.append("")
        lines.append("=" * 80)
        
        return "\n".join(lines)


# Made with Bob