"""
FastReports API Server
FastAPI backend for the dashboard UI
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
import duckdb
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.ingestion.data_loader import DataLoader
from src.profiling.profiler import DataProfiler
from src.utils.logger import get_logger

logger = get_logger("api_server")

# Initialize FastAPI app
app = FastAPI(
    title="FastReports API",
    description="Backend API for FastReports Dashboard",
    version="1.0.0"
)

# Add CORS middleware
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173,https://fastreports.netlify.app"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DuckDB connection
db = duckdb.connect(":memory:")

# Cache for loaded datasets
dataset_cache: Dict[str, pd.DataFrame] = {}


class QueryRequest(BaseModel):
    """Request model for SQL queries"""
    query: str
    data: Optional[List[Dict[str, Any]]] = None


class DatasetInfo(BaseModel):
    """Dataset information model"""
    name: str
    path: str
    size: Optional[int] = None
    rows: Optional[int] = None
    columns: Optional[int] = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FastReports API Server",
        "version": "1.0.0",
        "endpoints": [
            "/api/datasets",
            "/api/data",
            "/api/query",
            "/api/profile"
        ]
    }


@app.get("/api/datasets")
async def get_datasets() -> Dict[str, List[DatasetInfo]]:
    """
    Get list of available datasets
    
    Returns:
        Dictionary with list of datasets
    """
    try:
        datasets = []
        supported_extensions = [".csv", ".xlsx", ".xls", ".json", ".parquet"]

        # Scan both data/ and uploads/ directories
        scan_dirs = [Path("data").resolve(), Path("uploads").resolve()]

        for data_dir in scan_dirs:
            if not data_dir.exists():
                continue

            for root, dirs, files in os.walk(data_dir):
                for file in files:
                    if file == ".gitkeep":
                        continue
                    file_path = Path(root) / file
                    if file_path.suffix.lower() in supported_extensions:
                        try:
                            rel_path = file_path.relative_to(Path.cwd())
                            size = file_path.stat().st_size
                            name = file_path.stem.replace("_", " ").title()

                            datasets.append({
                                "name": name,
                                "path": str(rel_path).replace("\\", "/"),
                                "size": size
                            })
                        except (ValueError, OSError) as e:
                            logger.warning(f"Skipping file {file_path}: {e}")
                            continue

        logger.info(f"Found {len(datasets)} datasets")
        return {"datasets": datasets}
        
    except Exception as e:
        logger.error(f"Error listing datasets: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data")
async def get_data(
    path: str = Query(..., description="Path to the dataset file"),
    limit: Optional[int] = Query(None, description="Limit number of rows returned"),
    offset: Optional[int] = Query(0, description="Offset for pagination")
) -> Dict[str, Any]:
    """
    Load and return dataset
    
    Args:
        path: Path to the dataset file
        limit: Maximum number of rows to return
        offset: Number of rows to skip
        
    Returns:
        Dictionary with data, columns, and statistics
    """
    try:
        logger.info(f"Loading dataset: {path}")
        
        # Check if dataset is in cache
        if path in dataset_cache:
            df = dataset_cache[path]
            logger.info(f"Loaded from cache: {len(df)} rows")
        else:
            # Load dataset
            loader = DataLoader()
            result = loader.load_data(path)
            
            # Extract DataFrame from result
            if isinstance(result, dict):
                df = result.get('dataframe')
                if df is None:
                    raise ValueError("DataLoader did not return a dataframe")
            else:
                df = result
            
            # Cache the dataset
            dataset_cache[path] = df
            logger.info(f"Loaded and cached: {len(df)} rows")
        
        # Apply pagination
        total_rows = len(df)
        if limit:
            df_subset = df.iloc[offset:offset + limit]
        else:
            df_subset = df.iloc[offset:]
        
        # Convert to records
        data = df_subset.to_dict(orient="records")
        columns = df.columns.tolist()
        
        # Get basic statistics
        profiler = DataProfiler()
        profile = profiler.profile_dataframe(df)
        
        # Calculate quality score
        quality_score = calculate_quality_score(profile)
        
        return {
            "data": data,
            "columns": columns,
            "total_rows": total_rows,
            "returned_rows": len(data),
            "stats": {
                "quality_score": quality_score,
                "missing_values": profile.get("missing_summary", {}),
                "data_types": profile.get("column_types", {})
            }
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Dataset not found: {path}")
    except Exception as e:
        logger.error(f"Error loading dataset: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/query")
async def execute_query(request: QueryRequest) -> Dict[str, Any]:
    """
    Execute SQL query on dataset
    
    Args:
        request: Query request with SQL and optional data
        
    Returns:
        Query results
    """
    try:
        logger.info(f"Executing query: {request.query[:100]}...")
        
        # If data is provided, create temporary table
        if request.data:
            df = pd.DataFrame(request.data)
        else:
            # Use the last loaded dataset from cache
            if not dataset_cache:
                raise HTTPException(
                    status_code=400,
                    detail="No dataset loaded. Please load a dataset first."
                )
            
            # Get the most recently loaded dataset
            last_path = list(dataset_cache.keys())[-1]
            df = dataset_cache[last_path]
        
        # Register the dataframe with multiple common table names
        # This allows users to use 'data', 'temp_data', or 'df' in their queries
        db.register("data", df)
        db.register("temp_data", df)
        db.register("df", df)
        
        # Replace common table name variations in the query
        query = request.query
        
        # Execute query
        result = db.execute(query).fetchdf()
        
        # Convert to records
        data = result.to_dict(orient="records")
        columns = result.columns.tolist()
        
        logger.info(f"Query executed successfully, returned {len(data)} rows")
        
        return {
            "data": data,
            "columns": columns,
            "rows": len(data),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Query execution error: {e}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail=f"Query execution failed: {str(e)}"
        )


@app.get("/api/profile")
async def get_profile(
    path: str = Query(..., description="Path to the dataset file")
) -> Dict[str, Any]:
    """
    Get detailed profile of a dataset
    
    Args:
        path: Path to the dataset file
        
    Returns:
        Detailed profiling information
    """
    try:
        logger.info(f"Profiling dataset: {path}")
        
        # Load dataset if not in cache
        if path not in dataset_cache:
            loader = DataLoader()
            result = loader.load_data(path)
            
            # Extract DataFrame from result
            if isinstance(result, dict):
                df = result.get('dataframe')
                if df is None:
                    raise ValueError("DataLoader did not return a dataframe")
            else:
                df = result
            
            dataset_cache[path] = df
        else:
            df = dataset_cache[path]
        
        # Profile the dataset
        profiler = DataProfiler()
        profile = profiler.profile_dataframe(df)
        
        # Add quality score
        profile["quality_score"] = calculate_quality_score(profile)
        
        return profile
        
    except Exception as e:
        logger.error(f"Error profiling dataset: {e}")
        raise HTTPException(status_code=500, detail=str(e))


SUPPORTED_UPLOAD_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json", ".parquet"}
MAX_UPLOAD_SIZE_MB = 100


@app.post("/api/upload")
async def upload_dataset(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload a dataset file for analysis.

    Returns:
        Metadata about the uploaded dataset including path, rows, and columns.
    """
    ext = Path(file.filename).suffix.lower()
    if ext not in SUPPORTED_UPLOAD_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Supported: {', '.join(sorted(SUPPORTED_UPLOAD_EXTENSIONS))}"
        )

    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    dest = uploads_dir / file.filename

    try:
        contents = await file.read()
        if len(contents) > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {MAX_UPLOAD_SIZE_MB} MB."
            )

        with open(dest, "wb") as f:
            f.write(contents)

        loader = DataLoader()
        result = loader.load_data(str(dest))
        df = result.get("dataframe") if isinstance(result, dict) else result
        if df is None:
            dest.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail="Could not parse uploaded file.")

        rel_path = str(dest).replace("\\", "/")
        dataset_cache[rel_path] = df

        name = dest.stem.replace("_", " ").title()

        logger.info(f"Uploaded dataset '{file.filename}': {len(df)} rows, {len(df.columns)} cols")

        return {
            "name": name,
            "path": rel_path,
            "rows": len(df),
            "columns": df.columns.tolist(),
            "size": len(contents)
        }

    except HTTPException:
        raise
    except Exception as e:
        dest.unlink(missing_ok=True)
        logger.error(f"Upload failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


def calculate_quality_score(profile: Dict[str, Any]) -> float:
    """
    Calculate overall data quality score
    
    Args:
        profile: Data profile dictionary
        
    Returns:
        Quality score (0-100)
    """
    score = 100.0
    
    # Deduct for missing values
    missing_summary = profile.get("missing_summary", {})
    total_missing = missing_summary.get("total_missing", 0)
    total_values = missing_summary.get("total_values", 1)
    missing_pct = (total_missing / total_values) * 100 if total_values > 0 else 0
    score -= missing_pct * 0.5  # Deduct up to 50 points for missing values
    
    # Deduct for duplicates
    duplicates = profile.get("duplicates", {})
    duplicate_count = duplicates.get("count", 0)
    total_rows = profile.get("shape", {}).get("rows", 1)
    duplicate_pct = (duplicate_count / total_rows) * 100 if total_rows > 0 else 0
    score -= duplicate_pct * 0.3  # Deduct up to 30 points for duplicates
    
    # Ensure score is between 0 and 100
    return max(0.0, min(100.0, round(score, 2)))


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("FastReports API Server starting...")
    logger.info("Available endpoints:")
    logger.info("  GET  /api/datasets - List available datasets")
    logger.info("  GET  /api/data - Load dataset")
    logger.info("  POST /api/query - Execute SQL query")
    logger.info("  GET  /api/profile - Get dataset profile")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("FastReports API Server shutting down...")
    db.close()


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration
    port = int(os.getenv("API_PORT", "8000"))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

# Made with Bob