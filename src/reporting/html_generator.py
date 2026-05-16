"""
HTML Report Generator Module
Generates static HTML reports with embedded visualizations
"""

import math
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json
from src.utils.logger import get_logger
from src.visualization.plotly_charts import PlotlyChartBuilder

logger = get_logger(__name__)


def _safe_json(obj: Any) -> Any:
    """Recursively convert non-serializable types so json.dumps never raises."""
    if isinstance(obj, dict):
        return {k: _safe_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_safe_json(v) for v in obj]
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        v = float(obj)
        return None if math.isnan(v) or math.isinf(v) else v
    if isinstance(obj, np.ndarray):
        return _safe_json(obj.tolist())
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    return obj


def _fmt(value: Any, decimals: int = 2) -> str:
    """Format a number for display, returning '-' for None/NaN."""
    if value is None:
        return "-"
    try:
        f = float(value)
    except (TypeError, ValueError):
        return str(value)
    if math.isnan(f) or math.isinf(f):
        return "-"
    return f"{f:,.{decimals}f}"


class HTMLReportGenerator:
    """Generates comprehensive HTML reports with embedded visualizations."""

    def __init__(self):
        self.chart_builder = PlotlyChartBuilder()
        self.template_dir = Path(__file__).parent / "templates"

    def generate_report(
        self,
        profile: Dict[str, Any],
        charts: Optional[List[Any]] = None,
        analysis_results: Optional[Dict[str, Any]] = None,
        output_path: str = "report.html",
    ) -> str:
        logger.info(f"Generating HTML report: {output_path}")

        html_content = self._build_html(
            profile=profile,
            charts=charts or [],
            analysis_results=analysis_results or {},
        )

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html_content, encoding="utf-8")

        logger.info(f"Report generated successfully: {output_path}")
        return str(output_file)

    # ------------------------------------------------------------------
    # Top-level structure
    # ------------------------------------------------------------------

    def _build_html(
        self,
        profile: Dict[str, Any],
        charts: List[Any],
        analysis_results: Dict[str, Any],
    ) -> str:
        dataset_name = profile.get("dataset_name", "Dataset")
        sections = [
            ("executive-summary", "Executive Summary"),
            ("data-overview", "Data Overview"),
            ("data-quality", "Data Quality"),
            ("column-profiles", "Column Profiles"),
        ]
        if charts:
            sections.append(("visualizations", "Visualizations"))
        if analysis_results:
            sections.append(("analysis-results", "Analysis Results"))

        toc_items = "\n".join(
            f'<li><a href="#{anchor}">{label}</a></li>'
            for anchor, label in sections
        )

        body_sections = "\n".join([
            self._build_executive_summary(profile),
            self._build_data_overview(profile),
            self._build_data_quality_section(profile),
            self._build_column_profiles(profile),
            self._build_visualizations_section(charts),
            self._build_analysis_results_section(analysis_results),
        ])

        chart_scripts = self._collect_chart_scripts(charts)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Analysis Report — {dataset_name}</title>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js" defer></script>
    {self._get_styles()}
</head>
<body>
    <div class="container">
        {self._build_header(profile)}
        <nav class="toc">
            <strong>Contents</strong>
            <ol>{toc_items}</ol>
        </nav>
        {body_sections}
        {self._build_footer()}
    </div>
    <script>
        window.addEventListener('DOMContentLoaded', function() {{
            {chart_scripts}
            window.addEventListener('resize', function() {{
                document.querySelectorAll('[id^="chart_"]').forEach(function(el) {{
                    Plotly.Plots.resize(el);
                }});
            }});
        }});
    </script>
</body>
</html>"""

    # ------------------------------------------------------------------
    # Chart scripts collected into one deferred block
    # ------------------------------------------------------------------

    def _collect_chart_scripts(self, charts: List[Any]) -> str:
        lines = []
        for idx, fig in enumerate(charts):
            chart_id = f"chart_{idx}"
            try:
                chart_json = fig.to_json()
                parsed = json.loads(chart_json)
                data_json = json.dumps(parsed.get("data", []))
                layout_json = json.dumps(parsed.get("layout", {}))
                lines.append(
                    f"Plotly.newPlot('{chart_id}', {data_json}, "
                    f"Object.assign({{}}, {layout_json}, {{responsive: true}}));"
                )
            except Exception as exc:
                logger.warning(f"Could not serialize chart {idx}: {exc}")
        return "\n            ".join(lines)

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _build_header(self, profile: Dict[str, Any]) -> str:
        dataset_name = profile.get("dataset_name", "Dataset")
        timestamp = profile.get("timestamp", datetime.now().isoformat())
        return f"""
    <header>
        <h1>Data Analysis Report</h1>
        <p class="subtitle">{dataset_name}</p>
        <p class="timestamp">Generated: {timestamp}</p>
    </header>"""

    def _build_executive_summary(self, profile: Dict[str, Any]) -> str:
        overview = profile.get("overview", {})
        missing = profile.get("missing_values", {})
        duplicates = profile.get("duplicates", {})

        missing_pct = missing.get("missing_percentage", 0) or 0
        duplicate_pct = duplicates.get("duplicate_percentage", 0) or 0
        quality_score = profile.get("quality_score", None)

        if missing_pct < 5 and duplicate_pct < 1:
            badge_cls, badge_text = "status-good", "Excellent"
        elif missing_pct < 15 and duplicate_pct < 5:
            badge_cls, badge_text = "status-warning", "Good"
        else:
            badge_cls, badge_text = "status-error", "Needs Attention"

        score_html = ""
        if quality_score is not None:
            score_color = "#155724" if quality_score >= 80 else ("#856404" if quality_score >= 60 else "#721c24")
            score_html = f"""
            <div class="metric-card">
                <div class="metric-label">Quality Score</div>
                <div class="metric-value" style="color:{score_color}">{_fmt(quality_score, 0)}</div>
                <div class="metric-description">out of 100</div>
            </div>"""

        return f"""
    <section class="section" id="executive-summary">
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
                <div class="metric-value"><span class="status-badge {badge_cls}">{badge_text}</span></div>
                <div class="metric-description">{missing_pct:.1f}% missing, {duplicate_pct:.1f}% duplicates</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Memory Usage</div>
                <div class="metric-value">{_fmt(profile.get('memory', {}).get('total_mb', 0), 1)} MB</div>
                <div class="metric-description">Total size</div>
            </div>
            {score_html}
        </div>
    </section>"""

    def _build_data_overview(self, profile: Dict[str, Any]) -> str:
        overview = profile.get("overview", {})
        dtypes = overview.get("dtypes_summary", {})
        dtype_rows = "\n".join(
            f"<tr><td>{dtype}</td><td>{count}</td></tr>"
            for dtype, count in dtypes.items()
        )
        return f"""
    <section class="section" id="data-overview">
        <h2>Data Overview</h2>
        <table>
            <thead><tr><th>Metric</th><th>Value</th></tr></thead>
            <tbody>
                <tr><td>Total Rows</td><td>{overview.get('rows', 0):,}</td></tr>
                <tr><td>Total Columns</td><td>{overview.get('columns', 0)}</td></tr>
                <tr><td>Total Cells</td><td>{overview.get('total_cells', 0):,}</td></tr>
                <tr><td>Memory Usage</td><td>{_fmt(profile.get('memory', {}).get('total_mb', 0))} MB</td></tr>
            </tbody>
        </table>
        {f'<h3>Column Types</h3><table><thead><tr><th>Data Type</th><th>Count</th></tr></thead><tbody>{dtype_rows}</tbody></table>' if dtypes else ''}
    </section>"""

    def _build_data_quality_section(self, profile: Dict[str, Any]) -> str:
        missing = profile.get("missing_values", {})
        duplicates = profile.get("duplicates", {})

        # Per-column missing table
        col_missing = missing.get("missing_per_column", {})
        col_rows = ""
        if col_missing:
            rows = []
            for col, info in col_missing.items():
                count = info if isinstance(info, (int, float)) else info.get("count", 0)
                pct = info.get("percentage", 0) if isinstance(info, dict) else 0
                bar_width = min(100, max(0, pct))
                rows.append(
                    f"<tr><td>{col}</td><td>{int(count):,}</td><td>"
                    f'<div class="bar-bg"><div class="bar-fill" style="width:{bar_width:.1f}%"></div></div>'
                    f"{pct:.1f}%</td></tr>"
                )
            col_rows = f"""
        <h3>Missing Values by Column</h3>
        <table>
            <thead><tr><th>Column</th><th>Missing</th><th>Percentage</th></tr></thead>
            <tbody>{"".join(rows)}</tbody>
        </table>"""

        return f"""
    <section class="section" id="data-quality">
        <h2>Data Quality Assessment</h2>
        <h3>Missing Values</h3>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Total Missing</div>
                <div class="metric-value">{missing.get('total_missing_cells', 0):,}</div>
                <div class="metric-description">{_fmt(missing.get('missing_percentage', 0))}% of all cells</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Affected Columns</div>
                <div class="metric-value">{missing.get('columns_with_missing_count', 0)}</div>
                <div class="metric-description">Columns with missing data</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Affected Rows</div>
                <div class="metric-value">{missing.get('rows_with_missing', 0):,}</div>
                <div class="metric-description">{_fmt(missing.get('rows_with_missing_percentage', 0))}% of rows</div>
            </div>
        </div>
        {col_rows}
        <h3>Duplicate Records</h3>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Duplicate Rows</div>
                <div class="metric-value">{duplicates.get('duplicate_rows', 0):,}</div>
                <div class="metric-description">{_fmt(duplicates.get('duplicate_percentage', 0))}% of total</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Unique Rows</div>
                <div class="metric-value">{duplicates.get('unique_rows', 0):,}</div>
                <div class="metric-description">Distinct records</div>
            </div>
        </div>
    </section>"""

    def _build_column_profiles(self, profile: Dict[str, Any]) -> str:
        columns = profile.get("columns", {})
        if not columns:
            return ""
        profiles_html = "".join(
            self._build_single_column_profile(name, col)
            for name, col in columns.items()
        )
        return f"""
    <section class="section" id="column-profiles">
        <h2>Column Profiles</h2>
        {profiles_html}
    </section>"""

    def _build_single_column_profile(self, col_name: str, col_profile: Dict[str, Any]) -> str:
        col_type = col_profile.get("type", "unknown")

        def stat(label: str, key: str, decimals: int = 2) -> str:
            return (
                f'<div class="stat-item">'
                f'<span class="stat-label">{label}</span>'
                f'<span class="stat-value">{_fmt(col_profile.get(key), decimals)}</span>'
                f"</div>"
            )

        def stat_raw(label: str, value: Any) -> str:
            return (
                f'<div class="stat-item">'
                f'<span class="stat-label">{label}</span>'
                f'<span class="stat-value">{value if value is not None else "-"}</span>'
                f"</div>"
            )

        stats = [
            stat_raw("Type", col_profile.get("dtype", "N/A")),
            stat_raw("Non-Null", f"{col_profile.get('non_null_count', 0):,}"),
            stat("Missing", "null_percentage", 1),
            stat_raw("Unique", f"{col_profile.get('unique_count', 0):,}"),
        ]

        if col_type == "numeric":
            stats += [
                stat("Mean", "mean"),
                stat("Std Dev", "std"),
                stat("Min", "min"),
                stat("Max", "max"),
                stat("Outliers", "outlier_percentage", 1),
            ]
        elif col_type == "text":
            stats += [
                stat("Min Length", "min_length", 0),
                stat("Max Length", "max_length", 0),
                stat("Avg Length", "mean_length", 1),
            ]

        return f"""
        <div class="column-profile">
            <div class="column-name">{col_name} <span class="col-type-badge">{col_type}</span></div>
            <div class="column-stats">{"".join(stats)}</div>
        </div>"""

    def _build_visualizations_section(self, charts: List[Any]) -> str:
        if not charts:
            return ""
        chart_divs = []
        for idx, fig in enumerate(charts):
            chart_id = f"chart_{idx}"
            # Use Plotly figure title if available
            title = ""
            try:
                title = fig.layout.title.text or f"Chart {idx + 1}"
            except Exception:
                title = f"Chart {idx + 1}"
            chart_divs.append(f"""
        <div class="chart-container">
            <div class="chart-title">{title}</div>
            <div id="{chart_id}"></div>
        </div>""")
        return f"""
    <section class="section" id="visualizations">
        <h2>Visualizations</h2>
        {"".join(chart_divs)}
    </section>"""

    def _build_analysis_results_section(self, analysis_results: Dict[str, Any]) -> str:
        if not analysis_results:
            return ""
        blocks = []
        for name, results in analysis_results.items():
            title = name.replace("_", " ").title()
            blocks.append(f"""
        <div class="column-profile">
            <div class="column-name">{title}</div>
            {self._render_analysis_block(name, results)}
        </div>""")
        return f"""
    <section class="section" id="analysis-results">
        <h2>Analysis Results</h2>
        {"".join(blocks)}
    </section>"""

    def _render_analysis_block(self, name: str, results: Any) -> str:
        """Render a known analysis result type as a table; fall back to formatted JSON."""
        if not isinstance(results, dict):
            safe = _safe_json(results)
            return f'<pre class="json-block">{json.dumps(safe, indent=2)}</pre>'

        # Strong correlations list
        if "strong_correlations" in results:
            return self._render_correlations(results)

        # Descriptive statistics with numeric_columns/categorical_columns
        if "numeric_columns" in results or "categorical_columns" in results:
            return self._render_descriptive_stats(results)

        # Distribution analysis
        if "distributions" in results:
            return self._render_distributions(results)

        # Generic dict: render as a two-column table of key/value pairs
        if all(not isinstance(v, (dict, list)) for v in results.values()):
            rows = "".join(
                f"<tr><td>{k}</td><td>{_fmt(v) if isinstance(v, float) else v}</td></tr>"
                for k, v in results.items()
            )
            return f"<table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>{rows}</tbody></table>"

        # Nested: fall back to safe JSON
        safe = _safe_json(results)
        return f'<pre class="json-block">{json.dumps(safe, indent=2)}</pre>'

    def _render_correlations(self, results: Dict[str, Any]) -> str:
        strong = results.get("strong_correlations", [])
        count = results.get("num_strong_correlations", len(strong))
        if not strong:
            msg = results.get("message", "No strong correlations found.")
            return f"<p>{msg}</p>"
        rows = "".join(
            f"<tr><td>{c['variable1']}</td><td>{c['variable2']}</td>"
            f"<td>{_fmt(c['correlation'])}</td><td>{c.get('strength', '')}</td></tr>"
            for c in strong
        )
        return f"""
        <p>{count} strong correlation(s) found (|r| &gt; 0.7)</p>
        <table>
            <thead><tr><th>Variable 1</th><th>Variable 2</th><th>r</th><th>Direction</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>"""

    def _render_descriptive_stats(self, results: Dict[str, Any]) -> str:
        parts = []
        numeric = results.get("numeric_columns", {})
        if numeric:
            rows = "".join(
                f"<tr><td>{col}</td><td>{_fmt(s.get('mean'))}</td>"
                f"<td>{_fmt(s.get('std'))}</td><td>{_fmt(s.get('min'))}</td>"
                f"<td>{_fmt(s.get('max'))}</td></tr>"
                for col, s in numeric.items()
            )
            parts.append(f"""
        <h4>Numeric Columns</h4>
        <table>
            <thead><tr><th>Column</th><th>Mean</th><th>Std</th><th>Min</th><th>Max</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>""")
        categorical = results.get("categorical_columns", {})
        if categorical:
            rows = "".join(
                f"<tr><td>{col}</td><td>{s.get('unique', '-')}</td>"
                f"<td>{s.get('top', '-')}</td><td>{s.get('freq', '-')}</td></tr>"
                for col, s in categorical.items()
            )
            parts.append(f"""
        <h4>Categorical Columns</h4>
        <table>
            <thead><tr><th>Column</th><th>Unique</th><th>Most Common</th><th>Frequency</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>""")
        return "".join(parts)

    def _render_distributions(self, results: Dict[str, Any]) -> str:
        dists = results.get("distributions", {})
        rows = "".join(
            f"<tr><td>{col}</td><td>{info.get('shape', '-')}</td>"
            f"<td>{_fmt(info.get('skewness'))}</td><td>{_fmt(info.get('kurtosis'))}</td></tr>"
            for col, info in dists.items()
            if isinstance(info, dict)
        )
        return f"""
        <table>
            <thead><tr><th>Column</th><th>Shape</th><th>Skewness</th><th>Kurtosis</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>"""

    def _build_footer(self) -> str:
        return f"""
    <footer>
        <p>Generated by FastReports Data Analysis Pipeline</p>
        <p class="timestamp">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </footer>"""

    # ------------------------------------------------------------------
    # Styles
    # ------------------------------------------------------------------

    def _get_styles(self) -> str:
        return """
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,.1);
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 8px;
            margin-bottom: 24px;
        }
        header h1 { font-size: 2.2em; margin-bottom: 8px; }
        header .subtitle { font-size: 1.2em; opacity: .9; }
        header .timestamp { font-size: .85em; opacity: .7; margin-top: 6px; }

        /* Table of contents */
        .toc {
            background: #f0f4ff;
            border-left: 4px solid #667eea;
            padding: 16px 20px;
            border-radius: 6px;
            margin-bottom: 32px;
        }
        .toc strong { display: block; margin-bottom: 8px; color: #667eea; }
        .toc ol { padding-left: 20px; }
        .toc a { color: #667eea; text-decoration: none; }
        .toc a:hover { text-decoration: underline; }

        h2 {
            color: #667eea;
            margin: 0 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
            font-size: 1.5em;
        }
        h3 { color: #764ba2; margin: 20px 0 10px; font-size: 1.1em; }
        h4 { color: #555; margin: 14px 0 8px; font-size: 1em; }

        .section {
            margin-bottom: 40px;
            padding: 24px;
            background: #f9f9f9;
            border-radius: 8px;
        }

        /* Metric cards */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin: 16px 0;
        }
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,.08);
            border-left: 4px solid #667eea;
        }
        .metric-label { font-size: .8em; color: #888; text-transform: uppercase; letter-spacing: .5px; }
        .metric-value { font-size: 1.8em; font-weight: 700; color: #333; margin: 8px 0 4px; }
        .metric-description { font-size: .82em; color: #999; }

        /* Status badges */
        .status-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: .82em;
            font-weight: 600;
        }
        .status-good    { background: #d4edda; color: #155724; }
        .status-warning { background: #fff3cd; color: #856404; }
        .status-error   { background: #f8d7da; color: #721c24; }

        /* Column type badge */
        .col-type-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: .72em;
            font-weight: 500;
            background: #e9d8fd;
            color: #553c9a;
            margin-left: 8px;
            vertical-align: middle;
        }

        /* Tables */
        table { width: 100%; border-collapse: collapse; margin: 12px 0; background: white; }
        th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #667eea; color: white; font-weight: 600; font-size: .9em; }
        tr:hover td { background: #f5f5f5; }

        /* Missing-value progress bar */
        .bar-bg {
            display: inline-block;
            width: 80px;
            height: 8px;
            background: #eee;
            border-radius: 4px;
            margin-right: 6px;
            vertical-align: middle;
        }
        .bar-fill {
            height: 100%;
            background: #667eea;
            border-radius: 4px;
        }

        /* Chart containers — no inline scripts */
        .chart-container {
            margin: 24px 0;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,.08);
        }
        .chart-title { font-size: 1.05em; font-weight: 600; color: #444; margin-bottom: 12px; }
        .chart-container > div[id^="chart_"] { min-height: 400px; }

        /* Column profile cards */
        .column-profile {
            background: white;
            padding: 16px;
            margin: 12px 0;
            border-radius: 8px;
            border-left: 4px solid #764ba2;
        }
        .column-name { font-weight: 600; font-size: 1.05em; color: #333; margin-bottom: 10px; }
        .column-stats {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 8px;
            margin-top: 8px;
        }
        .stat-item { padding: 8px; background: #f9f9f9; border-radius: 4px; }
        .stat-label { display: block; font-size: .78em; color: #888; margin-bottom: 2px; }
        .stat-value { font-weight: 600; color: #333; font-size: .95em; }

        /* Analysis results fallback */
        .json-block {
            background: #f5f5f5;
            padding: 14px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: .82em;
            line-height: 1.5;
        }

        footer {
            margin-top: 48px;
            padding: 20px;
            text-align: center;
            color: #999;
            border-top: 1px solid #eee;
            font-size: .88em;
        }

        @media print {
            body { background: white; }
            .container { box-shadow: none; }
            .chart-container, .section { page-break-inside: avoid; }
            .toc { display: none; }
        }
    </style>"""


# Made with Bob
