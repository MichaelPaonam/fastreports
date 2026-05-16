"""
Exploratory Data Analysis (EDA) Module
Generates comprehensive EDA reports
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from src.analysis.statistics import StatisticalAnalyzer
from src.utils.logger import get_logger

logger = get_logger(__name__)


class EDAReportGenerator:
    """Generates comprehensive exploratory data analysis reports."""
    
    def __init__(self):
        """Initialize the EDA report generator."""
        self.statistical_analyzer = StatisticalAnalyzer()
    
    def generate_eda_report(
        self,
        df: pd.DataFrame,
        dataset_name: str,
        target_column: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive EDA report.
        
        Args:
            df: DataFrame to analyze
            dataset_name: Name of the dataset
            target_column: Optional target column for focused analysis
        
        Returns:
            Dictionary containing complete EDA report
        """
        logger.info(f"Generating EDA report for {dataset_name}")
        
        # Perform statistical analysis
        stats_results = self.statistical_analyzer.analyze_dataset(
            df, dataset_name, target_column
        )
        
        # Generate report sections
        report = {
            'dataset_name': dataset_name,
            'overview': self._generate_overview(df),
            'data_quality': self._generate_data_quality_section(df, stats_results),
            'variable_analysis': self._generate_variable_analysis(df, stats_results),
            'relationships': self._generate_relationships_section(stats_results),
            'key_findings': self._generate_key_findings(df, stats_results),
            'recommendations': self._generate_recommendations(df, stats_results),
            'statistical_results': stats_results
        }
        
        logger.info(f"EDA report generated for {dataset_name}")
        
        return report
    
    def _generate_overview(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate dataset overview section."""
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'memory_usage_mb': float(df.memory_usage(deep=True).sum() / 1024 / 1024),
            'column_types': {
                'numeric': len(df.select_dtypes(include=[np.number]).columns),
                'categorical': len(df.select_dtypes(include=['object', 'category']).columns),
                'datetime': len(df.select_dtypes(include=['datetime64']).columns),
                'other': len(df.columns) - len(df.select_dtypes(include=[np.number, 'object', 'category', 'datetime64']).columns)
            },
            'duplicate_rows': int(df.duplicated().sum()),
            'duplicate_percentage': float(df.duplicated().sum() / len(df) * 100)
        }
    
    def _generate_data_quality_section(
        self,
        df: pd.DataFrame,
        stats_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate data quality assessment section."""
        missing_analysis = stats_results.get('missing_value_analysis', {})
        outlier_analysis = stats_results.get('outlier_analysis', {})
        
        # Calculate quality score
        quality_score = 100
        
        # Deduct for missing values
        missing_pct = missing_analysis.get('missing_percentage_overall', 0)
        quality_score -= min(missing_pct, 30)
        
        # Deduct for duplicates
        dup_pct = df.duplicated().sum() / len(df) * 100
        quality_score -= min(dup_pct, 20)
        
        # Deduct for outliers
        outlier_cols = len(outlier_analysis.get('columns_with_outliers', []))
        total_numeric = len(df.select_dtypes(include=[np.number]).columns)
        if total_numeric > 0:
            outlier_pct = (outlier_cols / total_numeric) * 100
            quality_score -= min(outlier_pct / 2, 20)
        
        quality_score = max(0, quality_score)
        
        return {
            'quality_score': round(quality_score, 1),
            'quality_grade': self._get_quality_grade(quality_score),
            'missing_values': missing_analysis,
            'outliers': outlier_analysis,
            'duplicates': {
                'count': int(df.duplicated().sum()),
                'percentage': float(dup_pct)
            },
            'issues': self._identify_quality_issues(df, stats_results)
        }
    
    def _get_quality_grade(self, score: float) -> str:
        """Convert quality score to letter grade."""
        if score >= 90:
            return 'A - Excellent'
        elif score >= 80:
            return 'B - Good'
        elif score >= 70:
            return 'C - Fair'
        elif score >= 60:
            return 'D - Poor'
        else:
            return 'F - Critical Issues'
    
    def _identify_quality_issues(
        self,
        df: pd.DataFrame,
        stats_results: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Identify specific data quality issues."""
        issues = []
        
        # Missing value issues
        missing_analysis = stats_results.get('missing_value_analysis', {})
        for col, data in missing_analysis.get('columns_with_missing', {}).items():
            if data['percentage'] > 50:
                issues.append({
                    'severity': 'high',
                    'type': 'missing_values',
                    'column': col,
                    'description': f"{col} has {data['percentage']:.1f}% missing values"
                })
            elif data['percentage'] > 20:
                issues.append({
                    'severity': 'medium',
                    'type': 'missing_values',
                    'column': col,
                    'description': f"{col} has {data['percentage']:.1f}% missing values"
                })
        
        # Outlier issues
        outlier_analysis = stats_results.get('outlier_analysis', {})
        for col, data in outlier_analysis.get('outlier_details', {}).items():
            if data['percentage'] > 10:
                issues.append({
                    'severity': 'medium',
                    'type': 'outliers',
                    'column': col,
                    'description': f"{col} has {data['percentage']:.1f}% outliers"
                })
        
        # High cardinality issues
        categorical_analysis = stats_results.get('categorical_analysis', {})
        for col, data in categorical_analysis.items():
            if data['cardinality'] == 'high':
                issues.append({
                    'severity': 'low',
                    'type': 'high_cardinality',
                    'column': col,
                    'description': f"{col} has high cardinality ({data['unique_values']} unique values)"
                })
        
        return issues
    
    def _generate_variable_analysis(
        self,
        df: pd.DataFrame,
        stats_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate detailed variable analysis section."""
        numeric_analysis = {}
        categorical_analysis = {}
        
        # Numeric variables
        descriptive_stats = stats_results.get('descriptive_stats', {})
        distribution_analysis = stats_results.get('distribution_analysis', {})
        
        for col, stats in descriptive_stats.get('numeric_columns', {}).items():
            dist_info = distribution_analysis.get(col, {})
            
            numeric_analysis[col] = {
                'statistics': stats,
                'distribution': dist_info,
                'interpretation': self._interpret_numeric_variable(stats, dist_info)
            }
        
        # Categorical variables
        cat_stats = stats_results.get('categorical_analysis', {})
        for col, stats in cat_stats.items():
            categorical_analysis[col] = {
                'statistics': stats,
                'interpretation': self._interpret_categorical_variable(stats)
            }
        
        return {
            'numeric_variables': numeric_analysis,
            'categorical_variables': categorical_analysis,
            'total_numeric': len(numeric_analysis),
            'total_categorical': len(categorical_analysis)
        }
    
    def _interpret_numeric_variable(
        self,
        stats: Dict[str, Any],
        dist_info: Dict[str, Any]
    ) -> str:
        """Generate interpretation for numeric variable."""
        interpretations = []
        
        # Range interpretation
        if stats['min'] is not None and stats['max'] is not None:
            interpretations.append(
                f"Values range from {stats['min']:.2f} to {stats['max']:.2f}"
            )
        
        # Central tendency
        if stats['mean'] is not None and stats['median'] is not None:
            if abs(stats['mean'] - stats['median']) / stats['std'] > 0.5 if stats['std'] else False:
                interpretations.append("Mean and median differ significantly, indicating skewness")
        
        # Distribution
        if dist_info:
            dist_type = dist_info.get('distribution_type', '')
            if dist_type == 'right_skewed':
                interpretations.append("Distribution is right-skewed (tail extends to the right)")
            elif dist_type == 'left_skewed':
                interpretations.append("Distribution is left-skewed (tail extends to the left)")
            elif dist_type == 'approximately_normal':
                interpretations.append("Distribution is approximately normal")
        
        return "; ".join(interpretations) if interpretations else "No significant patterns detected"
    
    def _interpret_categorical_variable(self, stats: Dict[str, Any]) -> str:
        """Generate interpretation for categorical variable."""
        interpretations = []
        
        # Cardinality
        if stats['cardinality'] == 'high':
            interpretations.append(f"High cardinality with {stats['unique_values']} unique values")
        else:
            interpretations.append(f"Low cardinality with {stats['unique_values']} unique values")
        
        # Dominance
        if stats['most_common_percentage'] > 50:
            interpretations.append(
                f"Dominated by '{stats['most_common']}' ({stats['most_common_percentage']:.1f}%)"
            )
        elif stats['most_common_percentage'] < 10:
            interpretations.append("Values are relatively evenly distributed")
        
        return "; ".join(interpretations)
    
    def _generate_relationships_section(
        self,
        stats_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate relationships and correlations section."""
        correlation_analysis = stats_results.get('correlation_analysis', {})
        
        return {
            'correlations': correlation_analysis,
            'strong_relationships': correlation_analysis.get('strong_correlations', []),
            'relationship_summary': self._summarize_relationships(correlation_analysis)
        }
    
    def _summarize_relationships(self, correlation_analysis: Dict[str, Any]) -> str:
        """Summarize key relationships found."""
        strong_corr = correlation_analysis.get('strong_correlations', [])
        
        if not strong_corr:
            return "No strong correlations detected between variables"
        
        summaries = []
        for corr in strong_corr[:5]:  # Top 5
            summaries.append(
                f"{corr['variable1']} and {corr['variable2']} are {corr['strength']} "
                f"(r={corr['correlation']:.2f})"
            )
        
        return "; ".join(summaries)
    
    def _generate_key_findings(
        self,
        df: pd.DataFrame,
        stats_results: Dict[str, Any]
    ) -> List[str]:
        """Generate key findings from the analysis."""
        findings = []
        
        # Dataset size finding
        if len(df) > 100000:
            findings.append(f"Large dataset with {len(df):,} rows - suitable for robust analysis")
        elif len(df) < 100:
            findings.append(f"Small dataset with {len(df)} rows - statistical power may be limited")
        
        # Missing value findings
        missing_analysis = stats_results.get('missing_value_analysis', {})
        missing_pct = missing_analysis.get('missing_percentage_overall', 0)
        if missing_pct > 10:
            findings.append(f"Significant missing data ({missing_pct:.1f}%) requires attention")
        
        # Correlation findings
        correlation_analysis = stats_results.get('correlation_analysis', {})
        strong_corr = correlation_analysis.get('strong_correlations', [])
        if strong_corr:
            findings.append(f"Found {len(strong_corr)} strong correlations between variables")
        
        # Distribution findings
        distribution_analysis = stats_results.get('distribution_analysis', {})
        non_normal = sum(1 for d in distribution_analysis.values() if not d.get('is_normal', True))
        if non_normal > 0:
            findings.append(f"{non_normal} variables show non-normal distributions")
        
        # Outlier findings
        outlier_analysis = stats_results.get('outlier_analysis', {})
        outlier_cols = outlier_analysis.get('columns_with_outliers', [])
        if outlier_cols:
            findings.append(f"Outliers detected in {len(outlier_cols)} columns")
        
        # Time series findings
        if 'time_series_analysis' in stats_results:
            ts_analysis = stats_results['time_series_analysis']
            date_range = ts_analysis.get('date_range', {})
            if date_range:
                findings.append(
                    f"Time series data spans {date_range.get('span_days', 0)} days"
                )
        
        return findings if findings else ["No significant findings detected"]
    
    def _generate_recommendations(
        self,
        df: pd.DataFrame,
        stats_results: Dict[str, Any]
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Missing value recommendations
        missing_analysis = stats_results.get('missing_value_analysis', {})
        for col, data in missing_analysis.get('columns_with_missing', {}).items():
            if data['percentage'] > 50:
                recommendations.append(
                    f"Consider removing column '{col}' due to {data['percentage']:.1f}% missing values"
                )
            elif data['percentage'] > 20:
                recommendations.append(
                    f"Implement imputation strategy for '{col}' ({data['percentage']:.1f}% missing)"
                )
        
        # Outlier recommendations
        outlier_analysis = stats_results.get('outlier_analysis', {})
        for col, data in outlier_analysis.get('outlier_details', {}).items():
            if data['percentage'] > 5:
                recommendations.append(
                    f"Investigate outliers in '{col}' ({data['percentage']:.1f}% of values)"
                )
        
        # Distribution recommendations
        distribution_analysis = stats_results.get('distribution_analysis', {})
        for col, data in distribution_analysis.items():
            if data.get('distribution_type') in ['right_skewed', 'left_skewed']:
                recommendations.append(
                    f"Consider log transformation for '{col}' to normalize distribution"
                )
        
        # Correlation recommendations
        correlation_analysis = stats_results.get('correlation_analysis', {})
        strong_corr = correlation_analysis.get('strong_correlations', [])
        if len(strong_corr) > 5:
            recommendations.append(
                "Multiple strong correlations detected - consider dimensionality reduction"
            )
        
        # Categorical recommendations
        categorical_analysis = stats_results.get('categorical_analysis', {})
        for col, data in categorical_analysis.items():
            if data['cardinality'] == 'high' and data['unique_values'] > 100:
                recommendations.append(
                    f"Consider grouping or encoding '{col}' (high cardinality: {data['unique_values']} values)"
                )
        
        return recommendations if recommendations else ["No specific recommendations at this time"]
    
    def generate_text_report(self, eda_report: Dict[str, Any]) -> str:
        """
        Generate a human-readable text report from EDA results.
        
        Args:
            eda_report: EDA report dictionary
        
        Returns:
            Formatted text report
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"EXPLORATORY DATA ANALYSIS REPORT: {eda_report['dataset_name']}")
        lines.append("=" * 80)
        lines.append("")
        
        # Overview
        overview = eda_report['overview']
        lines.append("DATASET OVERVIEW")
        lines.append("-" * 80)
        lines.append(f"Rows: {overview['rows']:,}")
        lines.append(f"Columns: {overview['columns']}")
        lines.append(f"Memory Usage: {overview['memory_usage_mb']:.2f} MB")
        lines.append(f"Numeric Columns: {overview['column_types']['numeric']}")
        lines.append(f"Categorical Columns: {overview['column_types']['categorical']}")
        lines.append(f"Duplicate Rows: {overview['duplicate_rows']} ({overview['duplicate_percentage']:.1f}%)")
        lines.append("")
        
        # Data Quality
        quality = eda_report['data_quality']
        lines.append("DATA QUALITY ASSESSMENT")
        lines.append("-" * 80)
        lines.append(f"Quality Score: {quality['quality_score']}/100 ({quality['quality_grade']})")
        lines.append("")
        
        if quality['issues']:
            lines.append("Quality Issues:")
            for issue in quality['issues']:
                severity_icon = "🔴" if issue['severity'] == 'high' else "🟡" if issue['severity'] == 'medium' else "🟢"
                lines.append(f"  {severity_icon} {issue['description']}")
            lines.append("")
        
        # Key Findings
        lines.append("KEY FINDINGS")
        lines.append("-" * 80)
        for i, finding in enumerate(eda_report['key_findings'], 1):
            lines.append(f"{i}. {finding}")
        lines.append("")
        
        # Recommendations
        lines.append("RECOMMENDATIONS")
        lines.append("-" * 80)
        for i, rec in enumerate(eda_report['recommendations'], 1):
            lines.append(f"{i}. {rec}")
        lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)


# Made with Bob