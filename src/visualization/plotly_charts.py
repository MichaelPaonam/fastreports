"""
Plotly Chart Integration Module
Converts chart specifications to Plotly figures
"""

from typing import Dict, List, Any, Optional
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PlotlyChartBuilder:
    """Builds Plotly charts from chart specifications."""
    
    def __init__(self):
        """Initialize the Plotly chart builder."""
        self.default_template = 'plotly_white'
        self.color_palette = px.colors.qualitative.Set2
    
    def build_chart(self, chart_spec: Dict[str, Any]) -> go.Figure:
        """
        Build a Plotly figure from chart specification.
        
        Args:
            chart_spec: Chart specification dictionary
        
        Returns:
            Plotly Figure object
        """
        chart_type = chart_spec['type']
        
        builders = {
            'histogram': self._build_histogram,
            'box': self._build_box_plot,
            'bar': self._build_bar_chart,
            'heatmap': self._build_heatmap,
            'scatter': self._build_scatter_plot,
            'line': self._build_line_chart,
            'pie': self._build_pie_chart,
            'grouped_bar': self._build_grouped_bar_chart,
            'area': self._build_area_chart
        }
        
        if chart_type not in builders:
            logger.warning(f"Unknown chart type: {chart_type}")
            return self._build_placeholder_chart(chart_spec)
        
        try:
            fig = builders[chart_type](chart_spec)
            self._apply_common_layout(fig, chart_spec)
            return fig
        except Exception as e:
            logger.error(f"Error building {chart_type} chart: {e}")
            return self._build_placeholder_chart(chart_spec)
    
    def _build_histogram(self, spec: Dict[str, Any]) -> go.Figure:
        """Build histogram chart."""
        data = spec['data']
        config = spec.get('config', {})
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=data['values'],
            nbinsx=config.get('bins', 30),
            marker_color=config.get('color', '#3498db'),
            opacity=config.get('opacity', 0.7),
            name=data['column']
        ))
        
        return fig
    
    def _build_box_plot(self, spec: Dict[str, Any]) -> go.Figure:
        """Build box plot chart."""
        data = spec['data']
        config = spec.get('config', {})
        
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=data['values'],
            name=data['column'],
            marker_color=config.get('color', '#2ecc71'),
            boxmean=config.get('boxmean', True)
        ))
        
        return fig
    
    def _build_bar_chart(self, spec: Dict[str, Any]) -> go.Figure:
        """Build bar chart."""
        data = spec['data']
        config = spec.get('config', {})
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=data['categories'] if config.get('orientation', 'v') == 'v' else data['values'],
            y=data['values'] if config.get('orientation', 'v') == 'v' else data['categories'],
            marker_color=config.get('color', '#e74c3c'),
            orientation=config.get('orientation', 'v'),
            name=data['column']
        ))
        
        return fig
    
    def _build_heatmap(self, spec: Dict[str, Any]) -> go.Figure:
        """Build correlation heatmap."""
        data = spec['data']
        config = spec.get('config', {})
        
        fig = go.Figure()
        fig.add_trace(go.Heatmap(
            z=data['correlation_matrix'],
            x=data['x_labels'],
            y=data['y_labels'],
            colorscale=config.get('colorscale', 'RdBu'),
            zmid=config.get('zmid', 0),
            zmin=config.get('zmin', -1),
            zmax=config.get('zmax', 1),
            text=np.round(data['correlation_matrix'], 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        return fig
    
    def _build_scatter_plot(self, spec: Dict[str, Any]) -> go.Figure:
        """Build scatter plot."""
        data = spec['data']
        config = spec.get('config', {})
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data['x_values'],
            y=data['y_values'],
            mode=config.get('mode', 'markers'),
            marker=dict(
                color=config.get('marker_color', '#9b59b6'),
                size=config.get('marker_size', 6),
                opacity=config.get('opacity', 0.6)
            ),
            name=f"{data['y_column']} vs {data['x_column']}"
        ))
        
        # Add trendline if requested
        if config.get('trendline', False):
            z = np.polyfit(data['x_values'], data['y_values'], 1)
            p = np.poly1d(z)
            fig.add_trace(go.Scatter(
                x=data['x_values'],
                y=p(data['x_values']),
                mode='lines',
                line=dict(color='red', dash='dash'),
                name='Trendline'
            ))
        
        return fig
    
    def _build_line_chart(self, spec: Dict[str, Any]) -> go.Figure:
        """Build line chart."""
        data = spec['data']
        config = spec.get('config', {})
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data['x_values'],
            y=data['y_values'],
            mode=config.get('mode', 'lines+markers'),
            line=dict(
                color=config.get('line_color', '#1abc9c'),
                width=config.get('line_width', 2)
            ),
            marker=dict(size=4),
            name=data['y_column']
        ))
        
        return fig
    
    def _build_pie_chart(self, spec: Dict[str, Any]) -> go.Figure:
        """Build pie chart."""
        data = spec['data']
        config = spec.get('config', {})
        
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=data['labels'],
            values=data['values'],
            hole=config.get('hole', 0.3),
            textposition=config.get('textposition', 'inside'),
            textinfo='label+percent',
            marker=dict(colors=self.color_palette)
        ))
        
        return fig
    
    def _build_grouped_bar_chart(self, spec: Dict[str, Any]) -> go.Figure:
        """Build grouped bar chart."""
        data = spec['data']
        config = spec.get('config', {})
        
        fig = go.Figure()
        
        for i, group in enumerate(data['groups']):
            fig.add_trace(go.Bar(
                name=str(group),
                x=data['categories'],
                y=[row[i] for row in data['values']],
                marker_color=self.color_palette[i % len(self.color_palette)]
            ))
        
        fig.update_layout(barmode=config.get('barmode', 'group'))
        
        return fig
    
    def _build_area_chart(self, spec: Dict[str, Any]) -> go.Figure:
        """Build area chart."""
        data = spec['data']
        config = spec.get('config', {})
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data['x_values'],
            y=data['y_values'],
            fill=config.get('fill', 'tozeroy'),
            fillcolor=config.get('fillcolor', 'rgba(52, 152, 219, 0.3)'),
            line=dict(color=config.get('line_color', '#3498db')),
            name=data['y_column']
        ))
        
        return fig
    
    def _build_placeholder_chart(self, spec: Dict[str, Any]) -> go.Figure:
        """Build placeholder chart for unsupported types."""
        fig = go.Figure()
        fig.add_annotation(
            text=f"Chart type '{spec['type']}' not yet implemented",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    def _apply_common_layout(self, fig: go.Figure, spec: Dict[str, Any]):
        """Apply common layout settings to figure."""
        layout = spec.get('layout', {})
        
        fig.update_layout(
            title=dict(
                text=spec.get('title', ''),
                x=0.5,
                xanchor='center',
                font=dict(size=16, family='Arial, sans-serif')
            ),
            xaxis_title=layout.get('xaxis_title', ''),
            yaxis_title=layout.get('yaxis_title', ''),
            showlegend=layout.get('showlegend', True),
            template=self.default_template,
            hovermode='closest',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial, sans-serif', size=12),
            margin=dict(l=60, r=40, t=80, b=60)
        )
        
        # Update axes
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            showline=True,
            linewidth=1,
            linecolor='black'
        )
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            showline=True,
            linewidth=1,
            linecolor='black'
        )
    
    def build_multiple_charts(
        self,
        chart_specs: List[Dict[str, Any]]
    ) -> List[go.Figure]:
        """
        Build multiple Plotly figures from chart specifications.
        
        Args:
            chart_specs: List of chart specifications
        
        Returns:
            List of Plotly Figure objects
        """
        logger.info(f"Building {len(chart_specs)} Plotly charts")
        
        figures = []
        for spec in chart_specs:
            fig = self.build_chart(spec)
            figures.append(fig)
        
        logger.info(f"Successfully built {len(figures)} charts")
        
        return figures
    
    def save_chart_as_html(
        self,
        fig: go.Figure,
        output_path: str,
        include_plotlyjs: str = 'cdn'
    ):
        """
        Save Plotly figure as HTML file.
        
        Args:
            fig: Plotly Figure object
            output_path: Path to save HTML file
            include_plotlyjs: How to include plotly.js ('cdn', 'inline', or False)
        """
        fig.write_html(
            output_path,
            include_plotlyjs=include_plotlyjs,
            config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
            }
        )
        logger.info(f"Saved chart to {output_path}")
    
    def save_chart_as_image(
        self,
        fig: go.Figure,
        output_path: str,
        width: int = 1200,
        height: int = 800,
        format: str = 'png'
    ):
        """
        Save Plotly figure as static image.
        
        Args:
            fig: Plotly Figure object
            output_path: Path to save image file
            width: Image width in pixels
            height: Image height in pixels
            format: Image format ('png', 'jpg', 'svg', 'pdf')
        """
        try:
            fig.write_image(
                output_path,
                width=width,
                height=height,
                format=format
            )
            logger.info(f"Saved chart image to {output_path}")
        except Exception as e:
            logger.error(f"Error saving chart as image: {e}")
            logger.info("Note: Image export requires kaleido package")
    
    def get_chart_json(self, fig: go.Figure) -> str:
        """
        Get JSON representation of Plotly figure.
        
        Args:
            fig: Plotly Figure object
        
        Returns:
            JSON string
        """
        return fig.to_json()
    
    def create_dashboard_layout(
        self,
        figures: List[go.Figure],
        rows: int,
        cols: int,
        subplot_titles: Optional[List[str]] = None
    ) -> go.Figure:
        """
        Create a dashboard layout with multiple subplots.
        
        Args:
            figures: List of Plotly figures
            rows: Number of rows
            cols: Number of columns
            subplot_titles: Optional titles for subplots
        
        Returns:
            Combined Plotly Figure with subplots
        """
        fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=subplot_titles,
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )
        
        for idx, source_fig in enumerate(figures[:rows * cols]):
            row = (idx // cols) + 1
            col = (idx % cols) + 1
            
            for trace in source_fig.data:
                fig.add_trace(trace, row=row, col=col)
        
        fig.update_layout(
            height=400 * rows,
            showlegend=False,
            template=self.default_template
        )
        
        return fig
    
    def add_annotations(
        self,
        fig: go.Figure,
        annotations: List[Dict[str, Any]]
    ) -> go.Figure:
        """
        Add annotations to a Plotly figure.
        
        Args:
            fig: Plotly Figure object
            annotations: List of annotation dictionaries
        
        Returns:
            Updated Plotly Figure
        """
        for ann in annotations:
            fig.add_annotation(
                x=ann.get('x', 0),
                y=ann.get('y', 0),
                text=ann.get('text', ''),
                showarrow=ann.get('showarrow', True),
                arrowhead=ann.get('arrowhead', 2),
                ax=ann.get('ax', 0),
                ay=ann.get('ay', -40)
            )
        
        return fig


# Made with Bob