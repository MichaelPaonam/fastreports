# FastReports Dashboard

Interactive web-based dashboard for data analysis and visualization built with Preact and Vite.

## Features

- 📊 **Interactive Data Table** - Sortable, paginated data display with CSV export
- 📈 **Multiple Chart Types** - Bar, line, scatter, pie, histogram, and box plots
- 🔍 **Advanced Filtering** - Column-based filters with SQL query support
- ⚡ **Real-time Updates** - Instant visualization updates as you filter
- 🎨 **Responsive Design** - Works on desktop, tablet, and mobile
- 🚀 **Fast Performance** - Lightweight Preact framework with Vite bundling

## Prerequisites

- Node.js 16+ and npm
- Python backend running (for API endpoints)

## Installation

```bash
cd dashboard
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

The dashboard will be available at `http://localhost:3000`

## Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Preview Production Build

```bash
npm run preview
```

## Project Structure

```
dashboard/
├── public/              # Static assets
├── src/
│   ├── components/      # React components
│   │   ├── DataTable.jsx       # Data table component
│   │   ├── ChartViewer.jsx     # Chart visualization component
│   │   └── FilterPanel.jsx     # Filtering controls
│   ├── App.jsx          # Main application
│   ├── main.jsx         # Entry point
│   └── style.css        # Global styles
├── index.html           # HTML template
├── package.json         # Dependencies
└── vite.config.js       # Vite configuration
```

## Components

### DataTable
Displays data in a sortable, paginated table format.

**Features:**
- Click column headers to sort
- Pagination controls
- CSV export
- Responsive layout

### ChartViewer
Interactive chart visualization with multiple chart types.

**Supported Charts:**
- Bar Chart
- Line Chart
- Scatter Plot
- Pie Chart
- Histogram
- Box Plot

**Features:**
- Dynamic axis selection
- Group by support
- Real-time updates
- Plotly-powered interactivity

### FilterPanel
Advanced filtering controls with SQL query support.

**Features:**
- Column-based filters
- Text search
- Number range filters
- Dropdown selection for categorical data
- SQL query builder (DuckDB syntax)
- Active filter count
- Clear all filters

## API Integration

The dashboard expects the following API endpoints:

### GET `/api/datasets`
Returns list of available datasets.

**Response:**
```json
{
  "datasets": [
    {
      "name": "Dataset Name",
      "path": "path/to/dataset.csv"
    }
  ]
}
```

### GET `/api/data?path=<dataset_path>`
Returns dataset data and metadata.

**Response:**
```json
{
  "data": [...],
  "columns": ["col1", "col2"],
  "stats": {
    "quality_score": 0.95
  }
}
```

### POST `/api/query`
Executes SQL query on data.

**Request:**
```json
{
  "query": "SELECT * FROM data WHERE column > 10",
  "data": [...]
}
```

**Response:**
```json
{
  "data": [...]
}
```

## SQL Query Support

The dashboard supports DuckDB SQL syntax for advanced queries:

```sql
-- Filter data
SELECT * FROM data WHERE age > 25

-- Aggregate
SELECT category, COUNT(*) as count 
FROM data 
GROUP BY category

-- Order results
SELECT * FROM data 
ORDER BY value DESC 
LIMIT 10
```

## Customization

### Styling
Edit `src/style.css` and component-specific CSS files to customize the look and feel.

CSS variables are defined in `src/style.css`:
```css
:root {
  --primary: #2563eb;
  --secondary: #64748b;
  --success: #10b981;
  /* ... */
}
```

### Adding New Chart Types
Extend `ChartViewer.jsx` to add new visualization types:

```javascript
const generateCustomChart = () => {
  // Your chart logic
  setChartData([...]);
  setLayout({...});
};
```

### Custom Filters
Add new filter types in `FilterPanel.jsx`:

```javascript
// Add custom filter logic
const handleCustomFilter = (column, value) => {
  // Your filter logic
};
```

## Performance Tips

1. **Pagination** - Large datasets are automatically paginated
2. **Lazy Loading** - Charts render only when tab is active
3. **Debouncing** - Filter updates are debounced for better performance
4. **Memoization** - Use React hooks for expensive computations

## Troubleshooting

### Dashboard won't start
- Ensure Node.js 16+ is installed: `node --version`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

### API connection errors
- Verify backend is running on port 8000
- Check proxy configuration in `vite.config.js`
- Ensure CORS is enabled on backend

### Charts not displaying
- Check browser console for errors
- Verify Plotly.js is loaded correctly
- Ensure data format matches expected structure

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Dependencies

### Core
- `preact` - Fast 3kB alternative to React
- `preact-router` - Routing for Preact
- `plotly.js` - Interactive charts
- `react-plotly.js` - Plotly wrapper for React/Preact

### Development
- `vite` - Fast build tool
- `@preact/preset-vite` - Preact plugin for Vite
- `eslint` - Code linting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check existing issues on GitHub
- Create a new issue with detailed description
- Include browser version and error messages

## Roadmap

- [ ] Real-time collaboration
- [ ] Custom dashboard layouts
- [ ] More chart types
- [ ] Advanced SQL editor with syntax highlighting
- [ ] Data export to multiple formats
- [ ] Saved queries and filters
- [ ] User preferences persistence
- [ ] Dark mode support