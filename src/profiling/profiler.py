"""
Data Profiler Module
Analyzes data characteristics and generates comprehensive profiles.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger("profiling.profiler")


class DataProfiler:
    """Profiles data and generates comprehensive analysis."""
    
    def __init__(self):
        self.logger = logger
    
    def profile_dataframe(self, df: pd.DataFrame, dataset_name: str = "dataset") -> Dict[str, Any]:
        """
        Generate comprehensive profile of DataFrame.
        
        Args:
            df: DataFrame to profile
            dataset_name: Name of the dataset
            
        Returns:
            Dictionary with profiling results
        """
        self.logger.info(f"Profiling dataset: {dataset_name}")
        
        profile = {
            'dataset_name': dataset_name,
            'timestamp': datetime.now().isoformat(),
            'overview': self._profile_overview(df),
            'columns': self._profile_columns(df),
            'missing_values': self._profile_missing_values(df),
            'duplicates': self._profile_duplicates(df),
            'memory': self._profile_memory(df),
            'correlations': self._profile_correlations(df)
        }
        
        self.logger.info(f"Profiling complete for {dataset_name}")
        return profile
    
    def _profile_overview(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate overview statistics."""
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'total_cells': df.size,
            'column_names': list(df.columns),
            'dtypes_summary': df.dtypes.value_counts().to_dict()
        }
    
    def _profile_columns(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Profile each column individually."""
        column_profiles = {}
        
        for col in df.columns:
            column_profiles[col] = self._profile_single_column(df[col])
        
        return column_profiles
    
    def _profile_single_column(self, series: pd.Series) -> Dict[str, Any]:
        """Profile a single column."""
        profile = {
            'dtype': str(series.dtype),
            'non_null_count': int(series.count()),
            'null_count': int(series.isnull().sum()),
            'null_percentage': round(series.isnull().sum() / len(series) * 100, 2),
            'unique_count': int(series.nunique()),
            'unique_percentage': round(series.nunique() / len(series) * 100, 2)
        }
        
        # Add statistics based on data type
        if pd.api.types.is_numeric_dtype(series):
            profile.update(self._profile_numeric_column(series))
        elif pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series):
            profile.update(self._profile_text_column(series))
        elif pd.api.types.is_datetime64_any_dtype(series):
            profile.update(self._profile_datetime_column(series))
        elif pd.api.types.is_bool_dtype(series):
            profile.update(self._profile_boolean_column(series))
        
        return profile
    
    def _profile_numeric_column(self, series: pd.Series) -> Dict[str, Any]:
        """Profile numeric column."""
        # Remove NaN values for statistics
        clean_series = series.dropna()
        
        if len(clean_series) == 0:
            return {'type': 'numeric', 'all_null': True}
        
        profile = {
            'type': 'numeric',
            'min': float(clean_series.min()),
            'max': float(clean_series.max()),
            'mean': float(clean_series.mean()),
            'median': float(clean_series.median()),
            'std': float(clean_series.std()) if len(clean_series) > 1 else 0.0,
            'q25': float(clean_series.quantile(0.25)),
            'q75': float(clean_series.quantile(0.75)),
            'skewness': float(clean_series.skew()),
            'kurtosis': float(clean_series.kurtosis())
        }
        
        # Detect potential outliers using IQR method
        q1 = profile['q25']
        q3 = profile['q75']
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = clean_series[(clean_series < lower_bound) | (clean_series > upper_bound)]
        profile['outlier_count'] = len(outliers)
        profile['outlier_percentage'] = round(len(outliers) / len(clean_series) * 100, 2)
        
        # Check if all values are integers
        profile['is_integer'] = bool(clean_series.apply(lambda x: float(x).is_integer()).all())
        
        # Check for negative values
        profile['has_negative'] = bool((clean_series < 0).any())
        profile['negative_count'] = int((clean_series < 0).sum())
        
        # Check for zeros
        profile['zero_count'] = int((clean_series == 0).sum())
        
        return profile
    
    def _profile_text_column(self, series: pd.Series) -> Dict[str, Any]:
        """Profile text/object column."""
        clean_series = series.dropna()
        
        if len(clean_series) == 0:
            return {'type': 'text', 'all_null': True}
        
        # Convert to string
        str_series = clean_series.astype(str)
        
        profile = {
            'type': 'text',
            'min_length': int(str_series.str.len().min()),
            'max_length': int(str_series.str.len().max()),
            'mean_length': round(str_series.str.len().mean(), 2),
            'empty_string_count': int((str_series == '').sum()),
            'whitespace_only_count': int(str_series.str.strip().eq('').sum())
        }
        
        # Get most common values
        value_counts = series.value_counts()
        profile['top_values'] = value_counts.head(10).to_dict()
        
        # Check if categorical (low cardinality)
        unique_ratio = series.nunique() / len(series)
        profile['is_categorical'] = unique_ratio < 0.5
        
        # Check for potential issues
        profile['has_mixed_case'] = bool(
            str_series.str.islower().any() and str_series.str.isupper().any()
        )
        
        return profile
    
    def _profile_datetime_column(self, series: pd.Series) -> Dict[str, Any]:
        """Profile datetime column."""
        clean_series = series.dropna()
        
        if len(clean_series) == 0:
            return {'type': 'datetime', 'all_null': True}
        
        profile = {
            'type': 'datetime',
            'min_date': str(clean_series.min()),
            'max_date': str(clean_series.max()),
            'date_range_days': (clean_series.max() - clean_series.min()).days
        }
        
        return profile
    
    def _profile_boolean_column(self, series: pd.Series) -> Dict[str, Any]:
        """Profile boolean column."""
        clean_series = series.dropna()
        
        if len(clean_series) == 0:
            return {'type': 'boolean', 'all_null': True}
        
        value_counts = clean_series.value_counts()
        
        profile = {
            'type': 'boolean',
            'true_count': int(value_counts.get(True, 0)),
            'false_count': int(value_counts.get(False, 0)),
            'true_percentage': round(value_counts.get(True, 0) / len(clean_series) * 100, 2)
        }
        
        return profile
    
    def _profile_missing_values(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze missing values."""
        missing_counts = df.isnull().sum()
        missing_percentages = (missing_counts / len(df) * 100).round(2)
        
        # Columns with missing values
        columns_with_missing = missing_counts[missing_counts > 0].to_dict()
        
        # Rows with any missing values
        rows_with_missing = df.isnull().any(axis=1).sum()
        
        # Completely empty rows
        completely_empty_rows = (df.isnull().all(axis=1)).sum()
        
        return {
            'total_missing_cells': int(missing_counts.sum()),
            'missing_percentage': round(missing_counts.sum() / df.size * 100, 2),
            'columns_with_missing': columns_with_missing,
            'columns_with_missing_count': len(columns_with_missing),
            'rows_with_missing': int(rows_with_missing),
            'rows_with_missing_percentage': round(rows_with_missing / len(df) * 100, 2),
            'completely_empty_rows': int(completely_empty_rows)
        }
    
    def _profile_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze duplicate rows."""
        duplicate_rows = df.duplicated()
        duplicate_count = duplicate_rows.sum()
        
        return {
            'duplicate_rows': int(duplicate_count),
            'duplicate_percentage': round(duplicate_count / len(df) * 100, 2),
            'unique_rows': len(df) - duplicate_count
        }
    
    def _profile_memory(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze memory usage."""
        memory_usage = df.memory_usage(deep=True)
        
        return {
            'total_mb': round(memory_usage.sum() / (1024 * 1024), 2),
            'by_column_mb': {
                col: round(mem / (1024 * 1024), 2)
                for col, mem in memory_usage.items()
            }
        }
    
    def _profile_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze correlations between numeric columns."""
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty or len(numeric_df.columns) < 2:
            return {
                'has_correlations': False,
                'reason': 'Not enough numeric columns'
            }
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        # Find strong correlations (excluding diagonal)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:  # Strong correlation threshold
                    strong_correlations.append({
                        'column1': corr_matrix.columns[i],
                        'column2': corr_matrix.columns[j],
                        'correlation': round(float(corr_value), 3)
                    })
        
        return {
            'has_correlations': True,
            'numeric_columns': list(numeric_df.columns),
            'correlation_matrix': corr_matrix.to_dict(),
            'strong_correlations': strong_correlations,
            'strong_correlation_count': len(strong_correlations)
        }
    
    def generate_summary_report(self, profile: Dict[str, Any]) -> str:
        """Generate human-readable summary report."""
        overview = profile['overview']
        missing = profile['missing_values']
        duplicates = profile['duplicates']
        
        report = f"""
DATA PROFILE SUMMARY: {profile['dataset_name']}
{'=' * 80}

OVERVIEW:
  - Rows: {overview['rows']:,}
  - Columns: {overview['columns']}
  - Total Cells: {overview['total_cells']:,}

DATA QUALITY:
  - Missing Values: {missing['total_missing_cells']:,} ({missing['missing_percentage']}%)
  - Columns with Missing: {missing['columns_with_missing_count']}
  - Duplicate Rows: {duplicates['duplicate_rows']:,} ({duplicates['duplicate_percentage']}%)

MEMORY USAGE:
  - Total: {profile['memory']['total_mb']} MB

CORRELATIONS:
  - Strong Correlations Found: {profile['correlations'].get('strong_correlation_count', 0)}

{'=' * 80}
"""
        return report


# Example usage
if __name__ == "__main__":
    # Create sample data
    df = pd.DataFrame({
        'id': range(1, 101),
        'name': ['User' + str(i) for i in range(1, 101)],
        'age': np.random.randint(18, 80, 100),
        'score': np.random.normal(75, 15, 100),
        'active': np.random.choice([True, False], 100)
    })
    
    # Add some missing values
    df.loc[5:10, 'age'] = np.nan
    df.loc[15:20, 'score'] = np.nan
    
    # Profile the data
    profiler = DataProfiler()
    profile = profiler.profile_dataframe(df, "sample_data")
    
    # Print summary
    print(profiler.generate_summary_report(profile))

# Made with Bob
