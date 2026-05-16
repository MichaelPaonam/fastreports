"""
Visualization Recommender Module
Recommends appropriate visualizations based on data characteristics
"""

from typing import Dict, List, Any, Tuple
import pandas as pd
import numpy as np
from src.utils.logger import get_logger

logger = get_logger(__name__)


class VisualizationRecommender:
    """Recommends appropriate visualizations for data."""
    
    def __init__(self):
        """Initialize the visualization recommender."""
        self.recommendations = []
    
    def recommend_visualizations(
        self,
        df: pd.DataFrame,
        dataset_name: str,
        max_recommendations: int = 15
    ) -> List[Dict[str, Any]]:
        """
        Recommend visualizations based on data characteristics.
        
        Args:
            df: DataFrame to analyze
            dataset_name: Name of the dataset
            max_recommendations: Maximum number of recommendations
        
        Returns:
            List of visualization recommendations
        """
        logger.info(f"Generating visualization recommendations for {dataset_name}")
        
        recommendations = []
        
        # Analyze column types
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        # 1. Distribution visualizations for numeric columns
        for col in numeric_cols[:5]:
            recommendations.extend(self._recommend_for_numeric_column(df, col))
        
        # 2. Categorical visualizations
        for col in categorical_cols[:5]:
            recommendations.extend(self._recommend_for_categorical_column(df, col))
        
        # 3. Relationship visualizations
        if len(numeric_cols) >= 2:
            recommendations.extend(self._recommend_for_numeric_relationships(df, numeric_cols))
        
        # 4. Time series visualizations
        if datetime_cols and numeric_cols:
            recommendations.extend(self._recommend_for_time_series(df, datetime_cols[0], numeric_cols))
        
        # 5. Mixed type visualizations
        if categorical_cols and numeric_cols:
            recommendations.extend(self._recommend_for_mixed_types(df, categorical_cols, numeric_cols))
        
        # Prioritize and limit recommendations
        recommendations = self._prioritize_recommendations(recommendations)
        recommendations = recommendations[:max_recommendations]
        
        logger.info(f"Generated {len(recommendations)} visualization recommendations")
        
        return recommendations
    
    def _recommend_for_numeric_column(
        self,
        df: pd.DataFrame,
        column: str
    ) -> List[Dict[str, Any]]:
        """Recommend visualizations for a numeric column."""
        recommendations = []
        
        # Histogram for distribution
        recommendations.append({
            'chart_type': 'histogram',
            'priority': 'high',
            'reason': 'Show distribution of numeric values',
            'columns': [column],
            'description': f'Distribution of {column}',
            'use_case': 'Understanding value distribution and identifying patterns'
        })
        
        # Box plot for outlier detection
        recommendations.append({
            'chart_type': 'box',
            'priority': 'medium',
            'reason': 'Identify outliers and quartiles',
            'columns': [column],
            'description': f'Box plot of {column}',
            'use_case': 'Detecting outliers and understanding spread'
        })
        
        return recommendations
    
    def _recommend_for_categorical_column(
        self,
        df: pd.DataFrame,
        column: str
    ) -> List[Dict[str, Any]]:
        """Recommend visualizations for a categorical column."""
        recommendations = []
        
        unique_count = df[column].nunique()
        
        # Bar chart for low cardinality
        if unique_count <= 20:
            recommendations.append({
                'chart_type': 'bar',
                'priority': 'high',
                'reason': 'Compare frequencies of categories',
                'columns': [column],
                'description': f'Frequency of {column} categories',
                'use_case': 'Comparing category frequencies'
            })
        
        # Pie chart for composition (3-10 categories)
        if 3 <= unique_count <= 10:
            recommendations.append({
                'chart_type': 'pie',
                'priority': 'medium',
                'reason': 'Show composition and proportions',
                'columns': [column],
                'description': f'Composition of {column}',
                'use_case': 'Understanding proportional breakdown'
            })
        
        return recommendations
    
    def _recommend_for_numeric_relationships(
        self,
        df: pd.DataFrame,
        numeric_cols: List[str]
    ) -> List[Dict[str, Any]]:
        """Recommend visualizations for numeric relationships."""
        recommendations = []
        
        # Correlation heatmap
        if len(numeric_cols) >= 2:
            recommendations.append({
                'chart_type': 'heatmap',
                'priority': 'high',
                'reason': 'Visualize correlations between all numeric variables',
                'columns': numeric_cols,
                'description': 'Correlation matrix',
                'use_case': 'Identifying relationships between variables'
            })
        
        # Scatter plots for top correlated pairs
        if len(numeric_cols) >= 2:
            corr_matrix = df[numeric_cols].corr()
            top_pairs = self._get_top_correlated_pairs(corr_matrix, n=3)
            
            for col1, col2, corr_value in top_pairs:
                recommendations.append({
                    'chart_type': 'scatter',
                    'priority': 'high' if abs(corr_value) > 0.7 else 'medium',
                    'reason': f'Strong correlation detected (r={corr_value:.2f})',
                    'columns': [col1, col2],
                    'description': f'{col2} vs {col1}',
                    'use_case': 'Exploring relationship between correlated variables'
                })
        
        return recommendations
    
    def _recommend_for_time_series(
        self,
        df: pd.DataFrame,
        date_column: str,
        numeric_cols: List[str]
    ) -> List[Dict[str, Any]]:
        """Recommend visualizations for time series data."""
        recommendations = []
        
        for col in numeric_cols[:3]:  # Top 3 numeric columns
            # Line chart for trends
            recommendations.append({
                'chart_type': 'line',
                'priority': 'high',
                'reason': 'Show trends over time',
                'columns': [date_column, col],
                'description': f'{col} over time',
                'use_case': 'Analyzing temporal trends and patterns'
            })
            
            # Area chart for cumulative view
            recommendations.append({
                'chart_type': 'area',
                'priority': 'medium',
                'reason': 'Show cumulative trends',
                'columns': [date_column, col],
                'description': f'{col} area chart over time',
                'use_case': 'Visualizing cumulative changes'
            })
        
        return recommendations
    
    def _recommend_for_mixed_types(
        self,
        df: pd.DataFrame,
        categorical_cols: List[str],
        numeric_cols: List[str]
    ) -> List[Dict[str, Any]]:
        """Recommend visualizations for mixed categorical and numeric data."""
        recommendations = []
        
        # Grouped bar charts
        for cat_col in categorical_cols[:2]:
            if df[cat_col].nunique() <= 10:  # Low cardinality
                for num_col in numeric_cols[:2]:
                    recommendations.append({
                        'chart_type': 'grouped_bar',
                        'priority': 'medium',
                        'reason': 'Compare numeric values across categories',
                        'columns': [cat_col, num_col],
                        'description': f'{num_col} by {cat_col}',
                        'use_case': 'Comparing metrics across categories'
                    })
        
        return recommendations
    
    def _get_top_correlated_pairs(
        self,
        corr_matrix: pd.DataFrame,
        n: int = 3
    ) -> List[Tuple[str, str, float]]:
        """Get top N correlated variable pairs."""
        pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if not np.isnan(corr_value):
                    pairs.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        corr_value
                    ))
        
        # Sort by absolute correlation value
        pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        return pairs[:n]
    
    def _prioritize_recommendations(
        self,
        recommendations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Prioritize recommendations based on priority and usefulness."""
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        
        return sorted(
            recommendations,
            key=lambda x: priority_order.get(x['priority'], 3)
        )
    
    def get_recommendation_summary(
        self,
        recommendations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate summary of recommendations.
        
        Args:
            recommendations: List of recommendations
        
        Returns:
            Summary dictionary
        """
        chart_types = {}
        priorities = {'high': 0, 'medium': 0, 'low': 0}
        
        for rec in recommendations:
            chart_type = rec['chart_type']
            chart_types[chart_type] = chart_types.get(chart_type, 0) + 1
            
            priority = rec['priority']
            priorities[priority] = priorities.get(priority, 0) + 1
        
        return {
            'total_recommendations': len(recommendations),
            'chart_types': chart_types,
            'priorities': priorities,
            'high_priority_count': priorities['high']
        }
    
    def generate_recommendation_report(
        self,
        recommendations: List[Dict[str, Any]]
    ) -> str:
        """
        Generate human-readable recommendation report.
        
        Args:
            recommendations: List of recommendations
        
        Returns:
            Formatted report string
        """
        lines = []
        lines.append("=" * 80)
        lines.append("VISUALIZATION RECOMMENDATIONS")
        lines.append("=" * 80)
        lines.append("")
        
        summary = self.get_recommendation_summary(recommendations)
        lines.append(f"Total Recommendations: {summary['total_recommendations']}")
        lines.append(f"High Priority: {summary['high_priority_count']}")
        lines.append("")
        
        # Group by priority
        for priority in ['high', 'medium', 'low']:
            priority_recs = [r for r in recommendations if r['priority'] == priority]
            if priority_recs:
                lines.append(f"{priority.upper()} PRIORITY VISUALIZATIONS:")
                lines.append("-" * 80)
                for i, rec in enumerate(priority_recs, 1):
                    lines.append(f"{i}. {rec['description']} ({rec['chart_type']})")
                    lines.append(f"   Reason: {rec['reason']}")
                    lines.append(f"   Use Case: {rec['use_case']}")
                    lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)


# Made with Bob