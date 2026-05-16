"""
Cleaning Strategy Generator
Generates data cleaning strategies based on quality issues.
"""

import pandas as pd
from typing import Dict, Any, List
from src.utils.logger import get_logger
from src.utils.config_loader import get_config

logger = get_logger("cleaning.strategy_generator")


class CleaningStrategy:
    """Represents a cleaning strategy for a specific issue."""
    
    def __init__(self, column: str, issue_type: str, strategy: str,
                 parameters: Dict[str, Any] | None = None):
        self.column = column
        self.issue_type = issue_type
        self.strategy = strategy
        self.parameters = parameters or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'column': self.column,
            'issue_type': self.issue_type,
            'strategy': self.strategy,
            'parameters': self.parameters
        }


class StrategyGenerator:
    """Generates cleaning strategies based on data quality issues."""
    
    def __init__(self):
        self.logger = logger
        self.config = get_config()
    
    def generate_strategies(self, df: pd.DataFrame, 
                          quality_result: Dict[str, Any]) -> List[CleaningStrategy]:
        """
        Generate cleaning strategies based on quality issues.
        
        Args:
            df: DataFrame to clean
            quality_result: Quality check results
            
        Returns:
            List of cleaning strategies
        """
        self.logger.info("Generating cleaning strategies")
        
        strategies = []
        
        # Process each issue
        for issue in quality_result.get('issues', []):
            issue_strategies = self._generate_strategy_for_issue(df, issue)
            strategies.extend(issue_strategies)
        
        self.logger.info(f"Generated {len(strategies)} cleaning strategies")
        return strategies
    
    def _generate_strategy_for_issue(self, df: pd.DataFrame, 
                                    issue: Dict[str, Any]) -> List[CleaningStrategy]:
        """Generate strategies for a specific issue."""
        strategies = []
        category = issue.get('category')
        affected_columns = issue.get('affected_columns', [])
        
        if category == 'missing_values':
            strategies.extend(self._strategy_for_missing_values(df, affected_columns))
        elif category == 'duplicates':
            strategies.append(self._strategy_for_duplicates())
        elif category == 'outliers':
            strategies.extend(self._strategy_for_outliers(df, affected_columns))
        elif category == 'inconsistencies':
            strategies.extend(self._strategy_for_inconsistencies(df, affected_columns))
        elif category == 'data_types':
            strategies.extend(self._strategy_for_data_types(df, affected_columns))
        elif category == 'value_ranges':
            strategies.extend(self._strategy_for_value_ranges(df, affected_columns))
        elif category == 'irrelevant_columns':
            strategies.extend(self._strategy_for_irrelevant_columns(df, affected_columns))
        
        return strategies
    
    def _strategy_for_missing_values(self, df: pd.DataFrame, 
                                    columns: List[str]) -> List[CleaningStrategy]:
        """Generate strategies for missing values."""
        strategies = []
        
        for col in columns:
            if col not in df.columns:
                continue
            
            # Determine strategy based on data type
            if pd.api.types.is_numeric_dtype(df[col]):
                strategy_name = self.config.get('cleaning.missing_value_strategy.numeric', 'median')
                
                if strategy_name == 'mean':
                    value = df[col].mean()
                elif strategy_name == 'median':
                    value = df[col].median()
                elif strategy_name == 'mode':
                    value = df[col].mode()[0] if not df[col].mode().empty else 0
                else:
                    value = None
                
                strategies.append(CleaningStrategy(
                    column=col,
                    issue_type='missing_values',
                    strategy=strategy_name,
                    parameters={'fill_value': value}
                ))
            
            elif pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
                strategy_name = self.config.get('cleaning.missing_value_strategy.categorical', 'mode')
                
                if strategy_name == 'mode':
                    value = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
                elif strategy_name == 'constant':
                    value = 'Unknown'
                else:
                    value = None
                
                strategies.append(CleaningStrategy(
                    column=col,
                    issue_type='missing_values',
                    strategy=strategy_name,
                    parameters={'fill_value': value}
                ))
            
            else:
                # For other types, use forward fill
                strategies.append(CleaningStrategy(
                    column=col,
                    issue_type='missing_values',
                    strategy='forward_fill',
                    parameters={}
                ))
        
        return strategies
    
    def _strategy_for_duplicates(self) -> CleaningStrategy:
        """Generate strategy for duplicate rows."""
        remove_duplicates = self.config.get('cleaning.remove_duplicates', True)
        
        return CleaningStrategy(
            column='__all__',
            issue_type='duplicates',
            strategy='remove' if remove_duplicates else 'keep',
            parameters={'keep': 'first'}
        )
    
    def _strategy_for_outliers(self, df: pd.DataFrame, 
                              columns: List[str]) -> List[CleaningStrategy]:
        """Generate strategies for outliers."""
        strategies = []
        outlier_strategy = self.config.get('cleaning.outlier_strategy', 'cap')
        
        for col in columns:
            if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
                continue
            
            # Calculate bounds using IQR method
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            strategies.append(CleaningStrategy(
                column=col,
                issue_type='outliers',
                strategy=outlier_strategy,
                parameters={
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }
            ))
        
        return strategies
    
    def _strategy_for_inconsistencies(self, df: pd.DataFrame, 
                                     columns: List[str]) -> List[CleaningStrategy]:
        """Generate strategies for inconsistencies."""
        strategies = []
        
        for col in columns:
            if col not in df.columns:
                continue
            
            # Trim whitespace
            strategies.append(CleaningStrategy(
                column=col,
                issue_type='inconsistencies',
                strategy='trim_whitespace',
                parameters={}
            ))
            
            # Normalize case (lowercase)
            strategies.append(CleaningStrategy(
                column=col,
                issue_type='inconsistencies',
                strategy='normalize_case',
                parameters={'case': 'lower'}
            ))
            
            # Replace empty strings with NaN
            strategies.append(CleaningStrategy(
                column=col,
                issue_type='inconsistencies',
                strategy='replace_empty_strings',
                parameters={}
            ))
        
        return strategies
    
    def _strategy_for_data_types(self, df: pd.DataFrame, 
                                columns: List[str]) -> List[CleaningStrategy]:
        """Generate strategies for data type issues."""
        strategies = []
        
        for col in columns:
            if col not in df.columns:
                continue
            
            # Try to infer correct data type
            if df[col].dtype == 'object':
                # Check if it should be numeric
                try:
                    pd.to_numeric(df[col], errors='raise')
                    strategies.append(CleaningStrategy(
                        column=col,
                        issue_type='data_types',
                        strategy='convert_to_numeric',
                        parameters={}
                    ))
                except (ValueError, TypeError):
                    # Check if it should be datetime
                    try:
                        pd.to_datetime(df[col], errors='raise')
                        strategies.append(CleaningStrategy(
                            column=col,
                            issue_type='data_types',
                            strategy='convert_to_datetime',
                            parameters={}
                        ))
                    except (ValueError, TypeError):
                        pass
        
        return strategies
    
    def _strategy_for_value_ranges(self, df: pd.DataFrame,
                                  columns: List[str]) -> List[CleaningStrategy]:
        """Generate strategies for invalid value ranges."""
        strategies = []
        
        for col in columns:
            if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
                continue
            
            # For age columns, cap at reasonable values
            if 'age' in col.lower():
                strategies.append(CleaningStrategy(
                    column=col,
                    issue_type='value_ranges',
                    strategy='cap_values',
                    parameters={'min_value': 0, 'max_value': 120}
                ))
            
            # For count/quantity columns, ensure non-negative
            elif 'count' in col.lower() or 'quantity' in col.lower():
                strategies.append(CleaningStrategy(
                    column=col,
                    issue_type='value_ranges',
                    strategy='cap_values',
                    parameters={'min_value': 0, 'max_value': None}
                ))
        
        return strategies
    
    def _strategy_for_irrelevant_columns(self, df: pd.DataFrame,
                                        columns: List[str]) -> List[CleaningStrategy]:
        """Generate strategies for irrelevant columns."""
        strategies = []
        
        for col in columns:
            if col not in df.columns:
                continue
            
            # Check if column is completely empty
            if df[col].isnull().all():
                strategies.append(CleaningStrategy(
                    column=col,
                    issue_type='irrelevant_columns',
                    strategy='drop_column',
                    parameters={'reason': 'completely_empty'}
                ))
            
            # Check if column has only one unique value
            elif df[col].nunique() == 1:
                strategies.append(CleaningStrategy(
                    column=col,
                    issue_type='irrelevant_columns',
                    strategy='drop_column',
                    parameters={'reason': 'constant_value'}
                ))
            
            # Check if column has >95% null values
            elif df[col].isnull().sum() / len(df) > 0.95:
                strategies.append(CleaningStrategy(
                    column=col,
                    issue_type='irrelevant_columns',
                    strategy='drop_column',
                    parameters={'reason': 'mostly_null'}
                ))
        
        return strategies
    
    def generate_cleaning_plan(self, strategies: List[CleaningStrategy]) -> Dict[str, Any]:
        """
        Generate a comprehensive cleaning plan.
        
        Args:
            strategies: List of cleaning strategies
            
        Returns:
            Cleaning plan dictionary
        """
        # Group strategies by column
        by_column = {}
        for strategy in strategies:
            col = strategy.column
            if col not in by_column:
                by_column[col] = []
            by_column[col].append(strategy.to_dict())
        
        # Group strategies by issue type
        by_issue = {}
        for strategy in strategies:
            issue = strategy.issue_type
            if issue not in by_issue:
                by_issue[issue] = []
            by_issue[issue].append(strategy.to_dict())
        
        plan = {
            'total_strategies': len(strategies),
            'by_column': by_column,
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
        
        return plan
    
    def generate_summary(self, strategies: List[CleaningStrategy]) -> str:
        """Generate human-readable summary of cleaning strategies."""
        if not strategies:
            return "No cleaning strategies needed - data quality is good!"
        
        summary = f"""
CLEANING STRATEGY SUMMARY
{'=' * 80}

Total Strategies: {len(strategies)}

Strategies by Issue Type:
"""
        
        # Group by issue type
        by_issue = {}
        for strategy in strategies:
            issue = strategy.issue_type
            if issue not in by_issue:
                by_issue[issue] = []
            by_issue[issue].append(strategy)
        
        for issue_type, strats in by_issue.items():
            summary += f"\n  {issue_type.upper()}: {len(strats)} strategies\n"
            for strat in strats[:3]:  # Show first 3
                summary += f"    - {strat.column}: {strat.strategy}\n"
            if len(strats) > 3:
                summary += f"    ... and {len(strats) - 3} more\n"
        
        summary += f"\n{'=' * 80}\n"
        
        return summary


# Example usage
if __name__ == "__main__":
    # Create sample data with issues
    df = pd.DataFrame({
        'id': range(1, 101),
        'name': ['  User' + str(i) + '  ' if i % 5 == 0 else 'User' + str(i) for i in range(1, 101)],
        'age': [i if i % 10 != 0 else None for i in range(18, 118)],
        'score': [i * 1.5 if i % 15 != 0 else None for i in range(1, 101)]
    })
    
    # Mock quality result
    quality_result = {
        'issues': [
            {
                'category': 'missing_values',
                'affected_columns': ['age', 'score']
            },
            {
                'category': 'inconsistencies',
                'affected_columns': ['name']
            }
        ]
    }
    
    # Generate strategies
    generator = StrategyGenerator()
    strategies = generator.generate_strategies(df, quality_result)
    
    # Print summary
    print(generator.generate_summary(strategies))
    
    # Print plan
    plan = generator.generate_cleaning_plan(strategies)
    print(f"\nExecution order: {plan['execution_order']}")

# Made with Bob
