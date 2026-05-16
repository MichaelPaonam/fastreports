# FastReports API Documentation

## Overview

The FastReports API provides a RESTful interface for data analysis and visualization. Built with FastAPI, it offers high performance, automatic API documentation, and seamless integration with the dashboard UI.

**Base URL:** `http://localhost:8000`  
**API Documentation:** `http://localhost:8000/docs` (Swagger UI)  
**Alternative Docs:** `http://localhost:8000/redoc` (ReDoc)

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the API Server

**Linux/macOS:**
```bash
chmod +x start_server.sh
./start_server.sh
```

**Windows:**
```cmd
start_server.bat
```

**Or directly with Python:**
```bash
python api_server.py
```

### 3. Start Both API and Dashboard

**Linux/macOS:**
```bash
chmod +x start_all.sh
./start_all.sh
```

---

## API Endpoints

### 1. Root Endpoint

**GET** `/`

Get API information and available endpoints.

**Response:**
```json
{
  "message": "FastReports API Server",
  "version": "1.0.0",
  "endpoints": [
    "/api/datasets",
    "/api/data",
    "/api/query",
    "/api/profile"
  ]
}
```

---

### 2. List Datasets

**GET** `/api/datasets`

Get a list of all available datasets in the `data/` directory.

**Response:**
```json
{
  "datasets": [
    {
      "name": "Laliga 24 25",
      "path": "data/soccer/laliga_24_25.csv",
      "size": 45678
    },
    {
      "name": "Layoffs",
      "path": "data/layoffs/layoffs.csv",
      "size": 123456
    }
  ]
}
```

**Supported File Formats:**
- CSV (`.csv`)
- Excel (`.xlsx`, `.xls`)
- JSON (`.json`)
- Parquet (`.parquet`)

---

### 3. Load Dataset

**GET** `/api/data`

Load and return dataset with optional pagination.

**Query Parameters:**
- `path` (required): Path to the dataset file
- `limit` (optional): Maximum number of rows to return
- `offset` (optional): Number of rows to skip (default: 0)

**Example Request:**
```
GET /api/data?path=data/soccer/laliga_24_25.csv&limit=100&offset=0
```

**Response:**
```json
{
  "data": [
    {
      "team": "Real Madrid",
      "points": 85,
      "goals": 78
    }
  ],
  "columns": ["team", "points", "goals"],
  "total_rows": 380,
  "returned_rows": 100,
  "stats": {
    "quality_score": 95.5,
    "missing_values": {
      "total_missing": 5,
      "total_values": 1140
    },
    "data_types": {
      "team": "object",
      "points": "int64",
      "goals": "int64"
    }
  }
}
```

---

### 4. Execute SQL Query

**POST** `/api/query`

Execute SQL queries on datasets using DuckDB.

**Request Body:**
```json
{
  "query": "SELECT team, points FROM temp_data WHERE points > 70 ORDER BY points DESC",
  "data": [
    {"team": "Real Madrid", "points": 85},
    {"team": "Barcelona", "points": 82}
  ]
}
```

**Note:** If `data` is not provided, the query will run on the most recently loaded dataset.

**Response:**
```json
{
  "data": [
    {"team": "Real Madrid", "points": 85},
    {"team": "Barcelona", "points": 82}
  ],
  "columns": ["team", "points"],
  "rows": 2,
  "success": true
}
```

**SQL Examples:**

```sql
-- Filter data
SELECT * FROM temp_data WHERE column_name > 100

-- Aggregate data
SELECT category, COUNT(*), AVG(value) 
FROM temp_data 
GROUP BY category

-- Join operations (if multiple tables registered)
SELECT a.*, b.value 
FROM temp_data a 
LEFT JOIN other_table b ON a.id = b.id

-- Window functions
SELECT *, 
       ROW_NUMBER() OVER (PARTITION BY category ORDER BY value DESC) as rank
FROM temp_data
```

---

### 5. Get Dataset Profile

**GET** `/api/profile`

Get detailed profiling information about a dataset.

**Query Parameters:**
- `path` (required): Path to the dataset file

**Example Request:**
```
GET /api/profile?path=data/soccer/laliga_24_25.csv
```

**Response:**
```json
{
  "shape": {
    "rows": 380,
    "columns": 15
  },
  "column_types": {
    "team": "object",
    "points": "int64",
    "goals": "int64"
  },
  "missing_summary": {
    "total_missing": 5,
    "total_values": 5700,
    "missing_percentage": 0.088
  },
  "duplicates": {
    "count": 0,
    "percentage": 0.0
  },
  "quality_score": 95.5,
  "numeric_stats": {
    "points": {
      "mean": 45.2,
      "median": 44.0,
      "std": 15.3,
      "min": 10,
      "max": 85
    }
  }
}
```

---

## Error Handling

The API uses standard HTTP status codes:

- **200 OK**: Request successful
- **400 Bad Request**: Invalid request parameters or query
- **404 Not Found**: Dataset not found
- **500 Internal Server Error**: Server error

**Error Response Format:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Configuration

### Environment Variables

- `API_HOST`: Server host (default: `0.0.0.0`)
- `API_PORT`: Server port (default: `8000`)

**Example:**
```bash
export API_HOST=localhost
export API_PORT=9000
python api_server.py
```

### CORS Configuration

The API allows requests from:
- `http://localhost:3000` (Dashboard dev server)
- `http://localhost:5173` (Alternative Vite port)

To add more origins, modify `api_server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Integration with Dashboard

The dashboard automatically proxies API requests through Vite's dev server:

**Vite Configuration** (`dashboard/vite.config.js`):
```javascript
export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

This means the dashboard can make requests to `/api/datasets` and they will be forwarded to `http://localhost:8000/api/datasets`.

---

## Performance Considerations

### Caching

The API caches loaded datasets in memory to improve performance:

```python
dataset_cache: Dict[str, pd.DataFrame] = {}
```

Datasets are cached after first load and reused for subsequent requests.

### Pagination

For large datasets, use pagination to limit memory usage:

```
GET /api/data?path=data/large_file.csv&limit=1000&offset=0
```

### Query Optimization

DuckDB provides excellent performance for analytical queries:
- Columnar storage format
- Vectorized execution
- Parallel query processing

---

## Development

### Running Tests

```bash
# Test API endpoints
curl http://localhost:8000/api/datasets

# Test with specific dataset
curl "http://localhost:8000/api/data?path=data/soccer/laliga_24_25.csv&limit=10"

# Test SQL query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM temp_data LIMIT 5"}'
```

### Hot Reload

The API server runs with auto-reload enabled during development:

```python
uvicorn.run(
    "api_server:app",
    host=host,
    port=port,
    reload=True,  # Auto-reload on code changes
    log_level="info"
)
```

---

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:

```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or use a different port
export API_PORT=8001
python api_server.py
```

### Import Errors

Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Dataset Not Found

Verify the dataset path is relative to the project root:

```
✓ data/soccer/laliga_24_25.csv
✗ /absolute/path/to/file.csv
✗ ~/relative/to/home/file.csv
```

### CORS Errors

If you see CORS errors in the browser console:
1. Ensure the API server is running
2. Check that the dashboard is accessing through the proxy
3. Verify CORS origins in `api_server.py`

---

## API Client Examples

### Python

```python
import requests

# List datasets
response = requests.get("http://localhost:8000/api/datasets")
datasets = response.json()["datasets"]

# Load dataset
response = requests.get(
    "http://localhost:8000/api/data",
    params={"path": "data/soccer/laliga_24_25.csv", "limit": 100}
)
data = response.json()

# Execute query
response = requests.post(
    "http://localhost:8000/api/query",
    json={"query": "SELECT * FROM temp_data WHERE points > 70"}
)
results = response.json()
```

### JavaScript/TypeScript

```javascript
// List datasets
const response = await fetch('/api/datasets');
const { datasets } = await response.json();

// Load dataset
const dataResponse = await fetch(
  `/api/data?path=${encodeURIComponent('data/soccer/laliga_24_25.csv')}&limit=100`
);
const data = await dataResponse.json();

// Execute query
const queryResponse = await fetch('/api/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'SELECT * FROM temp_data WHERE points > 70'
  })
});
const results = await queryResponse.json();
```

### cURL

```bash
# List datasets
curl http://localhost:8000/api/datasets

# Load dataset
curl "http://localhost:8000/api/data?path=data/soccer/laliga_24_25.csv&limit=10"

# Execute query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM temp_data LIMIT 5"}'

# Get profile
curl "http://localhost:8000/api/profile?path=data/soccer/laliga_24_25.csv"
```

---

## Security Considerations

### Production Deployment

For production deployment:

1. **Disable auto-reload:**
   ```python
   uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=False)
   ```

2. **Use environment variables for sensitive data**

3. **Implement authentication:**
   ```python
   from fastapi.security import HTTPBearer
   security = HTTPBearer()
   ```

4. **Add rate limiting:**
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

5. **Use HTTPS in production**

6. **Restrict CORS origins to your domain**

---

## License

This API is part of the FastReports project. See the main README for license information.

---

## Support

For issues, questions, or contributions:
- Check the main project documentation
- Review the interactive API docs at `/docs`
- Examine the source code in `api_server.py`

---

**Made with Bob** 🤖