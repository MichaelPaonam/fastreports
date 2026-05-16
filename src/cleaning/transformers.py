"""
Data Transformers Module
Applies cleaning transformations to data based on strategies.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime
from src.cleaning.strategy_generator import CleaningStrategy
from src.utils.logger import get_logger

logger = get_logger("cleaning.transformers")


class DataTransformer:
    """Applies cleaning transformations to DataFrames."""
    
    def __init__(self):
        self.logger = logger
        self.transformation_log: List[Dict[str, Any]] = []
    
    def apply_strategies(self, df: pd.DataFrame, 
                        strategies: List[CleaningStrategy]) -> pd.DataFrame:
        """
        Apply cleaning strategies to DataFrame.
        
        Args:
            df: DataFrame to clean
            strategies: List of cleaning strategies
            
        Returns:
            Cleaned DataFrame
        """
        self.logger.info(f"Applying {len(strategies)} cleaning strategies")
        self.transformation_log = []
        
        # Create a copy to avoid modifying original
        cleaned_df = df.copy()
        
        # Group strategies by execution order
        strategy_groups = self._group_strategies_by_order(strategies)
        
        # Apply strategies in order
        for group_name in strategy_groups['execution_order']:
            if group_name in strategy_groups['by_issue_type']:
                group_strategies = strategy_groups['by_issue_type'][group_name]
                self.logger.info(f"Applying {len(group_strategies)} {group_name} strategies")
                
                for strategy in group_strategies:
                    cleaned_df = self._apply_single_strategy(cleaned_df, strategy)
        
        self.logger.info(f"Applied {len(self.transformation_log)} transformations")
        return cleaned_df
    
    def _group_strategies_by_order(self, strategies: List[CleaningStrategy]) -> Dict[str, Any]:
        """Group strategies by execution order."""
        by_issue = {}
        for strategy in strategies:
            issue = strategy.issue_type
            if issue not in by_issue:
                by_issue[issue] = []
            by_issue[issue].append(strategy)
        
        return {
            'by_issue_type': by_issue,
            'execution_order': [
                'irrelevant_columns',  # Remove irrelevant columns first
                'data_types',
                'inconsistencies',
                'missing_values',
                'outliers',
                'value_ranges',
                'duplicates'
            ]
        }
    
    def _apply_single_strategy(self, df: pd.DataFrame, 
                              strategy: CleaningStrategy) -> pd.DataFrame:
        """Apply a single cleaning strategy."""
        try:
            before_state = self._capture_state(df, strategy.column)
            
            # Apply transformation based on strategy type
            if strategy.strategy == 'mean':
                df = self._fill_with_mean(df, strategy)
            elif strategy.strategy == 'median':
                df = self._fill_with_median(df, strategy)
            elif strategy.strategy == 'mode':
                df = self._fill_with_mode(df, strategy)
            elif strategy.strategy == 'forward_fill':
                df = self._forward_fill(df, strategy)
            elif strategy.strategy == 'remove':
                df = self._remove_duplicates(df, strategy)
            elif strategy.strategy == 'cap':
                df = self._cap_outliers(df, strategy)
            elif strategy.strategy == 'trim_whitespace':
                df = self._trim_whitespace(df, strategy)
            elif strategy.strategy == 'normalize_case':
                df = self._normalize_case(df, strategy)
            elif strategy.strategy == 'replace_empty_strings':
                df = self._replace_empty_strings(df, strategy)
            elif strategy.strategy == 'convert_to_numeric':
                df = self._convert_to_numeric(df, strategy)
            elif strategy.strategy == 'convert_to_datetime':
                df = self._convert_to_datetime(df, strategy)
            elif strategy.strategy == 'cap_values':
                df = self._cap_values(df, strategy)
            elif strategy.strategy == 'drop_column':
                df = self._drop_column(df, strategy)
            else:
                self.logger.warning(f"Unknown strategy: {strategy.strategy}")
            
            after_state = self._capture_state(df, strategy.column)
            self._log_transformation(strategy, before_state, after_state)
            
        except Exception as e:
            self.logger.error(f"Error applying strategy {strategy.strategy} to {strategy.column}: {e}")
        
        return df
    
    def _fill_with_mean(self, df: pd.DataFrame, strategy: CleaningStrategy) -> pd.DataFrame:
        """Fill missing values with mean."""
        col = strategy.column
        fill_value = strategy.parameters.get('fill_value')
        df[col].fillna(fill_value, inplace=True)
        return df
    
    def _fill_with_median(self, df: pd.DataFrame, strategy: CleaningStrategy) -> pd.DataFrame:
        """Fill missing values with median."""
        col = strategy.column
        fill_value = strategy.parameters.get('fill_value')
        df[col].fillna(fill_value, inplace=True)
        return df
    
    def _fill_with_mode(self, df: pd.DataFrame, strategy: CleaningStrategy) -> pd.DataFrame:
        """Fill missing values with mode."""
        col = strategy.column
        fill_value = strategy.parameters.get('fill_value')
        df[col].fillna(fill_value, inplace=True)
        return df
    
    def _forward_fill(self, df: pd.DataFrame, strategy: CleaningStrategy) -> pd.DataFrame:
        """Forward fill missing values."""
        col = strategy.column
        df[col].fillna(method='ffill', inplace=True)
        # Backward fill any remaining NaN at the start
        df[col].fillna(method='bfill', inplace=True)
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame, strategy: CleaningStrategy) -> pd.DataFrame:
        """Remove duplicate rows."""
        keep = strategy.parameters.get('keep', 'first')
        return df.drop_duplicates(keep=keep)
    
    def _cap_outliers(self, df: pd.DataFrame, strategy: CleaningStrategy) -> pd.DataFrame:
        """Cap outliers at specified bounds."""
        col = strategy.column
        lower_bound = strategy.parameters.get('lower_bound')
        upper_bound = strategy.parameters.get('upper_bound')
        
        if lower_bound is not None:
            df[col] = df[col].clip(lower=lower_bound)
        if upper_bound is not None:
            df[col] = df[col].clip(upper=upper_bound)
        
        return df
    
    def _trim_whitespace(self, df: pd.DataFrame, strategy: CleaningStrategy) -> pd.DataFrame:
        """Trim leading and trailing whitespace."""
        col = strategy.column
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip()
        return df
    
    def _normalize_case(self, df: pd.DataFrame, strategy: CleaningStrategy) -> pd.DataFrame:
        """Normalize text case."""
        col = strategy.column
        case = strategy.parameters.get('case', 'lower')
        
        if df[col].dtype == 'object':
            if case == 'lower':
                df[col] = df[col].str.lower()
            elif case == 'upper':
                df[col] = df[col].str.upper()
            elif case == 'title':
                df[col] = df[col].str.title()
        
        return df
    
    def _replace_empty_strings(self, df: pd.DataFrame, strategy: CleaningStrategy) -> pd.DataFrame:
        """Replace empty strings with NaN."""
        col = strategy.column
        if df[col].dtype == 'object':
            df[col] = df[col].replace('', np.nan)
        return df
    
    def _convert_to_numeric(self, df: pd.DataFrame, strategy: CleaningStrategy) -> pd.DataFrame:
        """Convert column to numeric type."""
        col = strategy.column
        df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    
    def _convert_to_datetime(self, df: pd.DataFrame, strategy: CleaningStrategy) -> pd.DataFrame:
        """Convert column to datetime type."""
        col = strategy.column
        df[col] = pd.to_datetime(df[col], errors='coerce')
        return df
    
    def _cap_values(self, df: pd.DataFrame, strategy: CleaningStrategy) -> pd.DataFrame:
        """Cap values at min/max bounds."""
        col = strategy.column
        min_value = strategy.parameters.get('min_value')
        max_value = strategy.parameters.get('max_value')
        
        if min_value is not None:
            df[col] = df[col].clip(lower=min_value)
        if max_value is not None:
            df[col] = df[col].clip(upper=max_value)
        
        return df
    
    def _drop_column(self, df: pd.DataFrame, strategy: CleaningStrategy) -> pd.DataFrame:
        """Drop irrelevant column."""
        col = strategy.column
        reason = strategy.parameters.get('reason', 'irrelevant')
        
        if col in df.columns:
            df = df.drop(columns=[col])
            self.logger.info(f"Dropped column '{col}' (reason: {reason})")
        
        return df
    
    def _capture_state(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """Capture state of column before transformation."""
        if column == '__all__':
            return {
                'rows': len(df),
                'columns': len(df.columns)
            }
        
        if column not in df.columns:
            return {}
        
        return {
            'null_count': int(df[column].isnull().sum()),
            'unique_count': int(df[column].nunique()),
            'dtype': str(df[column].dtype)
        }
    
    def _log_transformation(self, strategy: CleaningStrategy, 
                          before: Dict[str, Any], after: Dict[str, Any]):
        """Log transformation details."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'column': strategy.column,
            'strategy': strategy.strategy,
            'issue_type': strategy.issue_type,
            'before': before,
            'after': after,
            'parameters': strategy.parameters
        }
        
        self.transformation_log.append(log_entry)
        
        # Log changes
        if strategy.column != '__all__':
            null_change = before.get('null_count', 0) - after.get('null_count', 0)
            if null_change != 0:
                self.logger.debug(f"{strategy.column}: Filled {null_change} missing values")
    
    def get_transformation_summary(self) -> Dict[str, Any]:
        """Get summary of all transformations applied."""
        if not self.transformation_log:
            return {
                'total_transformations': 0,
                'message': 'No transformations applied'
            }
        
        # Count by strategy type
        by_strategy = {}
        for entry in self.transformation_log:
            strategy = entry['strategy']
            by_strategy[strategy] = by_strategy.get(strategy, 0) + 1
        
        # Count by issue type
        by_issue = {}
        for entry in self.transformation_log:
            issue = entry['issue_type']
            by_issue[issue] = by_issue.get(issue, 0) + 1
        
        return {
            'total_transformations': len(self.transformation_log),
            'by_strategy': by_strategy,
            'by_issue_type': by_issue,
            'transformations': self.transformation_log
        }
    
    def generate_report(self) -> str:
        """Generate human-readable transformation report."""
        summary = self.get_transformation_summary()
        
        if summary['total_transformations'] == 0:
            return "No transformations applied - data was already clean!"
        
        report = f"""
DATA TRANSFORMATION REPORT
{'=' * 80}

Total Transformations: {summary['total_transformations']}

By Strategy Type:
"""
        
        for strategy, count in summary['by_strategy'].items():
            report += f"  - {strategy}: {count}\n"
        
        report += "\nBy Issue Type:\n"
        for issue, count in summary['by_issue_type'].items():
            report += f"  - {issue}: {count}\n"
        
        report += f"\n{'=' * 80}\n"
        
        return report


# Example usage
if __name__ == "__main__":
    # Create sample data
    df = pd.DataFrame({
        'id': range(1, 11),
        'name': ['  User1  ', 'User2', 'user3', None, 'User5', 
                 'User6', 'user7', 'User8', None, 'User10'],
        'age': [25, 30, None, 40, 35, None, 28, 32, 45, None],
        'score': [85.5, 90.0, 78.5, None, 88.0, 92.5, None, 87.0, 91.5, 89.0]
    })
    
    print("Original DataFrame:")
    print(df)
    print(f"\nMissing values:\n{df.isnull().sum()}")
    
    # Create strategies
    strategies = [
        CleaningStrategy('name', 'inconsistencies', 'trim_whitespace'),
        CleaningStrategy('name', 'inconsistencies', 'normalize_case', {'case': 'lower'}),
        CleaningStrategy('age', 'missing_values', 'median', {'fill_value': df['age'].median()}),
        CleaningStrategy('score', 'missing_values', 'mean', {'fill_value': df['score'].mean()})
    ]
    
    # Apply transformations
    transformer = DataTransformer()
    cleaned_df = transformer.apply_strategies(df, strategies)
    
    print("\nCleaned DataFrame:")
    print(cleaned_df)
    print(f"\nMissing values after cleaning:\n{cleaned_df.isnull().sum()}")
    
    # Print report
    print(transformer.generate_report())

# Made with Bob
