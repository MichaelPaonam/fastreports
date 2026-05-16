"""
HTML Report Generator Module
Generates static HTML reports with embedded visualizations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import base64
from io import BytesIO
from src.utils.logger import get_logger
from src.visualization.plotly_charts import PlotlyChartBuilder

logger = get_logger(__name__)


class HTMLReportGenerator:
    """Generates comprehensive HTML reports with embedded visualizations."""
    
    def __init__(self):
        """Initialize the HTML report generator."""
        self.chart_builder = PlotlyChartBuilder()
        self.template_dir = Path(__file__).parent / "templates"
        
    def generate_report(
        self,
        profile: Dict[str, Any],
        charts: Optional[List[Any]] = None,
        analysis_results: Optional[Dict[str, Any]] = None,
        output_path: str = "report.html"
    ) -> str:
        """
        Generate comprehensive HTML report.
        
        Args:
            profile: Data profile dictionary
            charts: List of Plotly figures
            analysis_results: Additional analysis results
            output_path: Path to save HTML report
            
        Returns:
            Path to generated report
        """
        logger.info(f"Generating HTML report: {output_path}")
        
        html_content = self._build_html_structure(
            profile=profile,
            charts=charts or [],
            analysis_results=analysis_results or {}
        )
        
        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html_content, encoding='utf-8')
        
        logger.info(f"Report generated successfully: {output_path}")
        return str(output_file)
    
    def _build_html_structure(
        self,
        profile: Dict[str, Any],
        charts: List[Any],
        analysis_results: Dict[str, Any]
    ) -> str:
        """Build complete HTML structure."""
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Analysis Report - {profile.get('dataset_name', 'Dataset')}</title>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
    {self._get_styles()}
</head>
<body>
    <div class="container">
        {self._build_header(profile)}
        {self._build_executive_summary(profile)}
        {self._build_data_overview(profile)}
        {self._build_data_quality_section(profile)}
        {self._build_column_profiles(profile)}
        {self._build_visualizations_section(charts)}
        {self._build_analysis_results_section(analysis_results)}
        {self._build_footer()}
    </div>
    {self._get_scripts()}
</body>
</html>"""
        
        return html
    
    def _get_styles(self) -> str:
        """Get CSS styles for the report."""
        return """
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        h2 {
            color: #667eea;
            margin: 30px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        
        h3 {
            color: #764ba2;
            margin: 20px 0 10px 0;
        }
        
        .section {
            margin-bottom: 40px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }
        
        .metric-label {
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #333;
            margin: 10px 0;
        }
        
        .metric-description {
            font-size: 0.85em;
            color: #888;
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }
        
        .status-good {
            background: #d4edda;
            color: #155724;
        }
        
        .status-warning {
            background: #fff3cd;
            color: #856404;
        }
        
        .status-error {
            background: #f8d7da;
            color: #721c24;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background: #667eea;
            color: white;
            font-weight: 600;
        }
        
        tr:hover {
            background: #f5f5f5;
        }
        
        .chart-container {
            margin: 30px 0;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .chart-title {
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 15px;
            color: #333;
        }
        
        footer {
            margin-top: 50px;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #ddd;
        }
        
        .timestamp {
            font-size: 0.9em;
            color: #888;
        }
        
        .column-profile {
            background: white;
            padding: 15px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #764ba2;
        }
        
        .column-name {
            font-weight: 600;
            font-size: 1.1em;
            color: #333;
            margin-bottom: 10px;
        }
        
        .column-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }
        
        .stat-item {
            padding: 8px;
            background: #f9f9f9;
            border-radius: 4px;
        }
        
        .stat-label {
            font-size: 0.85em;
            color: #666;
        }
        
        .stat-value {
            font-weight: 600;
            color: #333;
        }
        
        @media print {
            body {
                background: white;
            }
            
            .container {
                box-shadow: none;
            }
            
            .chart-container {
                page-break-inside: avoid;
            }
        }
    </style>
"""
    
    def _build_header(self, profile: Dict[str, Any]) -> str:
        """Build report header."""
        dataset_name = profile.get('dataset_name', 'Dataset')
        timestamp = profile.get('timestamp', datetime.now().isoformat())
        
        return f"""
    <header>
        <h1>📊 Data Analysis Report</h1>
        <p style="font-size: 1.2em; margin-top: 10px;">{dataset_name}</p>
        <p class="timestamp">Generated: {timestamp}</p>
    </header>
"""
    
    def _build_executive_summary(self, profile: Dict[str, Any]) -> str:
        """Build executive summary section."""
        overview = profile.get('overview', {})
        missing = profile.get('missing_values', {})
        duplicates = profile.get('duplicates', {})
        
        # Determine data quality status
        missing_pct = missing.get('missing_percentage', 0)
        duplicate_pct = duplicates.get('duplicate_percentage', 0)
        
        if missing_pct < 5 and duplicate_pct < 1:
            quality_status = '<span class="status-badge status-good">Excellent</span>'
        elif missing_pct < 15 and duplicate_pct < 5:
            quality_status = '<span class="status-badge status-warning">Good</span>'
        else:
            quality_status = '<span class="status-badge status-error">Needs Attention</span>'
        
        return f"""
    <section class="section">
        <h2>Executive Summary</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Total Rows</div>
                <div class="metric-value">{overview.get('rows', 0):,}</div>
                <div class="metric-description">Data records</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Columns</div>
                <div class="metric-value">{overview.get('columns', 0)}</div>
                <div class="metric-description">Features analyzed</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Data Quality</div>
                <div class="metric-value">{quality_status}</div>
                <div class="metric-description">{missing_pct:.1f}% missing data</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Memory Usage</div>
                <div class="metric-value">{profile.get('memory', {}).get('total_mb', 0):.1f} MB</div>
                <div class="metric-description">Total size</div>
            </div>
        </div>
    </section>
"""
    
    def _build_data_overview(self, profile: Dict[str, Any]) -> str:
        """Build data overview section."""
        overview = profile.get('overview', {})
        
        return f"""
    <section class="section">
        <h2>Data Overview</h2>
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Total Rows</td>
                <td>{overview.get('rows', 0):,}</td>
            </tr>
            <tr>
                <td>Total Columns</td>
                <td>{overview.get('columns', 0)}</td>
            </tr>
            <tr>
                <td>Total Cells</td>
                <td>{overview.get('total_cells', 0):,}</td>
            </tr>
            <tr>
                <td>Memory Usage</td>
                <td>{profile.get('memory', {}).get('total_mb', 0):.2f} MB</td>
            </tr>
        </table>
        
        <h3>Column Types</h3>
        <table>
            <tr>
                <th>Data Type</th>
                <th>Count</th>
            </tr>
            {self._build_dtype_rows(overview.get('dtypes_summary', {}))}
        </table>
    </section>
"""
    
    def _build_dtype_rows(self, dtypes: Dict[str, int]) -> str:
        """Build data type rows for table."""
        rows = []
        for dtype, count in dtypes.items():
            rows.append(f"<tr><td>{dtype}</td><td>{count}</td></tr>")
        return "\n".join(rows)
    
    def _build_data_quality_section(self, profile: Dict[str, Any]) -> str:
        """Build data quality section."""
        missing = profile.get('missing_values', {})
        duplicates = profile.get('duplicates', {})
        
        return f"""
    <section class="section">
        <h2>Data Quality Assessment</h2>
        
        <h3>Missing Values</h3>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Total Missing</div>
                <div class="metric-value">{missing.get('total_missing_cells', 0):,}</div>
                <div class="metric-description">{missing.get('missing_percentage', 0):.2f}% of all cells</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Affected Columns</div>
                <div class="metric-value">{missing.get('columns_with_missing_count', 0)}</div>
                <div class="metric-description">Columns with missing data</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Affected Rows</div>
                <div class="metric-value">{missing.get('rows_with_missing', 0):,}</div>
                <div class="metric-description">{missing.get('rows_with_missing_percentage', 0):.2f}% of rows</div>
            </div>
        </div>
        
        <h3>Duplicate Records</h3>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Duplicate Rows</div>
                <div class="metric-value">{duplicates.get('duplicate_rows', 0):,}</div>
                <div class="metric-description">{duplicates.get('duplicate_percentage', 0):.2f}% of total</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Unique Rows</div>
                <div class="metric-value">{duplicates.get('unique_rows', 0):,}</div>
                <div class="metric-description">Distinct records</div>
            </div>
        </div>
    </section>
"""
    
    def _build_column_profiles(self, profile: Dict[str, Any]) -> str:
        """Build column profiles section."""
        columns = profile.get('columns', {})
        
        if not columns:
            return ""
        
        column_html = []
        for col_name, col_profile in columns.items():
            column_html.append(self._build_single_column_profile(col_name, col_profile))
        
        return f"""
    <section class="section">
        <h2>Column Profiles</h2>
        {''.join(column_html)}
    </section>
"""
    
    def _build_single_column_profile(self, col_name: str, col_profile: Dict[str, Any]) -> str:
        """Build profile for a single column."""
        col_type = col_profile.get('type', 'unknown')
        
        stats_html = []
        
        # Common stats
        stats_html.append(f'<div class="stat-item"><span class="stat-label">Type:</span> <span class="stat-value">{col_profile.get("dtype", "N/A")}</span></div>')
        stats_html.append(f'<div class="stat-item"><span class="stat-label">Non-Null:</span> <span class="stat-value">{col_profile.get("non_null_count", 0):,}</span></div>')
        stats_html.append(f'<div class="stat-item"><span class="stat-label">Missing:</span> <span class="stat-value">{col_profile.get("null_percentage", 0):.1f}%</span></div>')
        stats_html.append(f'<div class="stat-item"><span class="stat-label">Unique:</span> <span class="stat-value">{col_profile.get("unique_count", 0):,}</span></div>')
        
        # Type-specific stats
        if col_type == 'numeric':
            stats_html.append(f'<div class="stat-item"><span class="stat-label">Mean:</span> <span class="stat-value">{col_profile.get("mean", 0):.2f}</span></div>')
            stats_html.append(f'<div class="stat-item"><span class="stat-label">Std Dev:</span> <span class="stat-value">{col_profile.get("std", 0):.2f}</span></div>')
            stats_html.append(f'<div class="stat-item"><span class="stat-label">Min:</span> <span class="stat-value">{col_profile.get("min", 0):.2f}</span></div>')
            stats_html.append(f'<div class="stat-item"><span class="stat-label">Max:</span> <span class="stat-value">{col_profile.get("max", 0):.2f}</span></div>')
            stats_html.append(f'<div class="stat-item"><span class="stat-label">Outliers:</span> <span class="stat-value">{col_profile.get("outlier_percentage", 0):.1f}%</span></div>')
        elif col_type == 'text':
            stats_html.append(f'<div class="stat-item"><span class="stat-label">Min Length:</span> <span class="stat-value">{col_profile.get("min_length", 0)}</span></div>')
            stats_html.append(f'<div class="stat-item"><span class="stat-label">Max Length:</span> <span class="stat-value">{col_profile.get("max_length", 0)}</span></div>')
            stats_html.append(f'<div class="stat-item"><span class="stat-label">Avg Length:</span> <span class="stat-value">{col_profile.get("mean_length", 0):.1f}</span></div>')
        
        return f"""
        <div class="column-profile">
            <div class="column-name">{col_name}</div>
            <div class="column-stats">
                {''.join(stats_html)}
            </div>
        </div>
"""
    
    def _build_visualizations_section(self, charts: List[Any]) -> str:
        """Build visualizations section with embedded charts."""
        if not charts:
            return ""
        
        chart_htmls = []
        for idx, fig in enumerate(charts):
            chart_id = f"chart_{idx}"
            chart_json = fig.to_json()
            
            chart_htmls.append(f"""
        <div class="chart-container">
            <div class="chart-title">Chart {idx + 1}</div>
            <div id="{chart_id}"></div>
            <script>
                Plotly.newPlot('{chart_id}', {chart_json});
            </script>
        </div>
""")
        
        return f"""
    <section class="section">
        <h2>Visualizations</h2>
        {''.join(chart_htmls)}
    </section>
"""
    
    def _build_analysis_results_section(self, analysis_results: Dict[str, Any]) -> str:
        """Build analysis results section."""
        if not analysis_results:
            return ""
        
        results_html = []
        for analysis_name, results in analysis_results.items():
            results_html.append(f"""
        <div class="column-profile">
            <div class="column-name">{analysis_name.replace('_', ' ').title()}</div>
            <pre style="background: #f5f5f5; padding: 15px; border-radius: 4px; overflow-x: auto;">{json.dumps(results, indent=2)}</pre>
        </div>
""")
        
        return f"""
    <section class="section">
        <h2>Analysis Results</h2>
        {''.join(results_html)}
    </section>
"""
    
    def _build_footer(self) -> str:
        """Build report footer."""
        return f"""
    <footer>
        <p>Generated by FastReports Data Analysis Pipeline</p>
        <p class="timestamp">Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </footer>
"""
    
    def _get_scripts(self) -> str:
        """Get JavaScript for interactivity."""
        return """
    <script>
        // Make charts responsive
        window.addEventListener('resize', function() {
            var charts = document.querySelectorAll('[id^="chart_"]');
            charts.forEach(function(chart) {
                Plotly.Plots.resize(chart);
            });
        });
        
        // Print functionality
        function printReport() {
            window.print();
        }
    </script>
"""


# Made with Bob