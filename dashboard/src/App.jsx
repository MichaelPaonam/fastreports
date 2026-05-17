import { h, createRef } from 'preact';
import { useState, useEffect, useRef } from 'preact/hooks';
import DataTable from './components/DataTable';
import ChartViewer from './components/ChartViewer';
import FilterPanel from './components/FilterPanel';
import './App.css';

export default function App() {
  const API_BASE = import.meta.env.VITE_API_URL || '';
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [data, setData] = useState([]);
  const [originalData, setOriginalData] = useState([]);
  const [originalColumns, setOriginalColumns] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [columns, setColumns] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('table');
  const [stats, setStats] = useState(null);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  useEffect(() => {
    loadDatasets();
  }, []);

  const loadDatasets = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/datasets`);
      if (!response.ok) throw new Error('Failed to load datasets');
      const data = await response.json();
      setDatasets(data.datasets || []);
    } catch (err) {
      console.error('Error loading datasets:', err);
      // For demo purposes, use mock data
      setDatasets([
        { name: 'Soccer Data', path: 'data/soccer/laliga_24_25.csv' },
        { name: 'Layoffs', path: 'data/layoffs/layoffs.csv' },
        { name: 'Pizza Delivery', path: 'data/pizza_delivery_app/purchase_log.xlsx' }
      ]);
    }
  };

  const loadDataset = async (datasetPath) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE}/api/data?path=${encodeURIComponent(datasetPath)}`);
      if (!response.ok) throw new Error('Failed to load dataset');
      
      const result = await response.json();
      setData(result.data || []);
      setOriginalData(result.data || []);
      setFilteredData(result.data || []);
      setColumns(result.columns || []);
      setOriginalColumns(result.columns || []);
      setStats(result.stats || null);
      setSelectedDataset(datasetPath);
    } catch (err) {
      console.error('Error loading dataset:', err);
      setError(err.message);
      // For demo, generate mock data
      generateMockData();
    } finally {
      setLoading(false);
    }
  };

  const generateMockData = () => {
    const mockData = Array.from({ length: 100 }, (_, i) => ({
      id: i + 1,
      name: `Item ${i + 1}`,
      category: ['A', 'B', 'C'][i % 3],
      value: Math.floor(Math.random() * 1000),
      date: new Date(2024, 0, i % 30 + 1).toISOString().split('T')[0],
      status: ['Active', 'Inactive'][i % 2]
    }));

    setData(mockData);
    setOriginalData(mockData);
    setFilteredData(mockData);
    setColumns(['id', 'name', 'category', 'value', 'date', 'status']);
    setOriginalColumns(['id', 'name', 'category', 'value', 'date', 'status']);
    setSelectedDataset('mock-data');
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_BASE}/api/upload`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || 'Upload failed');
      }

      const result = await response.json();

      setDatasets(prev => {
        const exists = prev.some(d => d.path === result.path);
        if (exists) return prev;
        return [...prev, { name: result.name, path: result.path, size: result.size }];
      });

      await loadDataset(result.path);
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.message);
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleFilterChange = (filters) => {
    if (Object.keys(filters).length === 0) {
      setData(originalData);
      setFilteredData(originalData);
      setColumns(originalColumns);
      return;
    }

    const filtered = data.filter(row => {
      return Object.entries(filters).every(([column, value]) => {
        if (!value) return true;

        const rowValue = row[column];

        // Handle number range filters
        if (typeof value === 'object' && (value.min || value.max)) {
          const numValue = Number(rowValue);
          if (value.min && numValue < Number(value.min)) return false;
          if (value.max && numValue > Number(value.max)) return false;
          return true;
        }

        // Handle text filters
        return String(rowValue).toLowerCase().includes(String(value).toLowerCase());
      });
    });

    setFilteredData(filtered);
  };

  const handleQueryExecute = async (query) => {
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/api/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, data: filteredData })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Query execution failed');
      }

      const result = await response.json();
      
      // Update both data and columns from query results
      if (result.data && result.data.length > 0) {
        // Update both data and filteredData so pagination and stats reflect query results
        setData(result.data);
        setFilteredData(result.data);
        // Update columns if they changed (e.g., SELECT specific columns)
        if (result.columns) {
          setColumns(result.columns);
        }
      } else {
        setData([]);
        setFilteredData([]);
        setError('Query returned no results');
      }
    } catch (err) {
      console.error('Error executing query:', err);
      setError(err.message || 'Query execution failed. Please check your SQL syntax.');
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="container">
          <h1>FastReports Dashboard</h1>
          <p>Interactive data analysis and visualization</p>
        </div>
      </header>

      <div className="container">
        <div className="dataset-selector">
          <label>Select Dataset:</label>
          <select 
            value={selectedDataset || ''} 
            onChange={(e) => loadDataset(e.target.value)}
            disabled={loading}
          >
            <option value="">Choose a dataset...</option>
            {datasets.map(ds => (
              <option key={ds.path} value={ds.path}>{ds.name}</option>
            ))}
          </select>
          <button
            type="button"
            className="btn btn-outline"
            onClick={generateMockData}
            disabled={loading}
          >
            Load Demo Data
          </button>
          <button
            type="button"
            className="btn btn-primary"
            onClick={() => fileInputRef.current?.click()}
            disabled={loading || uploading}
          >
            {uploading ? 'Uploading...' : 'Upload File'}
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv,.xlsx,.xls,.json,.parquet"
            onChange={handleFileUpload}
            style={{ display: 'none' }}
          />
        </div>

        {error && (
          <div className="error">
            <strong>Error:</strong> {error}
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Loading data...</p>
          </div>
        )}

        {!loading && data.length > 0 && (
          <>
            <div className="stats-bar">
              <div className="stat-item">
                <span className="stat-label">Total Rows</span>
                <span className="stat-value">{data.length.toLocaleString()}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Filtered Rows</span>
                <span className="stat-value">{filteredData.length.toLocaleString()}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Columns</span>
                <span className="stat-value">{columns.length}</span>
              </div>
              {stats && (
                <div className="stat-item">
                  <span className="stat-label">Quality Score</span>
                  <span className="stat-value">{stats.quality_score || 'N/A'}</span>
                </div>
              )}
            </div>

            <FilterPanel
              data={data}
              columns={columns}
              onFilterChange={handleFilterChange}
              onQueryExecute={handleQueryExecute}
            />

            <div className="tabs">
              <button
                type="button"
                className={`tab ${activeTab === 'table' ? 'active' : ''}`}
                onClick={() => setActiveTab('table')}
              >
                📊 Data Table
              </button>
              <button
                type="button"
                className={`tab ${activeTab === 'charts' ? 'active' : ''}`}
                onClick={() => setActiveTab('charts')}
              >
                📈 Visualizations
              </button>
            </div>

            <div className="tab-content">
              {activeTab === 'table' && (
                <DataTable data={filteredData} columns={columns} />
              )}
              {activeTab === 'charts' && (
                <ChartViewer data={filteredData} columns={columns} />
              )}
            </div>
          </>
        )}

        {!loading && data.length === 0 && !error && (
          <div className="empty-state">
            <h2>Welcome to FastReports Dashboard</h2>
            <p>Select a dataset from the dropdown above or load demo data to get started.</p>
          </div>
        )}
      </div>
    </div>
  );
}

// Made with Bob
