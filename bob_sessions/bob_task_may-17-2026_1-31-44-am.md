**User:**

<task>
What does the user flow look like for fastreports ?
</task>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
IMPLEMENTATION_STATUS.md,output/pizza_delivery_analysis.json

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T20:01:13.552Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>


# Current Workspace Directory (/Users/I329392/Lab/fastreports) Files
.gitignore
=5.2.0
API_DOCUMENTATION.md
api_server.py
ARCHITECTURE.md
BOB_USAGE_GUIDE.md
config.yaml
DATA_CLEANING_STRATEGIES.md
IMPLEMENTATION_PLAN.md
IMPLEMENTATION_STATUS.md
IMPLEMENTATION_SUMMARY.md
main.py
PLAN_SUMMARY.md
pytest.ini
README.md
requirements.txt
run_tests.py
SMOKE_TEST.md
start_all.sh
start_server.bat
start_server.sh
test_api.py
TEST_IMPLEMENTATION_SUMMARY.md
test_new_components.py
TEST_STATUS.md
TESTING.md
dashboard/
dashboard/index.html
dashboard/package.json
dashboard/README.md
dashboard/vite.config.js
dashboard/public/
dashboard/src/
dashboard/src/App.css
dashboard/src/App.jsx
dashboard/src/main.jsx
dashboard/src/style.css
dashboard/src/components/
dashboard/src/components/ChartViewer.css
dashboard/src/components/ChartViewer.jsx
dashboard/src/components/DataTable.css
dashboard/src/components/DataTable.jsx
dashboard/src/components/FilterPanel.css
dashboard/src/components/FilterPanel.jsx
data/
data/layoffs/
data/layoffs/layoffs.csv
data/pizza_delivery_app/
data/pizza_delivery_app/purchase_log.xlsx
data/pizza_delivery_app/survey_answers.xlsx
data/pizza_delivery_app/yelp_reviews.xlsx
data/soccer/
data/soccer/laliga_22_23.csv
data/soccer/laliga_23_24.csv
data/soccer/laliga_24_25.csv
data/soccer/laliga_25_26.csv
output/
output/pizza_delivery_analysis.json
output/test_report.html
src/
src/__init__.py
src/analysis/
src/analysis/__init__.py
src/analysis/eda.py
src/analysis/statistics.py
src/analysis/time_series_analyzer.py
src/analysis/transaction_analyzer.py
src/bob_integration/
src/bob_integration/__init__.py
src/bob_integration/prompt_templates.py
src/bob_integration/response_parser.py
src/bob_integration/session_manager.py
src/cleaning/
src/cleaning/__init__.py
src/cleaning/strategy_generator.py
src/cleaning/transformers.py
src/cleaning/validator.py
src/ingestion/
src/ingestion/__init__.py
src/ingestion/data_loader.py
src/ingestion/file_detector.py
src/orchestration/
src/orchestration/__init__.py
src/orchestration/checkpoint_manager.py
src/orchestration/pipeline.py
src/orchestration/progress_tracker.py
src/profiling/
src/profiling/__init__.py
src/profiling/profiler.py
src/profiling/quality_checker.py
src/reporting/
src/reporting/__init__.py
src/reporting/html_generator.py
src/utils/
src/utils/__init__.py
src/utils/config_loader.py
src/utils/logger.py
src/visualization/
src/visualization/__init__.py
src/visualization/chart_generator.py
src/visualization/plotly_charts.py
src/visualization/recommender.py
tests/
tests/__init__.py
tests/conftest.py
tests/test_cleaning.py
tests/test_ingestion.py
tests/test_integration.py
tests/test_profiling.py
tests/output/
tests/output/logs/
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll analyze the fastreports project to understand the user flow. Let me start by examining the key documentation and code files.

<read_file>
<args>
<file>
<path>README.md</path>
</file>
<file>
<path>ARCHITECTURE.md</path>
</file>
<file>
<path>API_DOCUMENTATION.md</path>
</file>
<file>
<path>main.py</path>
</file>
<file>
<path>api_server.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 5 files] Result:
<files>
<file><path>README.md</path>
<content lines="1-524">
  1 | # FastReports 🚀
  2 | 
  3 | **Automated Data Analysis Pipeline with IBM Bob Integration**
  4 | 
  5 | FastReports is an intelligent data analysis system that automates the entire workflow from raw data to actionable insights, leveraging IBM Bob as an AI development partner throughout the process.
  6 | 
  7 | ## 🎯 Project Overview
  8 | 
  9 | FastReports demonstrates meaningful IBM Bob integration by using AI assistance in every phase of the data analysis pipeline:
 10 | 
 11 | - **Data Ingestion**: Automatically detect and load various file formats
 12 | - **Data Profiling**: Analyze data characteristics and quality
 13 | - **Data Cleaning**: Generate and apply intelligent cleaning strategies
 14 | - **Statistical Analysis**: Perform comprehensive statistical tests
 15 | - **Visualization**: Create interactive charts with smart recommendations
 16 | - **Reporting**: Generate comprehensive analysis reports
 17 | 
 18 | ## 🏆 Hackathon Highlights
 19 | 
 20 | ### IBM Bob Integration Points
 21 | 
 22 | 1. **Architecture Design** (Plan Mode)
 23 |    - System architecture planning
 24 |    - Pipeline workflow design
 25 |    - Strategy recommendations
 26 | 
 27 | 2. **Code Generation** (Code Mode)
 28 |    - Module implementation
 29 |    - Function generation
 30 |    - Data transformations
 31 | 
 32 | 3. **Analysis Assistance** (Advanced Mode - Conceptual)
 33 |    - Statistical test selection
 34 |    - Insight generation
 35 |    - Complex queries
 36 | 
 37 | 4. **Session Tracking**
 38 |    - All Bob interactions logged
 39 |    - Usage analytics
 40 |    - Mode tracking
 41 |    - Export capabilities
 42 | 
 43 | ## 📋 Features
 44 | 
 45 | ### ✅ Implemented Core Features
 46 | 
 47 | - **Multi-format Data Loading**: CSV, XLSX, JSON, Parquet
 48 | - **Comprehensive Profiling**: Statistics, distributions, correlations
 49 | - **Quality Assessment**: Scoring system with issue detection
 50 | - **Automated Cleaning**: Multiple strategies (imputation, standardization, validation)
 51 | - **Statistical Analysis**: Descriptive stats, correlations, hypothesis testing
 52 | - **EDA Reports**: Key findings, recommendations, insights
 53 | - **Interactive Visualizations**: 9+ chart types with Plotly
 54 | - **Smart Recommendations**: AI-driven visualization suggestions
 55 | - **Pipeline Orchestration**: End-to-end workflow management
 56 | - **Bob Session Management**: Complete interaction tracking
 57 | - **REST API Backend**: FastAPI server with DuckDB query engine
 58 | - **Interactive Dashboard**: Preact-based web UI with real-time filtering
 59 | 
 60 | ## 🚀 Quick Start
 61 | 
 62 | ### Option 1: Full Stack (API + Dashboard)
 63 | 
 64 | ```bash
 65 | # Install Python dependencies
 66 | pip install -r requirements.txt
 67 | 
 68 | # Install dashboard dependencies
 69 | cd dashboard && npm install && cd ..
 70 | 
 71 | # Start both API server and dashboard
 72 | chmod +x start_all.sh
 73 | ./start_all.sh
 74 | 
 75 | # Access the dashboard at http://localhost:3000
 76 | # API documentation at http://localhost:8000/docs
 77 | ```
 78 | 
 79 | ### Option 2: API Server Only
 80 | 
 81 | ```bash
 82 | # Install dependencies
 83 | pip install -r requirements.txt
 84 | 
 85 | # Start API server
 86 | chmod +x start_server.sh
 87 | ./start_server.sh
 88 | 
 89 | # Or on Windows
 90 | start_server.bat
 91 | 
 92 | # API available at http://localhost:8000
 93 | ```
 94 | 
 95 | ### Option 3: Command-Line Pipeline
 96 | 
 97 | ### Prerequisites
 98 | 
 99 | ```bash
100 | # Python 3.10 or higher
101 | python --version
102 | 
103 | # Install dependencies
104 | pip install -r requirements.txt
105 | ```
106 | 
107 | ### Basic Usage
108 | 
109 | ```bash
110 | # Run with default dataset (layoffs)
111 | python main.py
112 | 
113 | # Run with specific dataset
114 | python main.py data/soccer/laliga_22_23.csv --dataset-name laliga
115 | 
116 | # Auto-clean data without prompts
117 | python main.py --auto-clean
118 | 
119 | # Skip visualization generation
120 | python main.py --no-viz
121 | ```
122 | 
123 | ### Command-Line Options
124 | 
125 | ```
126 | usage: main.py [-h] [--dataset-name DATASET_NAME] [--auto-clean] [--no-viz] [data_path]
127 | 
128 | positional arguments:
129 |   data_path             Path to the data file (default: data/layoffs/layoffs.csv)
130 | 
131 | optional arguments:
132 |   -h, --help            Show this help message and exit
133 |   --dataset-name DATASET_NAME
134 |                         Name of the dataset (default: layoffs)
135 |   --auto-clean          Automatically apply cleaning strategies
136 |   --no-viz              Skip visualization generation
137 | ```
138 | 
139 | ## 📊 Sample Datasets
140 | 
141 | The project includes three diverse datasets for demonstration:
142 | 
143 | 1. **Layoffs Dataset** (`data/layoffs/layoffs.csv`)
144 |    - Tech company layoffs data
145 |    - Mixed data types, missing values
146 |    - Good for demonstrating cleaning strategies
147 | 
148 | 2. **Soccer Dataset** (`data/soccer/laliga_*.csv`)
149 |    - La Liga match statistics
150 |    - Time series data, high dimensionality
151 |    - Good for trend analysis
152 | 
153 | 3. **Pizza Delivery** (`data/pizza_delivery_app/*.xlsx`)
154 |    - Customer surveys and transactions
155 |    - Multiple files, text data
156 |    - Good for sentiment analysis
157 | 
158 | ## 🏗️ Architecture
159 | 
160 | ### Module Structure
161 | 
162 | ```
163 | fastreports/
164 | ├── src/
165 | │   ├── ingestion/          # Data loading and format detection
166 | │   │   ├── file_detector.py
167 | │   │   └── data_loader.py
168 | │   ├── profiling/          # Data profiling and quality assessment
169 | │   │   ├── profiler.py
170 | │   │   └── quality_checker.py
171 | │   ├── cleaning/           # Data cleaning and validation
172 | │   │   ├── strategy_generator.py
173 | │   │   ├── transformers.py
174 | │   │   └── validator.py
175 | │   ├── analysis/           # Statistical analysis and EDA
176 | │   │   ├── statistics.py
177 | │   │   └── eda.py
178 | │   ├── visualization/      # Chart generation and recommendations
179 | │   │   ├── chart_generator.py
180 | │   │   ├── plotly_charts.py
181 | │   │   └── recommender.py
182 | │   ├── orchestration/      # Pipeline management
183 | │   │   └── pipeline.py
184 | │   ├── bob_integration/    # IBM Bob integration
185 | │   │   ├── session_manager.py
186 | │   │   └── prompt_templates.py
187 | │   └── utils/              # Utilities
188 | │       ├── logger.py
189 | │       └── config_loader.py
190 | ├── data/                   # Sample datasets
191 | ├── output/                 # Generated reports and logs
192 | ├── bob_sessions/           # Bob interaction logs
193 | ├── main.py                 # Application entry point
194 | └── requirements.txt        # Python dependencies
195 | ```
196 | 
197 | ### Pipeline Flow
198 | 
199 | ```mermaid
200 | graph TD
201 |     A[Data Ingestion] -->|Load and validate data| B[Data Profiling]
202 |     B -->|Analyze characteristics| C[Quality Check]
203 |     C -->|Identify issues, score quality| D{Quality Score}
204 |     D -->|Score < 70| E[Data Cleaning]
205 |     D -->|Score >= 70| F[Statistical Analysis]
206 |     E -->|Apply transformations| F
207 |     F -->|Comprehensive analysis| G[EDA Report]
208 |     G -->|Generate insights| H[Visualization]
209 |     H -->|Create interactive charts| I[Final Report]
210 |     
211 |     style A fill:#e1f5ff,stroke:#0288d1,stroke-width:2px
212 |     style B fill:#fff3e0,stroke:#f57c00,stroke-width:2px
213 |     style C fill:#fce4ec,stroke:#c2185b,stroke-width:2px
214 |     style D fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
215 |     style E fill:#fff9c4,stroke:#f9a825,stroke-width:2px
216 |     style F fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
217 |     style G fill:#e0f2f1,stroke:#00796b,stroke-width:2px
218 |     style H fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px
219 |     style I fill:#e0f7fa,stroke:#0097a7,stroke-width:2px
220 | ```
221 | 
222 | ## 🤖 IBM Bob Integration
223 | 
224 | ### How Bob is Used
225 | 
226 | 1. **Prompt Templates** (`src/bob_integration/prompt_templates.py`)
227 |    - Pre-built prompts for each pipeline phase
228 |    - Context-aware generation
229 |    - Reusable across datasets
230 | 
231 | 2. **Session Management** (`src/bob_integration/session_manager.py`)
232 |    - Tracks all Bob interactions
233 |    - Logs prompts, responses, and metadata
234 |    - Generates usage analytics
235 |    - Exports session history
236 | 
237 | 3. **Mode Utilization**
238 |    - **Plan Mode**: Architecture and strategy planning
239 |    - **Code Mode**: Implementation and code generation
240 |    - **Advanced Mode**: Complex analysis (conceptual)
241 | 
242 | ### Bob Session Output
243 | 
244 | Every run generates a Bob session log in `bob_sessions/` with:
245 | - Session ID and timestamp
246 | - All interactions with prompts and responses
247 | - Modes used
248 | - Success/failure tracking
249 | - Metadata for each interaction
250 | 
251 | ### Example Bob Interaction
252 | 
253 | ```python
254 | # Starting a session
255 | bob_session.start_session("layoffs", "Complete data analysis")
256 | 
257 | # Logging an interaction
258 | bob_session.log_interaction(
259 |     mode="Code Mode",
260 |     phase="cleaning",
261 |     prompt="Generate cleaning strategies for missing values",
262 |     response="Applied mean imputation for numeric columns",
263 |     success=True,
264 |     metadata={"columns_cleaned": 5}
265 | )
266 | 
267 | # Ending session
268 | summary = bob_session.end_session()
269 | ```
270 | 
271 | ## 📈 Output Examples
272 | 
273 | ### Console Output
274 | 
275 | ```
276 | ================================================================================
277 | FastReports - Automated Data Analysis Pipeline
278 | IBM Bob Integration Demonstration
279 | ================================================================================
280 | 
281 | [INFO] Starting Data Analysis Pipeline for: layoffs
282 | [INFO] ════════════════════════════════════════════════════════════════════════
283 | [INFO] PHASE: Data Ingestion
284 | [INFO] ════════════════════════════════════════════════════════════════════════
285 | [INFO] Loaded dataset: layoffs
286 | [INFO] Shape: (2361, 9)
287 | [INFO] Working directory: processed_data/layoffs
288 | 
289 | [INFO] ════════════════════════════════════════════════════════════════════════
290 | [INFO] PHASE: Data Profiling
291 | [INFO] ════════════════════════════════════════════════════════════════════════
292 | [INFO] Profile generated successfully
293 | 
294 | [INFO] ════════════════════════════════════════════════════════════════════════
295 | [INFO] PHASE: Quality Checking
296 | [INFO] ════════════════════════════════════════════════════════════════════════
297 | [INFO] Quality Score: 72.5/100
298 | 
299 | KEY RESULTS
300 | ================================================================================
301 | Data Quality Score: 72.5/100
302 | 
303 | Key Findings (5):
304 |   1. Large dataset with 2,361 rows - suitable for robust analysis
305 |   2. Significant missing data (15.3%) requires attention
306 |   3. Found 3 strong correlations between variables
307 |   4. 2 variables show non-normal distributions
308 |   5. Outliers detected in 3 columns
309 | 
310 | Visualizations Generated: 15
311 | ================================================================================
312 | ```
313 | 
314 | ### Bob Session Summary
315 | 
316 | ```
317 | ================================================================================
318 | BOB SESSION SUMMARY: layoffs_20260516_123045
319 | ================================================================================
320 | 
321 | Dataset: layoffs
322 | Purpose: Complete data analysis pipeline execution
323 | Start Time: 2026-05-16T12:30:45
324 | End Time: 2026-05-16T12:35:22
325 | 
326 | Total Interactions: 8
327 | Modes Used: Plan Mode, Code Mode
328 | 
329 | INTERACTIONS:
330 | --------------------------------------------------------------------------------
331 | 1. ✓ [Plan Mode] initialization
332 |    Time: 2026-05-16T12:30:45
333 |    
334 | 2. ✓ [Code Mode] ingestion
335 |    Time: 2026-05-16T12:31:12
336 |    
337 | 3. ✓ [Code Mode] profiling
338 |    Time: 2026-05-16T12:32:05
339 |    
340 | ...
341 | ================================================================================
342 | ```
343 | 
344 | ## 📊 Data Quality Scoring
345 | 
346 | The system provides a comprehensive quality score (0-100) based on:
347 | 
348 | - **Missing Values** (30 points): Percentage of missing data
349 | - **Duplicates** (20 points): Duplicate row detection
350 | - **Outliers** (20 points): Outlier prevalence
351 | - **Consistency** (15 points): Data type consistency
352 | - **Completeness** (15 points): Column completeness
353 | 
354 | ### Quality Grades
355 | 
356 | - **A (90-100)**: Excellent - Ready for analysis
357 | - **B (80-89)**: Good - Minor issues
358 | - **C (70-79)**: Fair - Cleaning recommended
359 | - **D (60-69)**: Poor - Significant issues
360 | - **F (<60)**: Critical - Major cleaning required
361 | 
362 | ## 🎨 Visualization Types
363 | 
364 | The system automatically generates appropriate visualizations:
365 | 
366 | 1. **Histogram**: Distribution of numeric values
367 | 2. **Box Plot**: Outlier detection and quartiles
368 | 3. **Bar Chart**: Categorical frequency comparison
369 | 4. **Scatter Plot**: Relationship between variables
370 | 5. **Line Chart**: Trends over time
371 | 6. **Heatmap**: Correlation matrix
372 | 7. **Pie Chart**: Composition and proportions
373 | 8. **Area Chart**: Cumulative trends
374 | 9. **Grouped Bar**: Multi-category comparisons
375 | 
376 | ## 🔧 Configuration
377 | 
378 | Edit `config.yaml` to customize:
379 | 
380 | ```yaml
381 | pipeline:
382 |   auto_clean: false
383 |   quality_threshold: 70
384 |   max_visualizations: 20
385 | 
386 | logging:
387 |   level: INFO
388 |   format: detailed
389 | 
390 | output:
391 |   directory: output/
392 |   save_intermediate: true
393 | ```
394 | 
395 | ## 📝 Logging
396 | 
397 | Comprehensive logging at multiple levels:
398 | 
399 | - **Console**: Real-time progress and key results
400 | - **File Logs**: Detailed execution logs in `output/logs/`
401 | - **Bob Sessions**: Interaction logs in `bob_sessions/`
402 | - **Phase Tracking**: Start/end times for each phase
403 | 
404 | ## 🧪 Testing
405 | 
406 | ```bash
407 | # Run with test dataset
408 | python main.py data/layoffs/layoffs.csv --dataset-name layoffs_test
409 | 
410 | # Verify all phases complete
411 | python main.py --auto-clean
412 | 
413 | # Check Bob session logs
414 | ls -la bob_sessions/
415 | ```
416 | 
417 | ## 🌐 API & Dashboard
418 | 
419 | ### REST API
420 | 
421 | The FastAPI backend provides:
422 | - **GET /api/datasets**: List available datasets
423 | - **GET /api/data**: Load dataset with pagination
424 | - **POST /api/query**: Execute SQL queries with DuckDB
425 | - **GET /api/profile**: Get detailed dataset profiling
426 | 
427 | See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference.
428 | 
429 | ### Interactive Dashboard
430 | 
431 | The Preact-based dashboard offers:
432 | - Real-time data filtering and search
433 | - SQL query builder with DuckDB
434 | - Interactive Plotly visualizations
435 | - Multiple chart types (bar, line, scatter, pie, histogram, box)
436 | - CSV export functionality
437 | - Responsive design
438 | 
439 | **Access**: http://localhost:3000 (when running `start_all.sh`)
440 | 
441 | ## 🚧 Known Limitations
442 | 
443 | 1. **HTML Report Generator**: Not yet implemented
444 | 2. **Large Files**: Memory constraints for files >1GB
445 | 3. **Real-time Bob API**: Uses simulated interactions for demo
446 | 
447 | ## 🔮 Future Enhancements
448 | 
449 | ### High Priority
450 | - HTML report generator with embedded visualizations
451 | - Report compiler for multiple datasets
452 | - Example outputs for all sample datasets
453 | 
454 | ### Medium Priority
455 | - User checkpoint system for approvals
456 | - Domain-specific analyzers (time series, text, transactions)
457 | - Authentication and authorization for API
458 | - WebSocket support for real-time updates
459 | 
460 | ### Low Priority
461 | - Cloud deployment (AWS, Azure, GCP)
462 | - Performance optimizations and caching
463 | - Export to PDF and PowerPoint
464 | - Advanced ML-based anomaly detection
465 | 
466 | ## 📚 Documentation
467 | 
468 | - **ARCHITECTURE.md**: Detailed system architecture
469 | - **IMPLEMENTATION_PLAN.md**: Phase-by-phase implementation guide
470 | - **IMPLEMENTATION_SUMMARY.md**: What was built and how
471 | - **DATA_CLEANING_STRATEGIES.md**: Cleaning approach documentation
472 | - **API_DOCUMENTATION.md**: Complete API reference and examples
473 | 
474 | ## 🤝 Contributing
475 | 
476 | This is a hackathon project demonstrating IBM Bob integration. Contributions welcome!
477 | 
478 | ## 📄 License
479 | 
480 | MIT License - See LICENSE file for details
481 | 
482 | ## 🙏 Acknowledgments
483 | 
484 | - **IBM Bob**: AI-assisted development throughout
485 | - **Plotly**: Interactive visualization library
486 | - **Pandas**: Data manipulation foundation
487 | - **SciPy**: Statistical analysis tools
488 | 
489 | ## 📧 Contact
490 | 
491 | For questions or feedback about this hackathon submission, please reach out through the IBM Bob hackathon platform.
492 | 
493 | ---
494 | 
495 | **Built with IBM Bob** 🤖 | **Hackathon 2026** 🏆
496 | 
497 | *Demonstrating meaningful AI integration in data analysis workflows*
498 | 
499 | ---
500 | 
501 | ## 🎯 Quick Demo
502 | 
503 | ```bash
504 | # 1. Install dependencies
505 | pip install -r requirements.txt
506 | 
507 | # 2. Run the pipeline
508 | python main.py
509 | 
510 | # 3. Check the outputs
511 | cat output/logs/fastreports_*.log
512 | ls bob_sessions/
513 | 
514 | # 4. Try with different dataset
515 | python main.py data/soccer/laliga_22_23.csv --dataset-name laliga --auto-clean
516 | ```
517 | 
518 | **Expected Runtime**: 30-60 seconds per dataset
519 | **Memory Usage**: ~200-500 MB
520 | **Output Files**: Logs, session data, processed datasets
521 | 
522 | ---
523 | 
524 | *Made with ❤️ and IBM Bob*
</content>
</file>
<file><path>ARCHITECTURE.md</path>
<content lines="1-406">
  1 | # FastReports - Automated Data Analysis Pipeline Architecture
  2 | 
  3 | ## Executive Summary
  4 | 
  5 | FastReports is an intelligent data analysis pipeline that leverages IBM Bob to automate the entire data analysis workflow for data analysts. The system automatically processes raw data through cleaning, exploration, and visualization phases, generating comprehensive reports with minimal manual intervention.
  6 | 
  7 | ## Data Quality Analysis
  8 | 
  9 | ### Layoffs Dataset Issues Identified:
 10 | 1. **NULL values** in critical columns (total_laid_off, percentage_laid_off, funds_raised_millions)
 11 | 2. **Empty strings** in industry column (line 10: Airbnb has empty industry)
 12 | 3. **Inconsistent country names** (line 12: "United States." with period)
 13 | 4. **Date format inconsistency** (M/D/YYYY format needs standardization)
 14 | 5. **Mixed data types** (NULL as string vs actual null values)
 15 | 
 16 | ### Soccer Dataset Characteristics:
 17 | 1. **High dimensionality** (100+ columns with betting odds)
 18 | 2. **Consistent structure** across multiple seasons
 19 | 3. **Clean data** with proper numeric types
 20 | 4. **Time series data** suitable for trend analysis
 21 | 
 22 | ### Pizza Delivery Dataset:
 23 | 1. **Mixed data types** (XLSX format with dates, text, numbers)
 24 | 2. **Survey responses** with free-text requiring NLP
 25 | 3. **Transactional data** with order details
 26 | 4. **Customer feedback** requiring sentiment analysis
 27 | 
 28 | ## System Architecture
 29 | 
 30 | ```mermaid
 31 | graph TB
 32 |     A[User Drops Data in Folder] --> B[Data Ingestion Module]
 33 |     B --> C[Data Profiler]
 34 |     C --> D{IBM Bob Analysis}
 35 |     D --> E[Data Cleaning Module]
 36 |     E --> F[Exploratory Data Analysis]
 37 |     F --> G[Visualization Engine]
 38 |     G --> H[Report Generator]
 39 |     H --> I[Static HTML Report]
 40 |     H --> J[Interactive Dashboard]
 41 |     
 42 |     K[Bob Session Manager] -.-> D
 43 |     K -.-> E
 44 |     K -.-> F
 45 |     K -.-> G
 46 |     
 47 |     L[User Checkpoints] -.-> E
 48 |     L -.-> F
 49 |     L -.-> G
 50 |     
 51 |     M[Original Data] --> N[processed_data/ Copy]
 52 |     N --> B
 53 | ```
 54 | 
 55 | ## Component Architecture
 56 | 
 57 | ### 1. Data Ingestion Module
 58 | **Purpose**: Safely copy and load data from various formats
 59 | 
 60 | **IBM Bob Integration**:
 61 | - **Mode**: Code Mode
 62 | - **Task**: Generate file format detection and parsing code
 63 | - **Output**: Python scripts for CSV, XLSX, JSON parsing
 64 | 
 65 | **Features**:
 66 | - Auto-detect file formats (CSV, XLSX, JSON, Parquet)
 67 | - Create working copies in `processed_data/` directory
 68 | - Preserve original data integrity
 69 | - Generate metadata about data sources
 70 | 
 71 | ### 2. Data Profiler
 72 | **Purpose**: Analyze data characteristics and quality
 73 | 
 74 | **IBM Bob Integration**:
 75 | - **Mode**: Plan Mode
 76 | - **Task**: Analyze data structure and suggest profiling strategies
 77 | - **Output**: Profiling plan and quality metrics
 78 | 
 79 | **Metrics Generated**:
 80 | - Column data types and distributions
 81 | - Missing value analysis
 82 | - Outlier detection
 83 | - Data quality scores
 84 | - Correlation analysis
 85 | 
 86 | ### 3. Data Cleaning Module
 87 | **Purpose**: Clean and transform data based on quality issues
 88 | 
 89 | **IBM Bob Integration**:
 90 | - **Mode**: Code Mode
 91 | - **Task**: Generate cleaning scripts based on profiling results
 92 | - **Output**: Python transformation scripts
 93 | 
 94 | **Cleaning Operations**:
 95 | - Handle NULL/missing values (imputation strategies)
 96 | - Standardize date formats
 97 | - Fix inconsistent categorical values
 98 | - Remove duplicates
 99 | - Normalize text fields
100 | - Type conversions
101 | 
102 | ### 4. Exploratory Data Analysis (EDA) Module
103 | **Purpose**: Generate insights and statistical analysis
104 | 
105 | **IBM Bob Integration**:
106 | - **Mode**: Advanced Mode (with MCP tools)
107 | - **Task**: Generate analysis queries and statistical tests
108 | - **Output**: Analysis scripts and insights
109 | 
110 | **Analysis Types**:
111 | - Descriptive statistics
112 | - Distribution analysis
113 | - Correlation matrices
114 | - Time series analysis (for soccer data)
115 | - Sentiment analysis (for survey data)
116 | - Trend identification
117 | 
118 | ### 5. Visualization Engine
119 | **Purpose**: Create meaningful visualizations
120 | 
121 | **IBM Bob Integration**:
122 | - **Mode**: Code Mode
123 | - **Task**: Generate visualization code based on data characteristics
124 | - **Output**: Plotly/D3.js visualization scripts
125 | 
126 | **Chart Types**:
127 | - Bar charts (categorical comparisons)
128 | - Line charts (time series trends)
129 | - Scatter plots (correlations)
130 | - Heatmaps (correlation matrices)
131 | - Box plots (distribution analysis)
132 | - Pie charts (composition)
133 | - Geographic maps (location data)
134 | 
135 | ### 6. Report Generator
136 | **Purpose**: Compile analysis into consumable formats
137 | 
138 | **IBM Bob Integration**:
139 | - **Mode**: Code Mode
140 | - **Task**: Generate report templates and styling
141 | - **Output**: HTML/CSS templates
142 | 
143 | **Output Formats**:
144 | 1. **Static HTML Report**:
145 |    - Executive summary
146 |    - Data quality report
147 |    - Statistical analysis
148 |    - Embedded visualizations
149 |    - Downloadable as single file
150 | 
151 | 2. **Interactive Dashboard** (Preact):
152 |    - Real-time filtering
153 |    - Interactive charts
154 |    - Drill-down capabilities
155 |    - Export functionality
156 | 
157 | ### 7. Orchestration Layer
158 | **Purpose**: Manage pipeline execution and user interaction
159 | 
160 | **IBM Bob Integration**:
161 | - **Mode**: Orchestrator Mode
162 | - **Task**: Coordinate multi-phase workflow
163 | - **Output**: Execution plan and progress tracking
164 | 
165 | **Features**:
166 | - Phase-by-phase execution
167 | - User checkpoints for approval
168 | - Progress tracking and logging
169 | - Error handling and recovery
170 | - Session state management
171 | 
172 | ## Technology Stack
173 | 
174 | ### Backend
175 | - **Python 3.10+**: Core processing language
176 | - **Pandas**: Data manipulation
177 | - **NumPy**: Numerical operations
178 | - **Plotly**: Interactive visualizations
179 | - **scikit-learn**: Statistical analysis
180 | - **openpyxl**: Excel file handling
181 | 
182 | ### Frontend
183 | - **Preact**: Lightweight UI framework (3KB)
184 | - **D3.js**: Advanced visualizations
185 | - **Tailwind CSS**: Styling
186 | - **Vite**: Build tool
187 | 
188 | ### IBM Bob Integration
189 | - **Modes Used**:
190 |   - Plan Mode: Architecture and strategy
191 |   - Code Mode: Implementation
192 |   - Advanced Mode: Complex analysis with MCP
193 |   - Orchestrator Mode: Workflow coordination
194 | 
195 | ## Directory Structure
196 | 
197 | ```
198 | fastreports/
199 | ├── data/                          # Original data (READ-ONLY)
200 | │   ├── layoffs/
201 | │   ├── soccer/
202 | │   └── pizza_delivery_app/
203 | ├── processed_data/                # Working copies
204 | │   ├── {dataset_name}/
205 | │   │   ├── raw_copy.csv
206 | │   │   ├── cleaned.csv
207 | │   │   └── metadata.json
208 | ├── src/
209 | │   ├── ingestion/
210 | │   │   ├── file_detector.py
211 | │   │   └── data_loader.py
212 | │   ├── profiling/
213 | │   │   ├── profiler.py
214 | │   │   └── quality_checker.py
215 | │   ├── cleaning/
216 | │   │   ├── cleaner.py
217 | │   │   └── transformers.py
218 | │   ├── analysis/
219 | │   │   ├── eda.py
220 | │   │   └── statistics.py
221 | │   ├── visualization/
222 | │   │   ├── chart_generator.py
223 | │   │   └── plotly_charts.py
224 | │   ├── reporting/
225 | │   │   ├── html_generator.py
226 | │   │   └── dashboard_builder.py
227 | │   ├── orchestration/
228 | │   │   ├── pipeline.py
229 | │   │   └── checkpoint_manager.py
230 | │   └── bob_integration/
231 | │       ├── session_manager.py
232 | │       └── prompt_templates.py
233 | ├── dashboard/                     # Preact dashboard
234 | │   ├── src/
235 | │   │   ├── components/
236 | │   │   ├── App.jsx
237 | │   │   └── main.jsx
238 | │   ├── package.json
239 | │   └── vite.config.js
240 | ├── output/
241 | │   └── reports/
242 | │       ├── {dataset_name}/
243 | │       │   ├── report.html
244 | │       │   ├── dashboard.html
245 | │       │   └── assets/
246 | ├── bob_sessions/                  # Bob interaction logs
247 | │   └── {timestamp}_session.log
248 | ├── tests/
249 | ├── ARCHITECTURE.md
250 | ├── README.md
251 | └── requirements.txt
252 | ```
253 | 
254 | ## Pipeline Execution Flow
255 | 
256 | ### Phase 1: Initialization
257 | 1. User drops data folder into `data/` directory
258 | 2. System detects new data
259 | 3. **Bob (Plan Mode)**: Analyzes folder structure and creates execution plan
260 | 
261 | ### Phase 2: Data Ingestion
262 | 1. **Bob (Code Mode)**: Generates file parsing code
263 | 2. System creates working copy in `processed_data/`
264 | 3. Generates metadata file
265 | 4. **Checkpoint**: User reviews data loading summary
266 | 
267 | ### Phase 3: Data Profiling
268 | 1. **Bob (Plan Mode)**: Plans profiling strategy
269 | 2. System runs profiling analysis
270 | 3. Generates quality report
271 | 4. **Checkpoint**: User reviews quality issues
272 | 
273 | ### Phase 4: Data Cleaning
274 | 1. **Bob (Code Mode)**: Generates cleaning scripts based on issues
275 | 2. System applies transformations
276 | 3. Validates cleaned data
277 | 4. **Checkpoint**: User reviews cleaning results
278 | 
279 | ### Phase 5: Exploratory Analysis
280 | 1. **Bob (Advanced Mode)**: Generates analysis queries
281 | 2. System runs statistical analysis
282 | 3. Identifies key insights
283 | 4. **Checkpoint**: User reviews insights
284 | 
285 | ### Phase 6: Visualization
286 | 1. **Bob (Code Mode)**: Generates visualization code
287 | 2. System creates charts based on data characteristics
288 | 3. Optimizes for web display
289 | 4. **Checkpoint**: User reviews visualizations
290 | 
291 | ### Phase 7: Report Generation
292 | 1. **Bob (Code Mode)**: Generates report templates
293 | 2. System compiles static HTML report
294 | 3. Builds interactive Preact dashboard
295 | 4. **Final Output**: Both report types ready
296 | 
297 | ## IBM Bob Usage Documentation
298 | 
299 | ### Mode Selection Strategy
300 | 
301 | | Phase | Mode | Reason |
302 | |-------|------|--------|
303 | | Planning | Plan Mode | Strategic thinking, architecture design |
304 | | Code Generation | Code Mode | Fast implementation, file operations |
305 | | Complex Analysis | Advanced Mode | MCP tools, browser automation |
306 | | Workflow Coordination | Orchestrator Mode | Multi-step task management |
307 | 
308 | ### Prompt Engineering Templates
309 | 
310 | #### Data Profiling Prompt
311 | ```
312 | Analyze this dataset and identify:
313 | 1. Data quality issues (missing values, outliers, inconsistencies)
314 | 2. Column types and distributions
315 | 3. Potential relationships between variables
316 | 4. Recommended cleaning strategies
317 | 
318 | Dataset preview: {data_sample}
319 | ```
320 | 
321 | #### Cleaning Script Generation Prompt
322 | ```
323 | Generate Python code to clean this dataset based on these issues:
324 | {quality_issues}
325 | 
326 | Requirements:
327 | - Use pandas for transformations
328 | - Preserve original data
329 | - Log all changes
330 | - Handle edge cases
331 | ```
332 | 
333 | #### Visualization Prompt
334 | ```
335 | Generate Plotly visualization code for:
336 | Dataset: {dataset_name}
337 | Key metrics: {metrics}
338 | Chart types needed: {chart_types}
339 | 
340 | Make visualizations interactive and publication-ready.
341 | ```
342 | 
343 | ## Safety Mechanisms
344 | 
345 | ### Data Protection
346 | 1. **Read-only original data**: Original files never modified
347 | 2. **Copy-on-write**: All operations on copies
348 | 3. **Backup before cleaning**: Preserve raw copy
349 | 4. **Audit trail**: Log all transformations
350 | 
351 | ### User Control
352 | 1. **Checkpoint system**: User approval at each phase
353 | 2. **Preview before apply**: Show changes before committing
354 | 3. **Rollback capability**: Revert to previous state
355 | 4. **Manual override**: User can modify Bob suggestions
356 | 
357 | ## Performance Considerations
358 | 
359 | ### Optimization Strategies
360 | 1. **Lazy loading**: Load data in chunks for large files
361 | 2. **Caching**: Cache profiling results
362 | 3. **Parallel processing**: Use multiprocessing for analysis
363 | 4. **Incremental updates**: Only reprocess changed data
364 | 
365 | ### Scalability
366 | - Handle datasets up to 1GB efficiently
367 | - Stream processing for larger files
368 | - Distributed processing option for future
369 | 
370 | ## Testing Strategy
371 | 
372 | ### Unit Tests
373 | - Each module independently tested
374 | - Mock Bob responses for consistency
375 | - Edge case handling
376 | 
377 | ### Integration Tests
378 | - End-to-end pipeline execution
379 | - All three datasets processed
380 | - Output validation
381 | 
382 | ### User Acceptance Tests
383 | - Real-world scenarios
384 | - Performance benchmarks
385 | - Usability testing
386 | 
387 | ## Future Enhancements
388 | 
389 | 1. **Real-time data streaming**: Process live data feeds
390 | 2. **ML model integration**: Automated predictive modeling
391 | 3. **Collaborative features**: Multi-user analysis
392 | 4. **Cloud deployment**: Web-based service
393 | 5. **API endpoints**: Programmatic access
394 | 6. **Custom plugins**: User-defined analysis modules
395 | 
396 | ## Success Metrics
397 | 
398 | 1. **Time Savings**: 80% reduction in manual analysis time
399 | 2. **Accuracy**: 95%+ data quality improvement
400 | 3. **User Satisfaction**: Positive feedback from data analysts
401 | 4. **Bob Integration**: Meaningful use in all phases
402 | 5. **Report Quality**: Publication-ready outputs
403 | 
404 | ## Conclusion
405 | 
406 | FastReports demonstrates meaningful IBM Bob integration by leveraging AI assistance throughout the entire data analysis pipeline. Bob acts as an intelligent development partner, generating code, suggesting strategies, and coordinating complex workflows - exactly as intended by the hackathon challenge.
</content>
</file>
<file><path>API_DOCUMENTATION.md</path>
<content lines="1-553">
  1 | # FastReports API Documentation
  2 | 
  3 | ## Overview
  4 | 
  5 | The FastReports API provides a RESTful interface for data analysis and visualization. Built with FastAPI, it offers high performance, automatic API documentation, and seamless integration with the dashboard UI.
  6 | 
  7 | **Base URL:** `http://localhost:8000`  
  8 | **API Documentation:** `http://localhost:8000/docs` (Swagger UI)  
  9 | **Alternative Docs:** `http://localhost:8000/redoc` (ReDoc)
 10 | 
 11 | ---
 12 | 
 13 | ## Quick Start
 14 | 
 15 | ### 1. Install Dependencies
 16 | 
 17 | ```bash
 18 | pip install -r requirements.txt
 19 | ```
 20 | 
 21 | ### 2. Start the API Server
 22 | 
 23 | **Linux/macOS:**
 24 | ```bash
 25 | chmod +x start_server.sh
 26 | ./start_server.sh
 27 | ```
 28 | 
 29 | **Windows:**
 30 | ```cmd
 31 | start_server.bat
 32 | ```
 33 | 
 34 | **Or directly with Python:**
 35 | ```bash
 36 | python api_server.py
 37 | ```
 38 | 
 39 | ### 3. Start Both API and Dashboard
 40 | 
 41 | **Linux/macOS:**
 42 | ```bash
 43 | chmod +x start_all.sh
 44 | ./start_all.sh
 45 | ```
 46 | 
 47 | ---
 48 | 
 49 | ## API Endpoints
 50 | 
 51 | ### 1. Root Endpoint
 52 | 
 53 | **GET** `/`
 54 | 
 55 | Get API information and available endpoints.
 56 | 
 57 | **Response:**
 58 | ```json
 59 | {
 60 |   "message": "FastReports API Server",
 61 |   "version": "1.0.0",
 62 |   "endpoints": [
 63 |     "/api/datasets",
 64 |     "/api/data",
 65 |     "/api/query",
 66 |     "/api/profile"
 67 |   ]
 68 | }
 69 | ```
 70 | 
 71 | ---
 72 | 
 73 | ### 2. List Datasets
 74 | 
 75 | **GET** `/api/datasets`
 76 | 
 77 | Get a list of all available datasets in the `data/` directory.
 78 | 
 79 | **Response:**
 80 | ```json
 81 | {
 82 |   "datasets": [
 83 |     {
 84 |       "name": "Laliga 24 25",
 85 |       "path": "data/soccer/laliga_24_25.csv",
 86 |       "size": 45678
 87 |     },
 88 |     {
 89 |       "name": "Layoffs",
 90 |       "path": "data/layoffs/layoffs.csv",
 91 |       "size": 123456
 92 |     }
 93 |   ]
 94 | }
 95 | ```
 96 | 
 97 | **Supported File Formats:**
 98 | - CSV (`.csv`)
 99 | - Excel (`.xlsx`, `.xls`)
100 | - JSON (`.json`)
101 | - Parquet (`.parquet`)
102 | 
103 | ---
104 | 
105 | ### 3. Load Dataset
106 | 
107 | **GET** `/api/data`
108 | 
109 | Load and return dataset with optional pagination.
110 | 
111 | **Query Parameters:**
112 | - `path` (required): Path to the dataset file
113 | - `limit` (optional): Maximum number of rows to return
114 | - `offset` (optional): Number of rows to skip (default: 0)
115 | 
116 | **Example Request:**
117 | ```
118 | GET /api/data?path=data/soccer/laliga_24_25.csv&limit=100&offset=0
119 | ```
120 | 
121 | **Response:**
122 | ```json
123 | {
124 |   "data": [
125 |     {
126 |       "team": "Real Madrid",
127 |       "points": 85,
128 |       "goals": 78
129 |     }
130 |   ],
131 |   "columns": ["team", "points", "goals"],
132 |   "total_rows": 380,
133 |   "returned_rows": 100,
134 |   "stats": {
135 |     "quality_score": 95.5,
136 |     "missing_values": {
137 |       "total_missing": 5,
138 |       "total_values": 1140
139 |     },
140 |     "data_types": {
141 |       "team": "object",
142 |       "points": "int64",
143 |       "goals": "int64"
144 |     }
145 |   }
146 | }
147 | ```
148 | 
149 | ---
150 | 
151 | ### 4. Execute SQL Query
152 | 
153 | **POST** `/api/query`
154 | 
155 | Execute SQL queries on datasets using DuckDB.
156 | 
157 | **Request Body:**
158 | ```json
159 | {
160 |   "query": "SELECT team, points FROM temp_data WHERE points > 70 ORDER BY points DESC",
161 |   "data": [
162 |     {"team": "Real Madrid", "points": 85},
163 |     {"team": "Barcelona", "points": 82}
164 |   ]
165 | }
166 | ```
167 | 
168 | **Note:** If `data` is not provided, the query will run on the most recently loaded dataset.
169 | 
170 | **Response:**
171 | ```json
172 | {
173 |   "data": [
174 |     {"team": "Real Madrid", "points": 85},
175 |     {"team": "Barcelona", "points": 82}
176 |   ],
177 |   "columns": ["team", "points"],
178 |   "rows": 2,
179 |   "success": true
180 | }
181 | ```
182 | 
183 | **SQL Examples:**
184 | 
185 | ```sql
186 | -- Filter data
187 | SELECT * FROM temp_data WHERE column_name > 100
188 | 
189 | -- Aggregate data
190 | SELECT category, COUNT(*), AVG(value) 
191 | FROM temp_data 
192 | GROUP BY category
193 | 
194 | -- Join operations (if multiple tables registered)
195 | SELECT a.*, b.value 
196 | FROM temp_data a 
197 | LEFT JOIN other_table b ON a.id = b.id
198 | 
199 | -- Window functions
200 | SELECT *, 
201 |        ROW_NUMBER() OVER (PARTITION BY category ORDER BY value DESC) as rank
202 | FROM temp_data
203 | ```
204 | 
205 | ---
206 | 
207 | ### 5. Get Dataset Profile
208 | 
209 | **GET** `/api/profile`
210 | 
211 | Get detailed profiling information about a dataset.
212 | 
213 | **Query Parameters:**
214 | - `path` (required): Path to the dataset file
215 | 
216 | **Example Request:**
217 | ```
218 | GET /api/profile?path=data/soccer/laliga_24_25.csv
219 | ```
220 | 
221 | **Response:**
222 | ```json
223 | {
224 |   "shape": {
225 |     "rows": 380,
226 |     "columns": 15
227 |   },
228 |   "column_types": {
229 |     "team": "object",
230 |     "points": "int64",
231 |     "goals": "int64"
232 |   },
233 |   "missing_summary": {
234 |     "total_missing": 5,
235 |     "total_values": 5700,
236 |     "missing_percentage": 0.088
237 |   },
238 |   "duplicates": {
239 |     "count": 0,
240 |     "percentage": 0.0
241 |   },
242 |   "quality_score": 95.5,
243 |   "numeric_stats": {
244 |     "points": {
245 |       "mean": 45.2,
246 |       "median": 44.0,
247 |       "std": 15.3,
248 |       "min": 10,
249 |       "max": 85
250 |     }
251 |   }
252 | }
253 | ```
254 | 
255 | ---
256 | 
257 | ## Error Handling
258 | 
259 | The API uses standard HTTP status codes:
260 | 
261 | - **200 OK**: Request successful
262 | - **400 Bad Request**: Invalid request parameters or query
263 | - **404 Not Found**: Dataset not found
264 | - **500 Internal Server Error**: Server error
265 | 
266 | **Error Response Format:**
267 | ```json
268 | {
269 |   "detail": "Error message describing what went wrong"
270 | }
271 | ```
272 | 
273 | ---
274 | 
275 | ## Configuration
276 | 
277 | ### Environment Variables
278 | 
279 | - `API_HOST`: Server host (default: `0.0.0.0`)
280 | - `API_PORT`: Server port (default: `8000`)
281 | 
282 | **Example:**
283 | ```bash
284 | export API_HOST=localhost
285 | export API_PORT=9000
286 | python api_server.py
287 | ```
288 | 
289 | ### CORS Configuration
290 | 
291 | The API allows requests from:
292 | - `http://localhost:3000` (Dashboard dev server)
293 | - `http://localhost:5173` (Alternative Vite port)
294 | 
295 | To add more origins, modify `api_server.py`:
296 | 
297 | ```python
298 | app.add_middleware(
299 |     CORSMiddleware,
300 |     allow_origins=["http://localhost:3000", "http://your-domain.com"],
301 |     allow_credentials=True,
302 |     allow_methods=["*"],
303 |     allow_headers=["*"],
304 | )
305 | ```
306 | 
307 | ---
308 | 
309 | ## Integration with Dashboard
310 | 
311 | The dashboard automatically proxies API requests through Vite's dev server:
312 | 
313 | **Vite Configuration** (`dashboard/vite.config.js`):
314 | ```javascript
315 | export default defineConfig({
316 |   server: {
317 |     port: 3000,
318 |     proxy: {
319 |       '/api': {
320 |         target: 'http://localhost:8000',
321 |         changeOrigin: true,
322 |       },
323 |     },
324 |   },
325 | });
326 | ```
327 | 
328 | This means the dashboard can make requests to `/api/datasets` and they will be forwarded to `http://localhost:8000/api/datasets`.
329 | 
330 | ---
331 | 
332 | ## Performance Considerations
333 | 
334 | ### Caching
335 | 
336 | The API caches loaded datasets in memory to improve performance:
337 | 
338 | ```python
339 | dataset_cache: Dict[str, pd.DataFrame] = {}
340 | ```
341 | 
342 | Datasets are cached after first load and reused for subsequent requests.
343 | 
344 | ### Pagination
345 | 
346 | For large datasets, use pagination to limit memory usage:
347 | 
348 | ```
349 | GET /api/data?path=data/large_file.csv&limit=1000&offset=0
350 | ```
351 | 
352 | ### Query Optimization
353 | 
354 | DuckDB provides excellent performance for analytical queries:
355 | - Columnar storage format
356 | - Vectorized execution
357 | - Parallel query processing
358 | 
359 | ---
360 | 
361 | ## Development
362 | 
363 | ### Running Tests
364 | 
365 | ```bash
366 | # Test API endpoints
367 | curl http://localhost:8000/api/datasets
368 | 
369 | # Test with specific dataset
370 | curl "http://localhost:8000/api/data?path=data/soccer/laliga_24_25.csv&limit=10"
371 | 
372 | # Test SQL query
373 | curl -X POST http://localhost:8000/api/query \
374 |   -H "Content-Type: application/json" \
375 |   -d '{"query": "SELECT * FROM temp_data LIMIT 5"}'
376 | ```
377 | 
378 | ### Hot Reload
379 | 
380 | The API server runs with auto-reload enabled during development:
381 | 
382 | ```python
383 | uvicorn.run(
384 |     "api_server:app",
385 |     host=host,
386 |     port=port,
387 |     reload=True,  # Auto-reload on code changes
388 |     log_level="info"
389 | )
390 | ```
391 | 
392 | ---
393 | 
394 | ## Troubleshooting
395 | 
396 | ### Port Already in Use
397 | 
398 | If port 8000 is already in use:
399 | 
400 | ```bash
401 | # Find process using port 8000
402 | lsof -i :8000  # macOS/Linux
403 | netstat -ano | findstr :8000  # Windows
404 | 
405 | # Kill the process or use a different port
406 | export API_PORT=8001
407 | python api_server.py
408 | ```
409 | 
410 | ### Import Errors
411 | 
412 | Ensure all dependencies are installed:
413 | 
414 | ```bash
415 | pip install -r requirements.txt
416 | ```
417 | 
418 | ### Dataset Not Found
419 | 
420 | Verify the dataset path is relative to the project root:
421 | 
422 | ```
423 | ✓ data/soccer/laliga_24_25.csv
424 | ✗ /absolute/path/to/file.csv
425 | ✗ ~/relative/to/home/file.csv
426 | ```
427 | 
428 | ### CORS Errors
429 | 
430 | If you see CORS errors in the browser console:
431 | 1. Ensure the API server is running
432 | 2. Check that the dashboard is accessing through the proxy
433 | 3. Verify CORS origins in `api_server.py`
434 | 
435 | ---
436 | 
437 | ## API Client Examples
438 | 
439 | ### Python
440 | 
441 | ```python
442 | import requests
443 | 
444 | # List datasets
445 | response = requests.get("http://localhost:8000/api/datasets")
446 | datasets = response.json()["datasets"]
447 | 
448 | # Load dataset
449 | response = requests.get(
450 |     "http://localhost:8000/api/data",
451 |     params={"path": "data/soccer/laliga_24_25.csv", "limit": 100}
452 | )
453 | data = response.json()
454 | 
455 | # Execute query
456 | response = requests.post(
457 |     "http://localhost:8000/api/query",
458 |     json={"query": "SELECT * FROM temp_data WHERE points > 70"}
459 | )
460 | results = response.json()
461 | ```
462 | 
463 | ### JavaScript/TypeScript
464 | 
465 | ```javascript
466 | // List datasets
467 | const response = await fetch('/api/datasets');
468 | const { datasets } = await response.json();
469 | 
470 | // Load dataset
471 | const dataResponse = await fetch(
472 |   `/api/data?path=${encodeURIComponent('data/soccer/laliga_24_25.csv')}&limit=100`
473 | );
474 | const data = await dataResponse.json();
475 | 
476 | // Execute query
477 | const queryResponse = await fetch('/api/query', {
478 |   method: 'POST',
479 |   headers: { 'Content-Type': 'application/json' },
480 |   body: JSON.stringify({
481 |     query: 'SELECT * FROM temp_data WHERE points > 70'
482 |   })
483 | });
484 | const results = await queryResponse.json();
485 | ```
486 | 
487 | ### cURL
488 | 
489 | ```bash
490 | # List datasets
491 | curl http://localhost:8000/api/datasets
492 | 
493 | # Load dataset
494 | curl "http://localhost:8000/api/data?path=data/soccer/laliga_24_25.csv&limit=10"
495 | 
496 | # Execute query
497 | curl -X POST http://localhost:8000/api/query \
498 |   -H "Content-Type: application/json" \
499 |   -d '{"query": "SELECT * FROM temp_data LIMIT 5"}'
500 | 
501 | # Get profile
502 | curl "http://localhost:8000/api/profile?path=data/soccer/laliga_24_25.csv"
503 | ```
504 | 
505 | ---
506 | 
507 | ## Security Considerations
508 | 
509 | ### Production Deployment
510 | 
511 | For production deployment:
512 | 
513 | 1. **Disable auto-reload:**
514 |    ```python
515 |    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=False)
516 |    ```
517 | 
518 | 2. **Use environment variables for sensitive data**
519 | 
520 | 3. **Implement authentication:**
521 |    ```python
522 |    from fastapi.security import HTTPBearer
523 |    security = HTTPBearer()
524 |    ```
525 | 
526 | 4. **Add rate limiting:**
527 |    ```python
528 |    from slowapi import Limiter
529 |    limiter = Limiter(key_func=get_remote_address)
530 |    ```
531 | 
532 | 5. **Use HTTPS in production**
533 | 
534 | 6. **Restrict CORS origins to your domain**
535 | 
536 | ---
537 | 
538 | ## License
539 | 
540 | This API is part of the FastReports project. See the main README for license information.
541 | 
542 | ---
543 | 
544 | ## Support
545 | 
546 | For issues, questions, or contributions:
547 | - Check the main project documentation
548 | - Review the interactive API docs at `/docs`
549 | - Examine the source code in `api_server.py`
550 | 
551 | ---
552 | 
553 | **Made with Bob** 🤖
</content>
</file>
<file><path>main.py</path>
<content lines="1-143">
  1 | """
  2 | FastReports - Main Entry Point
  3 | Automated Data Analysis Pipeline with IBM Bob Integration
  4 | """
  5 | 
  6 | import sys
  7 | import argparse
  8 | from pathlib import Path
  9 | from src.utils.logger import get_logger
 10 | from src.orchestration.pipeline import DataAnalysisPipeline
 11 | from src.bob_integration.session_manager import get_bob_session_manager
 12 | 
 13 | logger = get_logger("main")
 14 | 
 15 | 
 16 | def main():
 17 |     """Main execution function."""
 18 |     parser = argparse.ArgumentParser(
 19 |         description="FastReports - Automated Data Analysis Pipeline"
 20 |     )
 21 |     parser.add_argument(
 22 |         "data_path",
 23 |         nargs="?",
 24 |         default="data/layoffs/layoffs.csv",
 25 |         help="Path to the data file"
 26 |     )
 27 |     parser.add_argument(
 28 |         "--dataset-name",
 29 |         default="layoffs",
 30 |         help="Name of the dataset"
 31 |     )
 32 |     parser.add_argument(
 33 |         "--auto-clean",
 34 |         action="store_true",
 35 |         help="Automatically apply cleaning strategies"
 36 |     )
 37 |     parser.add_argument(
 38 |         "--no-viz",
 39 |         action="store_true",
 40 |         help="Skip visualization generation"
 41 |     )
 42 |     
 43 |     args = parser.parse_args()
 44 |     
 45 |     logger.info("=" * 80)
 46 |     logger.info("FastReports - Automated Data Analysis Pipeline")
 47 |     logger.info("IBM Bob Integration Demonstration")
 48 |     logger.info("=" * 80)
 49 |     
 50 |     try:
 51 |         # Initialize Bob session
 52 |         bob_session = get_bob_session_manager()
 53 |         bob_session.start_session(
 54 |             args.dataset_name,
 55 |             "Complete data analysis pipeline execution"
 56 |         )
 57 |         
 58 |         # Log Bob interaction for pipeline planning
 59 |         bob_session.log_interaction(
 60 |             mode="Plan Mode",
 61 |             phase="initialization",
 62 |             prompt="Plan the complete data analysis pipeline execution",
 63 |             response="Pipeline phases: Ingestion → Profiling → Quality Check → Cleaning → Analysis → Visualization → Reporting",
 64 |             success=True,
 65 |             metadata={"dataset": args.dataset_name}
 66 |         )
 67 |         
 68 |         # Initialize and run pipeline
 69 |         pipeline = DataAnalysisPipeline()
 70 |         
 71 |         results = pipeline.run_pipeline(
 72 |             data_path=args.data_path,
 73 |             dataset_name=args.dataset_name,
 74 |             auto_clean=args.auto_clean,
 75 |             generate_visualizations=not args.no_viz
 76 |         )
 77 |         
 78 |         # Log Bob interactions for each phase
 79 |         for phase in pipeline.state['completed_phases']:
 80 |             bob_session.log_interaction(
 81 |                 mode="Code Mode",
 82 |                 phase=phase,
 83 |                 prompt=f"Execute {phase} phase",
 84 |                 response=f"{phase} completed successfully",
 85 |                 success=True
 86 |             )
 87 |         
 88 |         # Print pipeline summary
 89 |         print("\n")
 90 |         print(pipeline.get_pipeline_summary())
 91 |         
 92 |         # Print Bob session summary
 93 |         print("\n")
 94 |         session_summary = bob_session.end_session()
 95 |         print(bob_session.get_session_summary())
 96 |         
 97 |         # Print key results
 98 |         print("\n")
 99 |         print("=" * 80)
100 |         print("KEY RESULTS")
101 |         print("=" * 80)
102 |         
103 |         if 'quality' in results:
104 |             quality_score = results['quality'].get('quality_score', 0)
105 |             print(f"Data Quality Score: {quality_score}/100")
106 |         
107 |         if 'eda' in results:
108 |             findings = results['eda'].get('key_findings', [])
109 |             print(f"\nKey Findings ({len(findings)}):")
110 |             for i, finding in enumerate(findings[:5], 1):
111 |                 print(f"  {i}. {finding}")
112 |         
113 |         if 'visualizations' in results and not results['visualizations'].get('skipped'):
114 |             viz_summary = results['visualizations'].get('summary', {})
115 |             print(f"\nVisualizations Generated: {viz_summary.get('total_charts', 0)}")
116 |         
117 |         print("\n" + "=" * 80)
118 |         print("Pipeline execution completed successfully!")
119 |         print("=" * 80)
120 |         
121 |         return 0
122 |         
123 |     except Exception as e:
124 |         logger.error(f"Pipeline execution failed: {e}", exc_info=True)
125 |         
126 |         # Log failure with Bob
127 |         if 'bob_session' in locals():
128 |             bob_session.log_interaction(
129 |                 mode="Error",
130 |                 phase="execution",
131 |                 prompt="Pipeline execution",
132 |                 response=str(e),
133 |                 success=False
134 |             )
135 |             bob_session.end_session()
136 |         
137 |         return 1
138 | 
139 | 
140 | if __name__ == "__main__":
141 |     sys.exit(main())
142 | 
143 | # Made with Bob
</content>
</file>
<file><path>api_server.py</path>
<content lines="1-370">
  1 | """
  2 | FastReports API Server
  3 | FastAPI backend for the dashboard UI
  4 | """
  5 | 
  6 | import os
  7 | import json
  8 | from pathlib import Path
  9 | from typing import Dict, List, Any, Optional
 10 | import pandas as pd
 11 | import duckdb
 12 | from fastapi import FastAPI, HTTPException, Query
 13 | from fastapi.middleware.cors import CORSMiddleware
 14 | from pydantic import BaseModel
 15 | 
 16 | from src.ingestion.data_loader import DataLoader
 17 | from src.profiling.profiler import DataProfiler
 18 | from src.utils.logger import get_logger
 19 | 
 20 | logger = get_logger("api_server")
 21 | 
 22 | # Initialize FastAPI app
 23 | app = FastAPI(
 24 |     title="FastReports API",
 25 |     description="Backend API for FastReports Dashboard",
 26 |     version="1.0.0"
 27 | )
 28 | 
 29 | # Add CORS middleware
 30 | app.add_middleware(
 31 |     CORSMiddleware,
 32 |     allow_origins=["http://localhost:3000", "http://localhost:5173"],
 33 |     allow_credentials=True,
 34 |     allow_methods=["*"],
 35 |     allow_headers=["*"],
 36 | )
 37 | 
 38 | # Initialize DuckDB connection
 39 | db = duckdb.connect(":memory:")
 40 | 
 41 | # Cache for loaded datasets
 42 | dataset_cache: Dict[str, pd.DataFrame] = {}
 43 | 
 44 | 
 45 | class QueryRequest(BaseModel):
 46 |     """Request model for SQL queries"""
 47 |     query: str
 48 |     data: Optional[List[Dict[str, Any]]] = None
 49 | 
 50 | 
 51 | class DatasetInfo(BaseModel):
 52 |     """Dataset information model"""
 53 |     name: str
 54 |     path: str
 55 |     size: Optional[int] = None
 56 |     rows: Optional[int] = None
 57 |     columns: Optional[int] = None
 58 | 
 59 | 
 60 | @app.get("/")
 61 | async def root():
 62 |     """Root endpoint"""
 63 |     return {
 64 |         "message": "FastReports API Server",
 65 |         "version": "1.0.0",
 66 |         "endpoints": [
 67 |             "/api/datasets",
 68 |             "/api/data",
 69 |             "/api/query",
 70 |             "/api/profile"
 71 |         ]
 72 |     }
 73 | 
 74 | 
 75 | @app.get("/api/datasets")
 76 | async def get_datasets() -> Dict[str, List[DatasetInfo]]:
 77 |     """
 78 |     Get list of available datasets
 79 |     
 80 |     Returns:
 81 |         Dictionary with list of datasets
 82 |     """
 83 |     try:
 84 |         data_dir = Path("data").resolve()
 85 |         datasets = []
 86 |         
 87 |         # Scan data directory for supported files
 88 |         supported_extensions = [".csv", ".xlsx", ".xls", ".json", ".parquet"]
 89 |         
 90 |         if not data_dir.exists():
 91 |             logger.warning(f"Data directory not found: {data_dir}")
 92 |             return {"datasets": []}
 93 |         
 94 |         for root, dirs, files in os.walk(data_dir):
 95 |             for file in files:
 96 |                 file_path = Path(root) / file
 97 |                 if file_path.suffix.lower() in supported_extensions:
 98 |                     try:
 99 |                         # Use relative path from current working directory
100 |                         rel_path = file_path.relative_to(Path.cwd())
101 |                         
102 |                         # Get file size
103 |                         size = file_path.stat().st_size
104 |                         
105 |                         # Create friendly name
106 |                         name = file_path.stem.replace("_", " ").title()
107 |                         
108 |                         datasets.append({
109 |                             "name": name,
110 |                             "path": str(rel_path).replace("\\", "/"),  # Normalize path separators
111 |                             "size": size
112 |                         })
113 |                     except (ValueError, OSError) as e:
114 |                         logger.warning(f"Skipping file {file_path}: {e}")
115 |                         continue
116 |         
117 |         logger.info(f"Found {len(datasets)} datasets")
118 |         return {"datasets": datasets}
119 |         
120 |     except Exception as e:
121 |         logger.error(f"Error listing datasets: {e}")
122 |         raise HTTPException(status_code=500, detail=str(e))
123 | 
124 | 
125 | @app.get("/api/data")
126 | async def get_data(
127 |     path: str = Query(..., description="Path to the dataset file"),
128 |     limit: Optional[int] = Query(None, description="Limit number of rows returned"),
129 |     offset: Optional[int] = Query(0, description="Offset for pagination")
130 | ) -> Dict[str, Any]:
131 |     """
132 |     Load and return dataset
133 |     
134 |     Args:
135 |         path: Path to the dataset file
136 |         limit: Maximum number of rows to return
137 |         offset: Number of rows to skip
138 |         
139 |     Returns:
140 |         Dictionary with data, columns, and statistics
141 |     """
142 |     try:
143 |         logger.info(f"Loading dataset: {path}")
144 |         
145 |         # Check if dataset is in cache
146 |         if path in dataset_cache:
147 |             df = dataset_cache[path]
148 |             logger.info(f"Loaded from cache: {len(df)} rows")
149 |         else:
150 |             # Load dataset
151 |             loader = DataLoader()
152 |             result = loader.load_data(path)
153 |             
154 |             # Extract DataFrame from result
155 |             if isinstance(result, dict):
156 |                 df = result.get('dataframe')
157 |                 if df is None:
158 |                     raise ValueError("DataLoader did not return a dataframe")
159 |             else:
160 |                 df = result
161 |             
162 |             # Cache the dataset
163 |             dataset_cache[path] = df
164 |             logger.info(f"Loaded and cached: {len(df)} rows")
165 |         
166 |         # Apply pagination
167 |         total_rows = len(df)
168 |         if limit:
169 |             df_subset = df.iloc[offset:offset + limit]
170 |         else:
171 |             df_subset = df.iloc[offset:]
172 |         
173 |         # Convert to records
174 |         data = df_subset.to_dict(orient="records")
175 |         columns = df.columns.tolist()
176 |         
177 |         # Get basic statistics
178 |         profiler = DataProfiler()
179 |         profile = profiler.profile_dataframe(df)
180 |         
181 |         # Calculate quality score
182 |         quality_score = calculate_quality_score(profile)
183 |         
184 |         return {
185 |             "data": data,
186 |             "columns": columns,
187 |             "total_rows": total_rows,
188 |             "returned_rows": len(data),
189 |             "stats": {
190 |                 "quality_score": quality_score,
191 |                 "missing_values": profile.get("missing_summary", {}),
192 |                 "data_types": profile.get("column_types", {})
193 |             }
194 |         }
195 |         
196 |     except FileNotFoundError:
197 |         raise HTTPException(status_code=404, detail=f"Dataset not found: {path}")
198 |     except Exception as e:
199 |         logger.error(f"Error loading dataset: {e}", exc_info=True)
200 |         raise HTTPException(status_code=500, detail=str(e))
201 | 
202 | 
203 | @app.post("/api/query")
204 | async def execute_query(request: QueryRequest) -> Dict[str, Any]:
205 |     """
206 |     Execute SQL query on dataset
207 |     
208 |     Args:
209 |         request: Query request with SQL and optional data
210 |         
211 |     Returns:
212 |         Query results
213 |     """
214 |     try:
215 |         logger.info(f"Executing query: {request.query[:100]}...")
216 |         
217 |         # If data is provided, create temporary table
218 |         if request.data:
219 |             df = pd.DataFrame(request.data)
220 |             db.register("temp_data", df)
221 |             table_name = "temp_data"
222 |         else:
223 |             # Use the last loaded dataset from cache
224 |             if not dataset_cache:
225 |                 raise HTTPException(
226 |                     status_code=400,
227 |                     detail="No dataset loaded. Please load a dataset first."
228 |                 )
229 |             
230 |             # Get the most recently loaded dataset
231 |             last_path = list(dataset_cache.keys())[-1]
232 |             df = dataset_cache[last_path]
233 |             db.register("temp_data", df)
234 |             table_name = "temp_data"
235 |         
236 |         # Execute query
237 |         result = db.execute(request.query).fetchdf()
238 |         
239 |         # Convert to records
240 |         data = result.to_dict(orient="records")
241 |         columns = result.columns.tolist()
242 |         
243 |         return {
244 |             "data": data,
245 |             "columns": columns,
246 |             "rows": len(data),
247 |             "success": True
248 |         }
249 |         
250 |     except Exception as e:
251 |         logger.error(f"Query execution error: {e}")
252 |         raise HTTPException(
253 |             status_code=400,
254 |             detail=f"Query execution failed: {str(e)}"
255 |         )
256 | 
257 | 
258 | @app.get("/api/profile")
259 | async def get_profile(
260 |     path: str = Query(..., description="Path to the dataset file")
261 | ) -> Dict[str, Any]:
262 |     """
263 |     Get detailed profile of a dataset
264 |     
265 |     Args:
266 |         path: Path to the dataset file
267 |         
268 |     Returns:
269 |         Detailed profiling information
270 |     """
271 |     try:
272 |         logger.info(f"Profiling dataset: {path}")
273 |         
274 |         # Load dataset if not in cache
275 |         if path not in dataset_cache:
276 |             loader = DataLoader()
277 |             result = loader.load_data(path)
278 |             
279 |             # Extract DataFrame from result
280 |             if isinstance(result, dict):
281 |                 df = result.get('dataframe')
282 |                 if df is None:
283 |                     raise ValueError("DataLoader did not return a dataframe")
284 |             else:
285 |                 df = result
286 |             
287 |             dataset_cache[path] = df
288 |         else:
289 |             df = dataset_cache[path]
290 |         
291 |         # Profile the dataset
292 |         profiler = DataProfiler()
293 |         profile = profiler.profile_dataframe(df)
294 |         
295 |         # Add quality score
296 |         profile["quality_score"] = calculate_quality_score(profile)
297 |         
298 |         return profile
299 |         
300 |     except Exception as e:
301 |         logger.error(f"Error profiling dataset: {e}")
302 |         raise HTTPException(status_code=500, detail=str(e))
303 | 
304 | 
305 | def calculate_quality_score(profile: Dict[str, Any]) -> float:
306 |     """
307 |     Calculate overall data quality score
308 |     
309 |     Args:
310 |         profile: Data profile dictionary
311 |         
312 |     Returns:
313 |         Quality score (0-100)
314 |     """
315 |     score = 100.0
316 |     
317 |     # Deduct for missing values
318 |     missing_summary = profile.get("missing_summary", {})
319 |     total_missing = missing_summary.get("total_missing", 0)
320 |     total_values = missing_summary.get("total_values", 1)
321 |     missing_pct = (total_missing / total_values) * 100 if total_values > 0 else 0
322 |     score -= missing_pct * 0.5  # Deduct up to 50 points for missing values
323 |     
324 |     # Deduct for duplicates
325 |     duplicates = profile.get("duplicates", {})
326 |     duplicate_count = duplicates.get("count", 0)
327 |     total_rows = profile.get("shape", {}).get("rows", 1)
328 |     duplicate_pct = (duplicate_count / total_rows) * 100 if total_rows > 0 else 0
329 |     score -= duplicate_pct * 0.3  # Deduct up to 30 points for duplicates
330 |     
331 |     # Ensure score is between 0 and 100
332 |     return max(0.0, min(100.0, round(score, 2)))
333 | 
334 | 
335 | @app.on_event("startup")
336 | async def startup_event():
337 |     """Startup event handler"""
338 |     logger.info("FastReports API Server starting...")
339 |     logger.info("Available endpoints:")
340 |     logger.info("  GET  /api/datasets - List available datasets")
341 |     logger.info("  GET  /api/data - Load dataset")
342 |     logger.info("  POST /api/query - Execute SQL query")
343 |     logger.info("  GET  /api/profile - Get dataset profile")
344 | 
345 | 
346 | @app.on_event("shutdown")
347 | async def shutdown_event():
348 |     """Shutdown event handler"""
349 |     logger.info("FastReports API Server shutting down...")
350 |     db.close()
351 | 
352 | 
353 | if __name__ == "__main__":
354 |     import uvicorn
355 |     
356 |     # Get configuration
357 |     port = int(os.getenv("API_PORT", "8000"))
358 |     host = os.getenv("API_HOST", "0.0.0.0")
359 |     
360 |     logger.info(f"Starting server on {host}:{port}")
361 |     
362 |     uvicorn.run(
363 |         "api_server:app",
364 |         host=host,
365 |         port=port,
366 |         reload=True,
367 |         log_level="info"
368 |     )
369 | 
370 | # Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
IMPLEMENTATION_STATUS.md,output/pizza_delivery_analysis.json

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T20:01:17.246Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.01

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Based on my analysis of the FastReports project, I can now provide you with a comprehensive overview of the user flow.

<attempt_completion>
<result>
# FastReports User Flow

## Overview
FastReports offers **three distinct user flows** depending on how users want to interact with the system:

---

## **Flow 1: Command-Line Pipeline (Automated Analysis)**

### User Journey:
1. **Start**: User runs `python main.py [data_path]` with optional flags
2. **Data Ingestion**: System automatically detects file format (CSV, XLSX, JSON, Parquet) and loads data
3. **Data Profiling**: Analyzes data characteristics, distributions, and quality metrics
4. **Quality Check**: Calculates quality score (0-100) based on:
   - Missing values (30 pts)
   - Duplicates (20 pts)
   - Outliers (20 pts)
   - Consistency (15 pts)
   - Completeness (15 pts)
5. **Decision Point**: 
   - If quality score < 70 OR user uses `--auto-clean` flag → Data Cleaning
   - If quality score ≥ 70 → Skip to Analysis
6. **Data Cleaning** (if needed): Applies transformations (imputation, standardization, validation)
7. **Statistical Analysis**: Performs descriptive stats, correlations, hypothesis testing
8. **EDA Report**: Generates key findings and recommendations
9. **Visualization** (unless `--no-viz` flag): Creates 9+ chart types (histogram, box plot, scatter, heatmap, etc.)
10. **Output**: 
    - Console summary with key results
    - Log files in `output/logs/`
    - Bob session logs in `bob_sessions/`
    - Processed data in `processed_data/`

### Command Examples:
```bash
# Default run
python main.py

# Specific dataset with auto-cleaning
python main.py data/soccer/laliga_22_23.csv --dataset-name laliga --auto-clean

# Skip visualizations
python main.py --no-viz
```

---

## **Flow 2: API Server (Programmatic Access)**

### User Journey:
1. **Start**: User starts API server via `./start_server.sh` or `python api_server.py`
2. **Server Ready**: API available at `http://localhost:8000`
3. **Discover Datasets**: `GET /api/datasets` - Lists all available datasets in `data/` directory
4. **Load Dataset**: `GET /api/data?path=...&limit=100&offset=0` - Loads data with pagination
5. **Query Data**: `POST /api/query` - Execute SQL queries using DuckDB engine
6. **Profile Dataset**: `GET /api/profile?path=...` - Get detailed profiling information
7. **Integration**: Use API from any client (Python, JavaScript, cURL, etc.)

### API Endpoints:
- **GET** `/` - API information
- **GET** `/api/datasets` - List datasets
- **GET** `/api/data` - Load dataset with pagination
- **POST** `/api/query` - Execute SQL queries
- **GET** `/api/profile` - Get dataset profile

---

## **Flow 3: Interactive Dashboard (Web UI)**

### User Journey:
1. **Start**: User runs `./start_all.sh` to start both API server and dashboard
2. **Access Dashboard**: Opens browser to `http://localhost:3000`
3. **Select Dataset**: Choose from dropdown of available datasets
4. **View Data**: 
   - Paginated table view with search/filter
   - Real-time data quality score display
   - Column type information
5. **Query Builder**: 
   - Write custom SQL queries using DuckDB
   - Execute queries and see results instantly
6. **Visualize**: 
   - Select chart type (bar, line, scatter, pie, histogram, box)
   - Choose X/Y axes from columns
   - Interactive Plotly charts with zoom, pan, hover
7. **Export**: Download filtered/queried data as CSV
8. **Iterate**: Refine queries and visualizations in real-time

### Dashboard Features:
- **Real-time filtering** and search
- **SQL query builder** with DuckDB
- **Interactive visualizations** (Plotly)
- **Multiple chart types**
- **CSV export**
- **Responsive design** (Preact-based, 3KB framework)

---

## **IBM Bob Integration Throughout**

Bob is integrated at every phase as an AI development partner:

### Planning Phase (Plan Mode):
- Architecture design
- Pipeline workflow planning
- Strategy recommendations

### Implementation Phase (Code Mode):
- Module implementation
- Data transformations
- Visualization code generation

### Analysis Phase (Advanced Mode - Conceptual):
- Statistical test selection
- Insight generation
- Complex queries

### Session Tracking:
- All Bob interactions logged in `bob_sessions/`
- Usage analytics and mode tracking
- Export capabilities for review

---

## **Key Decision Points**

1. **Quality Threshold**: Score < 70 triggers automatic cleaning recommendation
2. **Auto-clean Flag**: Bypasses user approval for cleaning
3. **Visualization Flag**: `--no-viz` skips chart generation
4. **Mode Selection**: CLI vs API vs Dashboard based on use case

---

## **Output Locations**

- **Logs**: `output/logs/fastreports_*.log`
- **Bob Sessions**: `bob_sessions/{timestamp}_session.log`
- **Processed Data**: `processed_data/{dataset_name}/`
- **Reports**: Console output + structured JSON
- **Visualizations**: Generated charts (when enabled)

---

## **Typical Runtime**
- **30-60 seconds** per dataset
- **200-500 MB** memory usage
- **Multiple output files** (logs, sessions, processed data)
</result>
</attempt_completion>

