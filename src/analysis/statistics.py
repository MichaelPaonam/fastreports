"""
Statistical Analysis Module
Performs comprehensive statistical analysis on datasets
"""

from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import numpy as np
from scipy import stats
from src.utils.logger import get_logger

logger = get_logger(__name__)


class StatisticalAnalyzer:
    """Performs statistical analysis on datasets."""
    
    def __init__(self):
        """Initialize the statistical analyzer."""
        self.analysis_results = {}
    
    def analyze_dataset(
        self,
        df: pd.DataFrame,
        dataset_name: str,
        target_column: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive statistical analysis.
        
        Args:
            df: DataFrame to analyze
            dataset_name: Name of the dataset
            target_column: Optional target column for focused analysis
        
        Returns:
            Dictionary containing all statistical analysis results
        """
        logger.info(f"Starting statistical analysis for {dataset_name}")
        
        results = {
            'dataset_name': dataset_name,
            'shape': df.shape,
            'descriptive_stats': self.descriptive_statistics(df),
            'correlation_analysis': self.correlation_analysis(df),
            'distribution_analysis': self.distribution_analysis(df),
            'outlier_analysis': self.outlier_analysis(df),
            'categorical_analysis': self.categorical_analysis(df),
            'missing_value_analysis': self.missing_value_analysis(df)
        }
        
        # Add time series analysis if date columns exist
        date_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
        if date_columns:
            results['time_series_analysis'] = self.time_series_analysis(df, date_columns[0])
        
        # Add target-focused analysis if specified
        if target_column and target_column in df.columns:
            results['target_analysis'] = self.target_variable_analysis(df, target_column)
        
        logger.info(f"Statistical analysis complete for {dataset_name}")
        
        return results
    
    def descriptive_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate descriptive statistics for all columns."""
        logger.info("Calculating descriptive statistics")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        stats_dict = {
            'numeric_columns': {},
            'categorical_columns': {}
        }
        
        # Numeric column statistics
        for col in numeric_cols:
            stats_dict['numeric_columns'][col] = {
                'count': int(df[col].count()),
                'mean': float(df[col].mean()) if not df[col].isna().all() else None,
                'median': float(df[col].median()) if not df[col].isna().all() else None,
                'std': float(df[col].std()) if not df[col].isna().all() else None,
                'min': float(df[col].min()) if not df[col].isna().all() else None,
                'max': float(df[col].max()) if not df[col].isna().all() else None,
                'q25': float(df[col].quantile(0.25)) if not df[col].isna().all() else None,
                'q75': float(df[col].quantile(0.75)) if not df[col].isna().all() else None,
                'skewness': float(df[col].skew()) if not df[col].isna().all() else None,
                'kurtosis': float(df[col].kurtosis()) if not df[col].isna().all() else None
            }
        
        # Categorical column statistics
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        for col in categorical_cols:
            stats_dict['categorical_columns'][col] = {
                'count': int(df[col].count()),
                'unique': int(df[col].nunique()),
                'top': str(df[col].mode()[0]) if len(df[col].mode()) > 0 else None,
                'freq': int(df[col].value_counts().iloc[0]) if len(df[col]) > 0 else 0
            }
        
        return stats_dict
    
    def correlation_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze correlations between numeric variables."""
        logger.info("Performing correlation analysis")
        
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            return {
                'correlation_matrix': {},
                'strong_correlations': [],
                'message': 'Insufficient numeric columns for correlation analysis'
            }
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        # Find strong correlations (|r| > 0.7)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_correlations.append({
                        'variable1': corr_matrix.columns[i],
                        'variable2': corr_matrix.columns[j],
                        'correlation': float(corr_value),
                        'strength': 'strong positive' if corr_value > 0 else 'strong negative'
                    })
        
        return {
            'correlation_matrix': corr_matrix.to_dict(),
            'strong_correlations': strong_correlations,
            'num_strong_correlations': len(strong_correlations)
        }
    
    def distribution_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze distributions of numeric variables."""
        logger.info("Analyzing distributions")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        distributions = {}
        for col in numeric_cols:
            if df[col].notna().sum() < 3:
                continue
            
            # Normality test (Shapiro-Wilk for small samples, Anderson-Darling for larger)
            sample_size = df[col].notna().sum()
            if sample_size <= 5000:
                try:
                    stat, p_value = stats.shapiro(df[col].dropna())
                    test_name = 'Shapiro-Wilk'
                except:
                    stat, p_value = 0, 1
                    test_name = 'None'
            else:
                # Use Anderson-Darling for larger samples
                try:
                    result = stats.anderson(df[col].dropna())
                    stat = result.statistic
                    p_value = 0.05 if stat > result.critical_values[2] else 0.1
                    test_name = 'Anderson-Darling'
                except:
                    stat, p_value = 0, 1
                    test_name = 'None'
            
            distributions[col] = {
                'normality_test': test_name,
                'test_statistic': float(stat),
                'p_value': float(p_value),
                'is_normal': p_value > 0.05,
                'skewness': float(df[col].skew()),
                'kurtosis': float(df[col].kurtosis()),
                'distribution_type': self._classify_distribution(df[col])
            }
        
        return distributions
    
    def _classify_distribution(self, series: pd.Series) -> str:
        """Classify the distribution type based on skewness and kurtosis."""
        skew = series.skew()
        kurt = series.kurtosis()
        
        if abs(skew) < 0.5 and abs(kurt) < 0.5:
            return 'approximately_normal'
        elif skew > 1:
            return 'right_skewed'
        elif skew < -1:
            return 'left_skewed'
        elif kurt > 3:
            return 'heavy_tailed'
        elif kurt < -1:
            return 'light_tailed'
        else:
            return 'moderately_skewed'
    
    def outlier_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect outliers using IQR method."""
        logger.info("Detecting outliers")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        outliers = {}
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            outlier_count = outlier_mask.sum()
            
            if outlier_count > 0:
                outliers[col] = {
                    'count': int(outlier_count),
                    'percentage': float(outlier_count / len(df) * 100),
                    'lower_bound': float(lower_bound),
                    'upper_bound': float(upper_bound),
                    'min_outlier': float(df[col][outlier_mask].min()),
                    'max_outlier': float(df[col][outlier_mask].max())
                }
        
        return {
            'columns_with_outliers': list(outliers.keys()),
            'outlier_details': outliers,
            'total_columns_analyzed': len(numeric_cols)
        }
    
    def categorical_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze categorical variables."""
        logger.info("Analyzing categorical variables")
        
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        analysis = {}
        for col in categorical_cols:
            value_counts = df[col].value_counts()
            
            analysis[col] = {
                'unique_values': int(df[col].nunique()),
                'most_common': str(value_counts.index[0]) if len(value_counts) > 0 else None,
                'most_common_count': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                'most_common_percentage': float(value_counts.iloc[0] / len(df) * 100) if len(value_counts) > 0 else 0,
                'top_5_values': value_counts.head(5).to_dict(),
                'cardinality': 'high' if df[col].nunique() > len(df) * 0.5 else 'low'
            }
        
        return analysis
    
    def missing_value_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze missing value patterns."""
        logger.info("Analyzing missing values")
        
        missing_counts = df.isnull().sum()
        missing_percentages = (missing_counts / len(df) * 100)
        
        columns_with_missing = missing_counts[missing_counts > 0].to_dict()
        
        return {
            'total_missing': int(missing_counts.sum()),
            'columns_with_missing': {
                col: {
                    'count': int(count),
                    'percentage': float(missing_percentages[col])
                }
                for col, count in columns_with_missing.items()
            },
            'missing_percentage_overall': float(missing_counts.sum() / (len(df) * len(df.columns)) * 100)
        }
    
    def time_series_analysis(self, df: pd.DataFrame, date_column: str) -> Dict[str, Any]:
        """Analyze time series patterns."""
        logger.info(f"Performing time series analysis on {date_column}")
        
        df_sorted = df.sort_values(date_column)
        
        analysis = {
            'date_column': date_column,
            'date_range': {
                'start': str(df_sorted[date_column].min()),
                'end': str(df_sorted[date_column].max()),
                'span_days': (df_sorted[date_column].max() - df_sorted[date_column].min()).days
            },
            'temporal_patterns': {}
        }
        
        # Analyze numeric columns over time
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        for col in numeric_cols[:5]:  # Limit to first 5 numeric columns
            # Calculate trend
            if df_sorted[col].notna().sum() > 1:
                x = np.arange(len(df_sorted))
                y = df_sorted[col].ffill().bfill()
                
                if len(y) > 0 and y.std() > 0:
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                    
                    analysis['temporal_patterns'][col] = {
                        'trend': 'increasing' if slope > 0 else 'decreasing',
                        'slope': float(slope),
                        'r_squared': float(r_value ** 2),
                        'p_value': float(p_value),
                        'significant': p_value < 0.05
                    }
        
        return analysis
    
    def target_variable_analysis(self, df: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """Analyze relationships with a target variable."""
        logger.info(f"Analyzing target variable: {target_column}")
        
        analysis = {
            'target_column': target_column,
            'target_type': str(df[target_column].dtype),
            'relationships': {}
        }
        
        # If target is numeric, calculate correlations
        if pd.api.types.is_numeric_dtype(df[target_column]):
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            numeric_cols.remove(target_column)
            
            for col in numeric_cols:
                if df[col].notna().sum() > 1 and df[target_column].notna().sum() > 1:
                    corr = df[col].corr(df[target_column])
                    if not np.isnan(corr):
                        analysis['relationships'][col] = {
                            'correlation': float(corr),
                            'strength': 'strong' if abs(corr) > 0.7 else 'moderate' if abs(corr) > 0.4 else 'weak'
                        }
        
        # If target is categorical, perform group analysis
        else:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            for col in numeric_cols[:5]:  # Limit to first 5
                group_means = df.groupby(target_column)[col].mean()
                
                analysis['relationships'][col] = {
                    'group_means': group_means.to_dict(),
                    'variance_between_groups': float(group_means.std())
                }
        
        return analysis
    
    def generate_insights(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate human-readable insights from analysis results."""
        insights = []
        
        # Correlation insights
        if 'correlation_analysis' in analysis_results:
            strong_corr = analysis_results['correlation_analysis'].get('strong_correlations', [])
            if strong_corr:
                insights.append(f"Found {len(strong_corr)} strong correlations between variables")
                for corr in strong_corr[:3]:  # Top 3
                    insights.append(
                        f"  - {corr['variable1']} and {corr['variable2']}: "
                        f"{corr['correlation']:.2f} ({corr['strength']})"
                    )
        
        # Outlier insights
        if 'outlier_analysis' in analysis_results:
            outlier_cols = analysis_results['outlier_analysis'].get('columns_with_outliers', [])
            if outlier_cols:
                insights.append(f"Detected outliers in {len(outlier_cols)} columns")
        
        # Distribution insights
        if 'distribution_analysis' in analysis_results:
            non_normal = [
                col for col, data in analysis_results['distribution_analysis'].items()
                if not data.get('is_normal', True)
            ]
            if non_normal:
                insights.append(f"{len(non_normal)} columns show non-normal distributions")
        
        # Missing value insights
        if 'missing_value_analysis' in analysis_results:
            missing_pct = analysis_results['missing_value_analysis'].get('missing_percentage_overall', 0)
            if missing_pct > 5:
                insights.append(f"Dataset has {missing_pct:.1f}% missing values overall")
        
        return insights


# Made with Bob