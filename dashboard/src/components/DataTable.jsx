import { h } from 'preact';
import { useState, useMemo } from 'preact/hooks';
import './DataTable.css';

export default function DataTable({ data, columns, pageSize = 50 }) {
  const [currentPage, setCurrentPage] = useState(1);
  const [sortColumn, setSortColumn] = useState(null);
  const [sortDirection, setSortDirection] = useState('asc');

  const sortedData = useMemo(() => {
    if (!sortColumn) return data;

    return [...data].sort((a, b) => {
      const aVal = a[sortColumn];
      const bVal = b[sortColumn];

      if (aVal === null || aVal === undefined) return 1;
      if (bVal === null || bVal === undefined) return -1;

      if (typeof aVal === 'number' && typeof bVal === 'number') {
        return sortDirection === 'asc' ? aVal - bVal : bVal - aVal;
      }

      const aStr = String(aVal).toLowerCase();
      const bStr = String(bVal).toLowerCase();

      if (sortDirection === 'asc') {
        return aStr.localeCompare(bStr);
      } else {
        return bStr.localeCompare(aStr);
      }
    });
  }, [data, sortColumn, sortDirection]);

  const totalPages = Math.ceil(sortedData.length / pageSize);
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  const currentData = sortedData.slice(startIndex, endIndex);

  const handleSort = (column) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(column);
      setSortDirection('asc');
    }
  };

  const formatValue = (value) => {
    if (value === null || value === undefined) return '-';
    if (typeof value === 'number') {
      return value.toLocaleString(undefined, { maximumFractionDigits: 2 });
    }
    if (typeof value === 'boolean') return value ? 'Yes' : 'No';
    return String(value);
  };

  const goToPage = (page) => {
    setCurrentPage(Math.max(1, Math.min(page, totalPages)));
  };

  if (!data || data.length === 0) {
    return (
      <div className="data-table-empty">
        <p>No data to display</p>
      </div>
    );
  }

  return (
    <div className="data-table-container">
      <div className="data-table-info">
        <span>
          Showing {startIndex + 1}-{Math.min(endIndex, sortedData.length)} of {sortedData.length} rows
        </span>
        <div className="data-table-actions">
          <button 
            className="btn btn-outline btn-sm"
            onClick={() => {
              const csv = [
                columns.join(','),
                ...sortedData.map(row => columns.map(col => `"${row[col]}"`).join(','))
              ].join('\n');
              const blob = new Blob([csv], { type: 'text/csv' });
              const url = URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = 'data.csv';
              a.click();
            }}
          >
            Export CSV
          </button>
        </div>
      </div>

      <div className="data-table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              {columns.map(column => (
                <th key={column} onClick={() => handleSort(column)}>
                  <div className="th-content">
                    <span>{column}</span>
                    {sortColumn === column && (
                      <span className="sort-indicator">
                        {sortDirection === 'asc' ? '↑' : '↓'}
                      </span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {currentData.map((row, idx) => (
              <tr key={idx}>
                {columns.map(column => (
                  <td key={column}>{formatValue(row[column])}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="data-table-pagination">
          <button
            className="btn btn-outline btn-sm"
            onClick={() => goToPage(1)}
            disabled={currentPage === 1}
          >
            First
          </button>
          <button
            className="btn btn-outline btn-sm"
            onClick={() => goToPage(currentPage - 1)}
            disabled={currentPage === 1}
          >
            Previous
          </button>
          
          <div className="pagination-info">
            Page {currentPage} of {totalPages}
          </div>

          <button
            className="btn btn-outline btn-sm"
            onClick={() => goToPage(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
          <button
            className="btn btn-outline btn-sm"
            onClick={() => goToPage(totalPages)}
            disabled={currentPage === totalPages}
          >
            Last
          </button>
        </div>
      )}
    </div>
  );
}

// Made with Bob
