import { h } from 'preact';
import { useState, useEffect } from 'preact/hooks';
import './FilterPanel.css';

export default function FilterPanel({ data, columns, onFilterChange, onQueryExecute, hasModifiedData }) {
  const [filters, setFilters] = useState({});
  const [sqlQuery, setSqlQuery] = useState('');
  const [showQueryBuilder, setShowQueryBuilder] = useState(false);

  useEffect(() => {
    onFilterChange(filters);
  }, [filters]);

  const handleFilterChange = (column, value) => {
    setFilters(prev => {
      if (!value) {
        const newFilters = { ...prev };
        delete newFilters[column];
        return newFilters;
      }
      return { ...prev, [column]: value };
    });
  };

  const clearFilters = () => {
    setFilters({});
  };

  const getUniqueValues = (column) => {
    if (!data || !data.length) return [];
    const values = [...new Set(data.map(row => row[column]))];
    return values.filter(v => v !== null && v !== undefined).slice(0, 100);
  };

  const getColumnType = (column) => {
    if (!data || !data.length) return 'text';
    const value = data[0][column];
    if (typeof value === 'number') return 'number';
    if (value instanceof Date || !isNaN(Date.parse(value))) return 'date';
    return 'text';
  };

  const executeQuery = (e) => {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    if (sqlQuery.trim()) {
      onQueryExecute(sqlQuery);
    }
  };

  const activeFilterCount = Object.keys(filters).length;

  return (
    <div className="filter-panel">
      <div className="filter-header">
        <h3>Filters & Query</h3>
        <div className="filter-actions">
          {activeFilterCount > 0 && (
            <span className="filter-badge">{activeFilterCount} active</span>
          )}
          <button
            type="button"
            className="btn btn-outline btn-sm"
            onClick={clearFilters}
            disabled={activeFilterCount === 0 && !hasModifiedData}
          >
            Clear All
          </button>
          <button
            type="button"
            className="btn btn-primary btn-sm"
            onClick={() => setShowQueryBuilder(!showQueryBuilder)}
          >
            {showQueryBuilder ? 'Hide' : 'Show'} SQL Query
          </button>
        </div>
      </div>

      {showQueryBuilder && (
        <div className="query-builder">
          <label>SQL Query (DuckDB syntax)</label>
          <textarea
            value={sqlQuery}
            onChange={(e) => setSqlQuery(e.target.value)}
            onKeyDown={(e) => {
              // Execute query on Ctrl+Enter or Cmd+Enter
              if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                executeQuery(e);
              }
            }}
            placeholder="SELECT * FROM data WHERE column = 'value'"
            rows="4"
          />
          <button type="button" className="btn btn-primary" onClick={executeQuery}>
            Execute Query
          </button>
          <div className="query-help">
            <small>
              <strong>Table name:</strong> Use <code>data</code> to reference the current dataset<br/>
              <strong>Example:</strong> <code>SELECT * FROM data WHERE age {'>'} 25 ORDER BY name LIMIT 100</code><br/>
              <strong>Tip:</strong> Press Ctrl+Enter (Cmd+Enter on Mac) to execute query
            </small>
          </div>
        </div>
      )}

      <div className="filter-grid">
        {columns.map(column => {
          const type = getColumnType(column);
          const uniqueValues = type === 'text' ? getUniqueValues(column) : [];

          return (
            <div key={column} className="filter-item">
              <label>{column}</label>
              
              {type === 'text' && uniqueValues.length > 0 && uniqueValues.length <= 50 ? (
                <select
                  value={filters[column] || ''}
                  onChange={(e) => handleFilterChange(column, e.target.value)}
                >
                  <option value="">All</option>
                  {uniqueValues.map(value => (
                    <option key={value} value={value}>{value}</option>
                  ))}
                </select>
              ) : type === 'number' ? (
                <div className="number-filter">
                  <input
                    type="number"
                    placeholder="Min"
                    value={filters[column]?.min || ''}
                    onChange={(e) => {
                      const next = { ...filters[column], min: e.target.value };
                      handleFilterChange(column, (!next.min && !next.max) ? '' : next);
                    }}
                  />
                  <input
                    type="number"
                    placeholder="Max"
                    value={filters[column]?.max || ''}
                    onChange={(e) => {
                      const next = { ...filters[column], max: e.target.value };
                      handleFilterChange(column, (!next.min && !next.max) ? '' : next);
                    }}
                  />
                </div>
              ) : (
                <input
                  type="text"
                  placeholder={`Filter ${column}...`}
                  value={filters[column] || ''}
                  onChange={(e) => handleFilterChange(column, e.target.value)}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

// Made with Bob
