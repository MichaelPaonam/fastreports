# FastReports — Demo Script
### 4–5 minute video walkthrough

---

## Setup (before recording)

```bash
./start_all.sh          # start API on :8000 and dashboard on :3000
```

Have ready in separate terminal tabs:
- The project root (for CLI demo)
- `output/reports/layoffs_report.html` pre-generated and ready to open

---

## [0:00 – 0:30] Hook

> "Every data project starts the same way — load the data, profile it, clean it, analyse it, make some charts, write a report. It's the same 6 hours of work every time. FastReports does all of that in one command."

Show the terminal. Run:

```bash
python main.py data/layoffs/layoffs.csv --auto-clean
```

Watch the phases tick by live. Point out:

> "Eight phases — ingestion, profiling, quality check, cleaning, analysis, EDA, visualizations, HTML report. Done in under half a second."

Highlight the clickable link at the end:

```
HTML Report: output/reports/layoffs_report.html
```

---

## [0:30 – 1:30] HTML Report

Open `output/reports/layoffs_report.html` in the browser.

Scroll through slowly:

> "This is a fully self-contained HTML file — no server needed, share it anywhere."

Point out each section:

- **Table of contents** — jump to any section
- **Executive Summary** — rows, columns, quality badge, memory usage
- **Data Quality** — missing value bars per column, duplicate count
- **Column Profiles** — type badge, stats per column, numeric vs text
- **Visualizations** — Plotly charts embedded and interactive, hover to explore
- **Analysis Results** — correlations table, descriptive stats, distribution shapes

> "The quality score went from 74 before cleaning to 91.8 after. FastReports detected the issues, generated the cleaning strategies, applied them, then validated the result — all automatically."

---

## [1:30 – 2:30] Dashboard — Data Table

Switch to browser tab with `http://localhost:3000`.

Select **Layoffs** from the dropdown.

> "The dashboard connects to the same API and loads the data live."

Point out the stats bar: 2,361 rows, 9 columns, quality score 100.

**Demo filtering:**

- Type `United States` in the country filter → rows drop
- Set `total_laid_off` Min to `500` → rows drop further
- Point out Filtered Rows counter updating in real time

> "Every filter updates instantly — no page reload, no server round-trip for the filtering itself."

Clear filters.

---

## [2:30 – 3:15] Dashboard — SQL Query

Click **Show SQL Query**.

Type:

```sql
SELECT industry, SUM(total_laid_off) as total, COUNT(*) as companies
FROM data
GROUP BY industry
ORDER BY total DESC
LIMIT 10
```

Press **Ctrl+Enter** (or click Execute Query).

> "Full DuckDB SQL — aggregations, joins, anything. The query panel stays open so you can iterate."

Point out: columns update to match the query result, filter panel adapts.

---

## [3:15 – 4:00] Dashboard — Visualizations

Click the **Visualizations** tab.

> "Charts update dynamically based on whatever data is currently loaded — including query results."

Walk through a couple of changes:

1. Change Chart Type to **Bar Chart**, X-Axis to `industry` — instant count by industry
2. Change to **Pie Chart**, X-Axis to `stage` — funding stage distribution
3. Change to **Histogram**, X-Axis to `total_laid_off` — distribution of layoff sizes

> "Six chart types, all interactive Plotly — zoom, hover, export. The Y-axis auto-selects numeric columns."

---

## [4:00 – 4:30] Bob Integration + Wrap-up

Back to terminal. Show the Bob session log:

```bash
cat bob_sessions/layoffs_*.json | python -m json.tool | head -60
```

> "Every phase logs its Bob interaction — the prompt sent, the response received, success or failure. This is how we track exactly where Bob contributed throughout the pipeline."

Final line:

> "FastReports: drop in any dataset, get a complete analysis. One command for the CLI, one URL for the API, one browser tab for the dashboard. Built with IBM Bob from day one."

---

## Timing Reference

| Segment | Time | Duration |
|---|---|---|
| Hook + CLI run | 0:00 | 30s |
| HTML report walkthrough | 0:30 | 60s |
| Dashboard filtering | 1:30 | 60s |
| SQL query demo | 2:30 | 45s |
| Visualizations | 3:15 | 45s |
| Bob logs + wrap-up | 4:00 | 30s |
| **Total** | | **~4:30** |

---

## Fallback (if live demo breaks)

- HTML report is pre-generated at `output/reports/layoffs_report.html` — open directly
- Dashboard: use **Load Demo Data** button if API is down — uses mock data, all features still work
- CLI error: show the pre-recorded output in `output/logs/`
