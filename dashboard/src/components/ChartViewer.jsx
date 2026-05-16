import { h } from 'preact';
import { useState, useEffect, useRef } from 'preact/hooks';
import Plot from 'react-plotly.js';
import './ChartViewer.css';

export default function ChartViewer({ data, columns }) {
  const [chartType, setChartType] = useState('bar');
  const [xAxis, setXAxis] = useState(columns[0] || '');
  const [yAxis, setYAxis] = useState(columns[1] || '');
  const [groupBy, setGroupBy] = useState('');
  const [chartData, setChartData] = useState([]);
  const [layout, setLayout] = useState({});

  useEffect(() => {
    if (!data || !data.length || !xAxis) return;

    generateChart();
  }, [data, chartType, xAxis, yAxis, groupBy]);

  const generateChart = () => {
    try {
      switch (chartType) {
        case 'bar':
          generateBarChart();
          break;
        case 'line':
          generateLineChart();
          break;
        case 'scatter':
          generateScatterChart();
          break;
        case 'pie':
          generatePieChart();
          break;
        case 'histogram':
          generateHistogram();
          break;
        case 'box':
          generateBoxPlot();
          break;
        default:
          generateBarChart();
      }
    } catch (error) {
      console.error('Error generating chart:', error);
    }
  };

  const generateBarChart = () => {
    if (!yAxis) {
      // Count frequency
      const counts = {};
      data.forEach(row => {
        const key = row[xAxis];
        counts[key] = (counts[key] || 0) + 1;
      });

      const trace = {
        x: Object.keys(counts),
        y: Object.values(counts),
        type: 'bar',
        marker: { color: '#2563eb' }
      };

      setChartData([trace]);
      setLayout({
        title: `Count by ${xAxis}`,
        xaxis: { title: xAxis },
        yaxis: { title: 'Count' },
        margin: { t: 50, r: 30, b: 80, l: 60 }
      });
    } else {
      // Aggregate by group
      if (groupBy) {
        const groups = {};
        data.forEach(row => {
          const group = row[groupBy];
          if (!groups[group]) groups[group] = { x: [], y: [] };
          groups[group].x.push(row[xAxis]);
          groups[group].y.push(row[yAxis]);
        });

        const traces = Object.entries(groups).map(([name, values]) => ({
          x: values.x,
          y: values.y,
          type: 'bar',
          name: name
        }));

        setChartData(traces);
      } else {
        const trace = {
          x: data.map(row => row[xAxis]),
          y: data.map(row => row[yAxis]),
          type: 'bar',
          marker: { color: '#2563eb' }
        };

        setChartData([trace]);
      }

      setLayout({
        title: `${yAxis} by ${xAxis}`,
        xaxis: { title: xAxis },
        yaxis: { title: yAxis },
        margin: { t: 50, r: 30, b: 80, l: 60 }
      });
    }
  };

  const generateLineChart = () => {
    if (!yAxis) return;

    if (groupBy) {
      const groups = {};
      data.forEach(row => {
        const group = row[groupBy];
        if (!groups[group]) groups[group] = { x: [], y: [] };
        groups[group].x.push(row[xAxis]);
        groups[group].y.push(row[yAxis]);
      });

      const traces = Object.entries(groups).map(([name, values]) => ({
        x: values.x,
        y: values.y,
        type: 'scatter',
        mode: 'lines+markers',
        name: name
      }));

      setChartData(traces);
    } else {
      const trace = {
        x: data.map(row => row[xAxis]),
        y: data.map(row => row[yAxis]),
        type: 'scatter',
        mode: 'lines+markers',
        marker: { color: '#2563eb' }
      };

      setChartData([trace]);
    }

    setLayout({
      title: `${yAxis} over ${xAxis}`,
      xaxis: { title: xAxis },
      yaxis: { title: yAxis },
      margin: { t: 50, r: 30, b: 80, l: 60 }
    });
  };

  const generateScatterChart = () => {
    if (!yAxis) return;

    const trace = {
      x: data.map(row => row[xAxis]),
      y: data.map(row => row[yAxis]),
      type: 'scatter',
      mode: 'markers',
      marker: { 
        color: '#2563eb',
        size: 8,
        opacity: 0.6
      }
    };

    setChartData([trace]);
    setLayout({
      title: `${yAxis} vs ${xAxis}`,
      xaxis: { title: xAxis },
      yaxis: { title: yAxis },
      margin: { t: 50, r: 30, b: 80, l: 60 }
    });
  };

  const generatePieChart = () => {
    const counts = {};
    data.forEach(row => {
      const key = row[xAxis];
      counts[key] = (counts[key] || 0) + 1;
    });

    const trace = {
      labels: Object.keys(counts),
      values: Object.values(counts),
      type: 'pie'
    };

    setChartData([trace]);
    setLayout({
      title: `Distribution of ${xAxis}`,
      margin: { t: 50, r: 30, b: 30, l: 30 }
    });
  };

  const generateHistogram = () => {
    const values = data.map(row => row[xAxis]).filter(v => typeof v === 'number');

    const trace = {
      x: values,
      type: 'histogram',
      marker: { color: '#2563eb' }
    };

    setChartData([trace]);
    setLayout({
      title: `Distribution of ${xAxis}`,
      xaxis: { title: xAxis },
      yaxis: { title: 'Frequency' },
      margin: { t: 50, r: 30, b: 80, l: 60 }
    });
  };

  const generateBoxPlot = () => {
    if (groupBy) {
      const groups = {};
      data.forEach(row => {
        const group = row[groupBy];
        if (!groups[group]) groups[group] = [];
        groups[group].push(row[xAxis]);
      });

      const traces = Object.entries(groups).map(([name, values]) => ({
        y: values,
        type: 'box',
        name: name
      }));

      setChartData(traces);
    } else {
      const trace = {
        y: data.map(row => row[xAxis]),
        type: 'box',
        marker: { color: '#2563eb' }
      };

      setChartData([trace]);
    }

    setLayout({
      title: `Distribution of ${xAxis}`,
      yaxis: { title: xAxis },
      margin: { t: 50, r: 30, b: 80, l: 60 }
    });
  };

  const numericColumns = columns.filter(col => {
    return data.some(row => typeof row[col] === 'number');
  });

  return (
    <div className="chart-viewer">
      <div className="chart-controls">
        <div className="control-group">
          <label>Chart Type</label>
          <select value={chartType} onChange={(e) => setChartType(e.target.value)}>
            <option value="bar">Bar Chart</option>
            <option value="line">Line Chart</option>
            <option value="scatter">Scatter Plot</option>
            <option value="pie">Pie Chart</option>
            <option value="histogram">Histogram</option>
            <option value="box">Box Plot</option>
          </select>
        </div>

        <div className="control-group">
          <label>X-Axis</label>
          <select value={xAxis} onChange={(e) => setXAxis(e.target.value)}>
            {columns.map(col => (
              <option key={col} value={col}>{col}</option>
            ))}
          </select>
        </div>

        {chartType !== 'pie' && chartType !== 'histogram' && chartType !== 'box' && (
          <div className="control-group">
            <label>Y-Axis</label>
            <select value={yAxis} onChange={(e) => setYAxis(e.target.value)}>
              <option value="">Count</option>
              {numericColumns.map(col => (
                <option key={col} value={col}>{col}</option>
              ))}
            </select>
          </div>
        )}

        {(chartType === 'bar' || chartType === 'line' || chartType === 'box') && (
          <div className="control-group">
            <label>Group By</label>
            <select value={groupBy} onChange={(e) => setGroupBy(e.target.value)}>
              <option value="">None</option>
              {columns.map(col => (
                <option key={col} value={col}>{col}</option>
              ))}
            </select>
          </div>
        )}
      </div>

      <div className="chart-container">
        {chartData.length > 0 ? (
          <Plot
            data={chartData}
            layout={{
              ...layout,
              autosize: true,
              paper_bgcolor: 'white',
              plot_bgcolor: '#f8fafc'
            }}
            config={{
              responsive: true,
              displayModeBar: true,
              displaylogo: false
            }}
            style={{ width: '100%', height: '500px' }}
          />
        ) : (
          <div className="chart-empty">
            <p>Select chart parameters to visualize data</p>
          </div>
        )}
      </div>
    </div>
  );
}

// Made with Bob
