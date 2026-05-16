"""
Chart Generation Module
Generates various types of charts for data visualization
"""

from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import numpy as np
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ChartGenerator:
    """Generates chart specifications for various visualization libraries."""
    
    def __init__(self):
        """Initialize the chart generator."""
        self.chart_specs = []
    
    def generate_charts_for_dataset(
        self,
        df: pd.DataFrame,
        dataset_name: str,
        max_charts: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Generate appropriate charts for a dataset.
        
        Args:
            df: DataFrame to visualize
            dataset_name: Name of the dataset
            max_charts: Maximum number of charts to generate
        
        Returns:
            List of chart specifications
        """
        logger.info(f"Generating charts for {dataset_name}")
        
        charts = []
        
        # 1. Distribution charts for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        for col in numeric_cols[:5]:  # Limit to first 5
            charts.append(self.create_histogram_spec(df, col, dataset_name))
            charts.append(self.create_box_plot_spec(df, col, dataset_name))
        
        # 2. Bar charts for categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        for col in categorical_cols[:5]:  # Limit to first 5
            if df[col].nunique() <= 20:  # Only for low cardinality
                charts.append(self.create_bar_chart_spec(df, col, dataset_name))
        
        # 3. Correlation heatmap if multiple numeric columns
        if len(numeric_cols) >= 2:
            charts.append(self.create_correlation_heatmap_spec(df, numeric_cols, dataset_name))
        
        # 4. Scatter plots for numeric pairs
        if len(numeric_cols) >= 2:
            # Create scatter plots for top correlated pairs
            corr_matrix = df[numeric_cols].corr()
            top_pairs = self._get_top_correlated_pairs(corr_matrix, n=3)
            for col1, col2 in top_pairs:
                charts.append(self.create_scatter_plot_spec(df, col1, col2, dataset_name))
        
        # 5. Time series charts if datetime columns exist
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        if date_cols and numeric_cols:
            date_col = date_cols[0]
            for num_col in numeric_cols[:3]:  # First 3 numeric columns
                charts.append(self.create_line_chart_spec(df, date_col, num_col, dataset_name))
        
        # 6. Pie charts for categorical composition
        for col in categorical_cols[:2]:  # First 2 categorical
            if 3 <= df[col].nunique() <= 10:  # Good range for pie charts
                charts.append(self.create_pie_chart_spec(df, col, dataset_name))
        
        # Limit total charts
        charts = charts[:max_charts]
        
        logger.info(f"Generated {len(charts)} charts for {dataset_name}")
        
        return charts
    
    def create_histogram_spec(
        self,
        df: pd.DataFrame,
        column: str,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Create histogram specification."""
        return {
            'type': 'histogram',
            'title': f'Distribution of {column}',
            'dataset': dataset_name,
            'data': {
                'column': column,
                'values': df[column].dropna().tolist()
            },
            'config': {
                'bins': 30,
                'color': '#3498db',
                'opacity': 0.7
            },
            'layout': {
                'xaxis_title': column,
                'yaxis_title': 'Frequency',
                'showlegend': False
            }
        }
    
    def create_box_plot_spec(
        self,
        df: pd.DataFrame,
        column: str,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Create box plot specification."""
        return {
            'type': 'box',
            'title': f'Box Plot of {column}',
            'dataset': dataset_name,
            'data': {
                'column': column,
                'values': df[column].dropna().tolist()
            },
            'config': {
                'color': '#2ecc71',
                'boxmean': True
            },
            'layout': {
                'yaxis_title': column,
                'showlegend': False
            }
        }
    
    def create_bar_chart_spec(
        self,
        df: pd.DataFrame,
        column: str,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Create bar chart specification."""
        value_counts = df[column].value_counts().head(20)
        
        return {
            'type': 'bar',
            'title': f'Distribution of {column}',
            'dataset': dataset_name,
            'data': {
                'column': column,
                'categories': value_counts.index.tolist(),
                'values': value_counts.values.tolist()
            },
            'config': {
                'color': '#e74c3c',
                'orientation': 'v'
            },
            'layout': {
                'xaxis_title': column,
                'yaxis_title': 'Count',
                'showlegend': False
            }
        }
    
    def create_correlation_heatmap_spec(
        self,
        df: pd.DataFrame,
        columns: List[str],
        dataset_name: str
    ) -> Dict[str, Any]:
        """Create correlation heatmap specification."""
        corr_matrix = df[columns].corr()
        
        return {
            'type': 'heatmap',
            'title': 'Correlation Matrix',
            'dataset': dataset_name,
            'data': {
                'columns': columns,
                'correlation_matrix': corr_matrix.values.tolist(),
                'x_labels': corr_matrix.columns.tolist(),
                'y_labels': corr_matrix.index.tolist()
            },
            'config': {
                'colorscale': 'RdBu',
                'zmid': 0,
                'zmin': -1,
                'zmax': 1
            },
            'layout': {
                'xaxis_title': '',
                'yaxis_title': '',
                'showlegend': False
            }
        }
    
    def create_scatter_plot_spec(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Create scatter plot specification."""
        # Remove rows with NaN in either column
        clean_df = df[[x_column, y_column]].dropna()
        
        return {
            'type': 'scatter',
            'title': f'{y_column} vs {x_column}',
            'dataset': dataset_name,
            'data': {
                'x_column': x_column,
                'y_column': y_column,
                'x_values': clean_df[x_column].tolist(),
                'y_values': clean_df[y_column].tolist()
            },
            'config': {
                'mode': 'markers',
                'marker_color': '#9b59b6',
                'marker_size': 6,
                'opacity': 0.6
            },
            'layout': {
                'xaxis_title': x_column,
                'yaxis_title': y_column,
                'showlegend': False
            }
        }
    
    def create_line_chart_spec(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Create line chart specification for time series."""
        # Sort by date and remove NaN
        clean_df = df[[x_column, y_column]].dropna().sort_values(x_column)
        
        return {
            'type': 'line',
            'title': f'{y_column} over Time',
            'dataset': dataset_name,
            'data': {
                'x_column': x_column,
                'y_column': y_column,
                'x_values': clean_df[x_column].astype(str).tolist(),
                'y_values': clean_df[y_column].tolist()
            },
            'config': {
                'mode': 'lines+markers',
                'line_color': '#1abc9c',
                'line_width': 2
            },
            'layout': {
                'xaxis_title': x_column,
                'yaxis_title': y_column,
                'showlegend': False
            }
        }
    
    def create_pie_chart_spec(
        self,
        df: pd.DataFrame,
        column: str,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Create pie chart specification."""
        value_counts = df[column].value_counts().head(10)
        
        return {
            'type': 'pie',
            'title': f'Composition of {column}',
            'dataset': dataset_name,
            'data': {
                'column': column,
                'labels': value_counts.index.tolist(),
                'values': value_counts.values.tolist()
            },
            'config': {
                'hole': 0.3,  # Donut chart
                'textposition': 'inside'
            },
            'layout': {
                'showlegend': True
            }
        }
    
    def create_grouped_bar_chart_spec(
        self,
        df: pd.DataFrame,
        category_column: str,
        value_column: str,
        group_column: str,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Create grouped bar chart specification."""
        # Pivot data for grouped bar chart
        pivot_df = df.pivot_table(
            values=value_column,
            index=category_column,
            columns=group_column,
            aggfunc='mean'
        ).fillna(0)
        
        return {
            'type': 'grouped_bar',
            'title': f'{value_column} by {category_column} and {group_column}',
            'dataset': dataset_name,
            'data': {
                'categories': pivot_df.index.tolist(),
                'groups': pivot_df.columns.tolist(),
                'values': pivot_df.values.tolist()
            },
            'config': {
                'barmode': 'group'
            },
            'layout': {
                'xaxis_title': category_column,
                'yaxis_title': value_column,
                'showlegend': True
            }
        }
    
    def create_area_chart_spec(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        dataset_name: str
    ) -> Dict[str, Any]:
        """Create area chart specification."""
        clean_df = df[[x_column, y_column]].dropna().sort_values(x_column)
        
        return {
            'type': 'area',
            'title': f'{y_column} over {x_column}',
            'dataset': dataset_name,
            'data': {
                'x_column': x_column,
                'y_column': y_column,
                'x_values': clean_df[x_column].astype(str).tolist(),
                'y_values': clean_df[y_column].tolist()
            },
            'config': {
                'fill': 'tozeroy',
                'fillcolor': 'rgba(52, 152, 219, 0.3)',
                'line_color': '#3498db'
            },
            'layout': {
                'xaxis_title': x_column,
                'yaxis_title': y_column,
                'showlegend': False
            }
        }
    
    def _get_top_correlated_pairs(
        self,
        corr_matrix: pd.DataFrame,
        n: int = 3
    ) -> List[Tuple[str, str]]:
        """Get top N correlated variable pairs."""
        # Get upper triangle of correlation matrix
        pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = abs(corr_matrix.iloc[i, j])
                if not np.isnan(corr_value):
                    pairs.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        corr_value
                    ))
        
        # Sort by correlation strength and return top N
        pairs.sort(key=lambda x: x[2], reverse=True)
        return [(p[0], p[1]) for p in pairs[:n]]
    
    def save_chart_specs(self, charts: List[Dict[str, Any]], output_path: str):
        """
        Save chart specifications to JSON file.
        
        Args:
            charts: List of chart specifications
            output_path: Path to save JSON file
        """
        import json
        
        with open(output_path, 'w') as f:
            json.dump(charts, f, indent=2)
        
        logger.info(f"Saved {len(charts)} chart specifications to {output_path}")
    
    def get_chart_summary(self, charts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary of charts.
        
        Args:
            charts: List of chart specifications
        
        Returns:
            Summary dictionary
        """
        chart_types = {}
        for chart in charts:
            chart_type = chart['type']
            chart_types[chart_type] = chart_types.get(chart_type, 0) + 1
        
        return {
            'total_charts': len(charts),
            'chart_types': chart_types,
            'datasets': list(set(chart['dataset'] for chart in charts))
        }


# Made with Bob