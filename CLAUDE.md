# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastReports is an automated data analysis pipeline (Python 3.10+ backend, Preact frontend) that transforms raw data into insights through a 7-phase workflow: ingestion → profiling → quality check → cleaning → analysis → visualization → report generation.

## Commands

### Running the Application

```bash
# Full stack (API + Dashboard)
./start_all.sh

# API server only (http://localhost:8000, docs at /docs)
./start_server.sh

# CLI pipeline
python main.py                                            # Default: layoffs dataset
python main.py data/soccer/laliga_22_23.csv --auto-clean  # With auto-cleaning
python main.py --no-viz                                   # Skip visualizations
```

### Testing

```bash
pytest tests/                    # Full suite (verbose, short traceback by default via pytest.ini)
pytest tests/ --cov=src          # With coverage
pytest tests/test_ingestion.py   # Single module
pytest -m unit                   # By marker: unit, integration, slow, performance
```

### Code Quality

```bash
black src/ tests/                # Format
flake8 src/ tests/               # Lint
mypy src/                        # Type check
```

### Frontend (dashboard/)

```bash
cd dashboard
npm install
npm run dev      # Dev server on http://localhost:3000
npm run build    # Production build
npm run lint     # ESLint
```

## Architecture

**Three deployment modes:** CLI (`main.py`), API server (`api_server.py` via FastAPI+DuckDB), or full-stack (`start_all.sh` runs both API and Preact dashboard).

### Backend (`src/`)

The pipeline is orchestrated by `src/orchestration/pipeline.py` (`DataAnalysisPipeline.run_pipeline()`), which sequences these modules:

- **ingestion/** - Auto-detects format (CSV/XLSX/JSON/Parquet), loads data, creates working copies in `processed_data/`
- **profiling/** - Statistical profiling and quality scoring (0-100 scale)
- **cleaning/** - Strategy generation → transformation → validation. Strategies configured in `config.yaml`
- **analysis/** - EDA, statistical tests, time series, domain-specific analyzers (transaction, sentiment via NLTK/TextBlob)
- **visualization/** - Chart generation (9+ types via Plotly), smart recommendations via `recommender.py`
- **reporting/** - Static HTML report generation
- **bob_integration/** - Session management, prompt templates, response parsing for IBM Bob
- **orchestration/** - Pipeline sequencing, checkpoint/approval system, progress tracking

### Frontend (`dashboard/`)

Preact app (Vite build) with components: DataTable, ChartViewer, FilterPanel. Uses DuckDB-WASM for client-side SQL queries and Plotly.js for charts. Connects to the API at `http://localhost:8000`.

### Data Flow

- Original data stays read-only in `data/`
- Working copies go to `processed_data/{dataset_name}/`
- Outputs (reports, logs, visualizations) go to `output/`
- Bob interaction logs stored as JSON in `bob_sessions/`

## Configuration

`config.yaml` controls all pipeline behavior: quality thresholds, cleaning strategies, analysis parameters, visualization settings, checkpoint behavior, and Bob integration. Key settings:

- `checkpoints.auto_approve: false` — pipeline pauses for user approval between phases
- `quality.missing_value_threshold: 0.5` — triggers cleaning if >50% missing
- `cleaning.missing_value_strategy` — `median` for numeric, `mode` for categorical

## Key Entry Points

| Purpose | File | Notes |
|---------|------|-------|
| CLI | `main.py` | argparse, returns 0/1 |
| API | `api_server.py` | FastAPI, endpoints: `/api/datasets`, `/api/data`, `/api/query`, `/api/profile` |
| Pipeline | `src/orchestration/pipeline.py` | Core orchestrator class |
| Dashboard | `dashboard/src/App.jsx` | Main Preact component |

## Sample Datasets

Three datasets in `data/` for testing different pipeline capabilities:
- **layoffs/** — Tech layoffs (missing values, inconsistent formats) — default dataset
- **soccer/** — La Liga seasons (time-series, 100+ columns, clean)
- **pizza_delivery_app/** — Excel files (surveys, reviews, transactions — NLP-suitable)
