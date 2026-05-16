# FastReports
## Automated Data Analysis Pipeline
### IBM Bob Integration Hackathon

---

## The Problem

Raw data → insight is **slow and manual**

- Data engineers spend hours on repetitive profiling, cleaning, and visualization
- Each dataset requires custom code
- No consistency across analyses
- Reports are one-offs with no interactivity

---

## The Solution: FastReports

> Drop in any dataset. Get a complete analysis in seconds.

A 7-phase automated pipeline that transforms raw data into interactive insights — powered by IBM Bob throughout.

---

## How It Works

```
Raw Data
   ↓  Ingestion      — CSV, XLSX, JSON, Parquet auto-detected
   ↓  Profiling      — statistical fingerprint, quality score
   ↓  Quality Check  — missing values, duplicates, outliers
   ↓  Cleaning       — auto-generated strategies, applied & validated
   ↓  Analysis       — EDA, statistics, correlations, time series
   ↓  Visualization  — 9+ chart types, smart recommendations
   ↓  Report         — self-contained HTML with embedded charts
```

---

## IBM Bob Integration

Bob is used **at every phase**, not just as a chatbot:

| Phase | Bob's Role |
|---|---|
| Pipeline planning | Generates execution strategy |
| Cleaning | Recommends strategies per column type |
| EDA | Interprets findings, writes narrative |
| Visualization | Recommends chart types for the data |
| Reporting | Structures the final report |

All interactions logged to `bob_sessions/` as JSON.

---

## Three Ways to Use It

**CLI** — one command, full pipeline
```bash
python main.py data/layoffs/layoffs.csv --auto-clean
```

**API** — FastAPI + DuckDB, OpenAPI docs at `/docs`
```bash
./start_server.sh
```

**Dashboard** — interactive Preact UI with live filtering + SQL
```bash
./start_all.sh
```

---

## Live Demo: Layoffs Dataset

- **2,361 rows** × 9 columns
- Real-world data: missing values, inconsistent formats
- Quality score: **74/100** → auto-cleaned to **91.8/100**
- **11 visualizations** generated
- Full HTML report in **0.31 seconds**

---

## Dashboard Features

- Load any dataset from the API
- Filter across all columns simultaneously
- Run arbitrary **DuckDB SQL** queries
- Switch between table and chart views
- 6 chart types with dynamic axis selection
- Export filtered data as CSV

---

## The Numbers

| | |
|---|---|
| Backend | 9,269 lines across 33 Python modules |
| Frontend | 942 lines, 5 Preact components |
| Pipeline phases | 8 (including HTML report) |
| Chart types | 9+ |
| Sample datasets | 3 (layoffs, La Liga, pizza delivery) |
| Report generation | < 0.5 seconds |

---

## Tech Stack

**Backend:** Python 3.10+, FastAPI, DuckDB, Pandas, Plotly, NLTK/TextBlob, scikit-learn

**Frontend:** Preact, Vite, DuckDB-WASM, Plotly.js, Tailwind CSS

**AI:** IBM Bob — plan mode, code mode, error handling

---

## Key Takeaway

FastReports turns any dataset into a **production-quality analysis** in seconds — with Bob as the intelligence layer that makes every phase smarter.

```bash
python main.py your_data.csv --auto-clean
# → output/reports/your_data_report.html
```
