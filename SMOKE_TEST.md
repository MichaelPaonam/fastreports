# FastReports - Smoke Test Guide

## Quick Smoke Test (5 minutes)

This guide will help you verify that FastReports is working correctly.

## Prerequisites

```bash
# 1. Check Python version (3.10+ required)
python --version

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify installation
pip list | grep -E "pandas|numpy|plotly|scipy|pyyaml|openpyxl"
```

## Test 1: Basic Pipeline Execution ✅

**What it tests**: Complete pipeline with default dataset

```bash
# Run the pipeline
python main.py

# Expected output:
# - "FastReports - Automated Data Analysis Pipeline"
# - Phase completion messages (Ingestion, Profiling, Quality, etc.)
# - Quality score (should be around 72-75/100 for layoffs dataset)
# - Key findings (5 items)
# - "Pipeline execution completed successfully!"
```

**Success Criteria**:
- ✅ No errors or exceptions
- ✅ All phases complete (6-7 phases)
- ✅ Quality score displayed
- ✅ Bob session summary shown
- ✅ Exit code 0

**Expected Runtime**: 30-60 seconds

## Test 2: Different Dataset ✅

**What it tests**: Pipeline with soccer dataset

```bash
# Run with soccer data
python main.py data/soccer/laliga_22_23.csv --dataset-name laliga

# Expected output:
# - Successfully loads CSV file
# - Higher quality score (soccer data is cleaner)
# - Time series analysis detected
# - More visualizations generated
```

**Success Criteria**:
- ✅ Loads different file format
- ✅ Completes all phases
- ✅ Different quality score than layoffs
- ✅ No errors

## Test 3: Auto-Clean Mode ✅

**What it tests**: Automatic data cleaning

```bash
# Run with auto-clean enabled
python main.py --auto-clean

# Expected output:
# - Cleaning phase executes
# - Strategies applied (shown in logs)
# - Validation report displayed
# - Cleaned data shape shown
```

**Success Criteria**:
- ✅ Cleaning phase runs
- ✅ Validation report shows improvements
- ✅ Quality score may improve
- ✅ No data corruption

## Test 4: Skip Visualizations ✅

**What it tests**: Pipeline without visualization phase

```bash
# Run without visualizations
python main.py --no-viz

# Expected output:
# - Faster execution
# - Visualization phase skipped
# - All other phases complete
```

**Success Criteria**:
- ✅ Faster runtime (20-30 seconds)
- ✅ "Visualization skipped" message
- ✅ Other phases complete normally

## Test 5: Output Verification ✅

**What it tests**: Generated files and logs

```bash
# Check output directories
ls -la output/logs/
ls -la bob_sessions/
ls -la processed_data/

# Expected files:
# - output/logs/fastreports_*.log (log file)
# - bob_sessions/layoffs_*.json (Bob session log)
# - processed_data/layoffs/ (processed data directory)
```

**Success Criteria**:
- ✅ Log file created with content
- ✅ Bob session JSON file exists
- ✅ Processed data directory created
- ✅ Metadata files present

## Test 6: Log Content Verification ✅

**What it tests**: Logging functionality

```bash
# View the latest log
cat output/logs/fastreports_*.log | tail -50

# Should contain:
# - Phase start/end markers
# - Quality scores
# - Statistics
# - No ERROR messages (warnings OK)
```

**Success Criteria**:
- ✅ Structured log entries
- ✅ Timestamps present
- ✅ Phase markers visible
- ✅ No critical errors

## Test 7: Bob Session Verification ✅

**What it tests**: Bob integration tracking

```bash
# View Bob session
cat bob_sessions/layoffs_*.json | python -m json.tool

# Should contain:
# - session_id
# - interactions array
# - modes_used
# - total_prompts count
```

**Success Criteria**:
- ✅ Valid JSON format
- ✅ Multiple interactions logged
- ✅ Modes tracked (Plan Mode, Code Mode)
- ✅ Timestamps present

## Test 8: Module Import Test ✅

**What it tests**: All modules can be imported

```bash
# Test imports
python -c "
from src.ingestion.data_loader import DataLoader
from src.profiling.profiler import DataProfiler
from src.profiling.quality_checker import QualityChecker
from src.cleaning.strategy_generator import CleaningStrategyGenerator
from src.cleaning.transformers import DataTransformer
from src.cleaning.validator import DataValidator
from src.analysis.statistics import StatisticalAnalyzer
from src.analysis.eda import EDAReportGenerator
from src.visualization.chart_generator import ChartGenerator
from src.visualization.plotly_charts import PlotlyChartBuilder
from src.visualization.recommender import VisualizationRecommender
from src.orchestration.pipeline import DataAnalysisPipeline
from src.bob_integration.session_manager import get_bob_session_manager
from src.bob_integration.prompt_templates import BobPromptTemplates
print('✅ All modules imported successfully!')
"
```

**Success Criteria**:
- ✅ No import errors
- ✅ Success message displayed

## Test 9: Help Command ✅

**What it tests**: CLI interface

```bash
# Show help
python main.py --help

# Should display:
# - Usage information
# - Available arguments
# - Default values
```

**Success Criteria**:
- ✅ Help text displays
- ✅ All options listed
- ✅ No errors

## Test 10: Error Handling ✅

**What it tests**: Graceful error handling

```bash
# Test with non-existent file
python main.py nonexistent.csv --dataset-name test

# Expected:
# - Error message displayed
# - No crash
# - Exit code 1
```

**Success Criteria**:
- ✅ Error message shown
- ✅ No stack trace (or clean error)
- ✅ Graceful exit

## Quick Verification Checklist

Run through this checklist for a complete smoke test:

```bash
# 0. Setup virtual environment
[ ] python -m venv venv
[ ] source venv/bin/activate  # or venv\Scripts\activate on Windows

# 1. Install dependencies
[ ] pip install -r requirements.txt

# 2. Run basic test
[ ] python main.py
[ ] Check for "Pipeline execution completed successfully!"

# 3. Verify outputs
[ ] ls output/logs/
[ ] ls bob_sessions/
[ ] ls processed_data/

# 4. Test different dataset
[ ] python main.py data/soccer/laliga_22_23.csv --dataset-name laliga

# 5. Test auto-clean
[ ] python main.py --auto-clean

# 6. Check logs
[ ] cat output/logs/fastreports_*.log | grep "ERROR"
[ ] Should return nothing or only warnings

# 7. Verify Bob session
[ ] cat bob_sessions/*.json | python -m json.tool
[ ] Should show valid JSON with interactions
```

## Expected Console Output (Sample)

```
================================================================================
FastReports - Automated Data Analysis Pipeline
IBM Bob Integration Demonstration
================================================================================

[INFO] Starting Data Analysis Pipeline for: layoffs
[INFO] ════════════════════════════════════════════════════════════════════════
[INFO] PHASE: Data Ingestion
[INFO] ════════════════════════════════════════════════════════════════════════
[INFO] Loaded dataset: layoffs
[INFO] Shape: (2361, 9)
[INFO] Working directory: processed_data/layoffs
[INFO] ✓ Phase completed successfully

[INFO] ════════════════════════════════════════════════════════════════════════
[INFO] PHASE: Data Profiling
[INFO] ════════════════════════════════════════════════════════════════════════
[INFO] Profile generated successfully
[INFO] ✓ Phase completed successfully

[INFO] ════════════════════════════════════════════════════════════════════════
[INFO] PHASE: Quality Checking
[INFO] ════════════════════════════════════════════════════════════════════════
[INFO] Quality Score: 72.5/100
[INFO] ✓ Phase completed successfully

... (more phases) ...

================================================================================
PIPELINE EXECUTION SUMMARY
================================================================================

Duration: 45.23 seconds
Completed Phases: 7
  ✓ ingestion
  ✓ profiling
  ✓ quality_checking
  ✓ statistical_analysis
  ✓ eda
  ✓ visualization

================================================================================

KEY RESULTS
================================================================================
Data Quality Score: 72.5/100

Key Findings (5):
  1. Large dataset with 2,361 rows - suitable for robust analysis
  2. Significant missing data (15.3%) requires attention
  3. Found 3 strong correlations between variables
  4. 2 variables show non-normal distributions
  5. Outliers detected in 3 columns

Visualizations Generated: 15

================================================================================
Pipeline execution completed successfully!
================================================================================
```

## Troubleshooting

### Issue: Import errors

```bash
# Solution: Install missing packages
pip install pandas numpy plotly scipy pyyaml openpyxl
```

### Issue: File not found

```bash
# Solution: Check data directory exists
ls -la data/layoffs/layoffs.csv

# If missing, verify you're in the project root
pwd
# Should end with /fastreports
```

### Issue: Permission errors

```bash
# Solution: Create output directories
mkdir -p output/logs bob_sessions processed_data
chmod 755 output bob_sessions processed_data
```

### Issue: Memory errors

```bash
# Solution: Use smaller dataset or skip visualizations
python main.py --no-viz
```

## Performance Benchmarks

Expected performance on standard hardware:

| Dataset | Rows | Columns | Runtime | Memory |
|---------|------|---------|---------|--------|
| Layoffs | 2,361 | 9 | 30-60s | ~200MB |
| Soccer | 380 | 100+ | 45-90s | ~300MB |
| Pizza | ~1,000 | 15 | 40-70s | ~250MB |

## Success Indicators

✅ **All tests pass if**:
1. No Python exceptions or errors
2. All phases complete successfully
3. Output files are created
4. Bob sessions are logged
5. Quality scores are calculated
6. Visualizations are generated (unless --no-viz)
7. Console output is clean and informative
8. Exit code is 0

## Quick One-Liner Test

```bash
# Run all basic tests in sequence
python main.py && \
python main.py data/soccer/laliga_22_23.csv --dataset-name laliga && \
python main.py --auto-clean && \
echo "✅ All smoke tests passed!"
```

## Next Steps After Smoke Test

If all tests pass:
1. ✅ Review generated logs in `output/logs/`
2. ✅ Examine Bob sessions in `bob_sessions/`
3. ✅ Check processed data in `processed_data/`
4. ✅ Read the comprehensive reports in console output
5. ✅ Try with your own datasets!

---

**Estimated Total Test Time**: 5-10 minutes
**Required**: Python 3.10+, ~500MB disk space, ~1GB RAM

---

*Made with IBM Bob* 🤖