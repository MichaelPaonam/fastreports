"""
Data Validation Module
Validates cleaned data to ensure quality and integrity
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataValidator:
    """Validates cleaned data against quality criteria."""
    
    def __init__(self):
        """Initialize the validator."""
        self.validation_results = {}
    
    def validate_cleaned_data(
        self,
        original_df: pd.DataFrame,
        cleaned_df: pd.DataFrame,
        dataset_name: str,
        allow_row_reduction: bool = True
    ) -> Dict[str, Any]:
        """
        Validate cleaned data against original data.
        
        Args:
            original_df: Original dataframe before cleaning
            cleaned_df: Cleaned dataframe
            dataset_name: Name of the dataset
            allow_row_reduction: Whether row count reduction is allowed (e.g., duplicate removal)
        
        Returns:
            Dictionary containing validation results
        """
        logger.info(f"Validating cleaned data for {dataset_name}")
        
        results = {
            'dataset_name': dataset_name,
            'is_valid': True,
            'validations': [],
            'warnings': [],
            'errors': []
        }
        
        # Validation 1: Row count check
        row_check = self._validate_row_count(original_df, cleaned_df, allow_row_reduction)
        results['validations'].append(row_check)
        if not row_check['passed']:
            results['errors'].append(row_check['message'])
            results['is_valid'] = False
        
        # Validation 2: Column preservation
        col_check = self._validate_columns(original_df, cleaned_df)
        results['validations'].append(col_check)
        if not col_check['passed']:
            results['warnings'].append(col_check['message'])
        
        # Validation 3: Data type consistency
        type_check = self._validate_data_types(original_df, cleaned_df)
        results['validations'].append(type_check)
        if not type_check['passed']:
            results['warnings'].append(type_check['message'])
        
        # Validation 4: Missing value improvement
        missing_check = self._validate_missing_values(original_df, cleaned_df)
        results['validations'].append(missing_check)
        if not missing_check['passed']:
            results['warnings'].append(missing_check['message'])
        
        # Validation 5: Value range checks
        range_check = self._validate_value_ranges(cleaned_df)
        results['validations'].append(range_check)
        if not range_check['passed']:
            results['warnings'].append(range_check['message'])
        
        # Validation 6: Duplicate check
        dup_check = self._validate_duplicates(cleaned_df)
        results['validations'].append(dup_check)
        if not dup_check['passed']:
            results['warnings'].append(dup_check['message'])
        
        # Calculate overall validation score
        passed_count = sum(1 for v in results['validations'] if v['passed'])
        total_count = len(results['validations'])
        results['validation_score'] = (passed_count / total_count) * 100
        
        logger.info(f"Validation complete. Score: {results['validation_score']:.1f}%")
        
        return results
    
    def _validate_row_count(
        self,
        original_df: pd.DataFrame,
        cleaned_df: pd.DataFrame,
        allow_reduction: bool
    ) -> Dict[str, Any]:
        """Validate row count preservation."""
        original_rows = len(original_df)
        cleaned_rows = len(cleaned_df)
        
        if cleaned_rows > original_rows:
            return {
                'name': 'Row Count',
                'passed': False,
                'message': f"Row count increased from {original_rows} to {cleaned_rows}",
                'original': original_rows,
                'cleaned': cleaned_rows
            }
        
        if cleaned_rows < original_rows and not allow_reduction:
            return {
                'name': 'Row Count',
                'passed': False,
                'message': f"Row count decreased from {original_rows} to {cleaned_rows} (not allowed)",
                'original': original_rows,
                'cleaned': cleaned_rows
            }
        
        return {
            'name': 'Row Count',
            'passed': True,
            'message': f"Row count: {original_rows} → {cleaned_rows}",
            'original': original_rows,
            'cleaned': cleaned_rows
        }
    
    def _validate_columns(
        self,
        original_df: pd.DataFrame,
        cleaned_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """Validate column preservation."""
        original_cols = set(original_df.columns)
        cleaned_cols = set(cleaned_df.columns)
        
        missing_cols = original_cols - cleaned_cols
        new_cols = cleaned_cols - original_cols
        
        if missing_cols:
            return {
                'name': 'Column Preservation',
                'passed': False,
                'message': f"Missing columns: {missing_cols}",
                'missing_columns': list(missing_cols),
                'new_columns': list(new_cols)
            }
        
        return {
            'name': 'Column Preservation',
            'passed': True,
            'message': f"All {len(original_cols)} columns preserved",
            'missing_columns': [],
            'new_columns': list(new_cols)
        }
    
    def _validate_data_types(
        self,
        original_df: pd.DataFrame,
        cleaned_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """Validate data type consistency or improvement."""
        type_changes = []
        
        for col in original_df.columns:
            if col in cleaned_df.columns:
                orig_type = str(original_df[col].dtype)
                clean_type = str(cleaned_df[col].dtype)
                
                if orig_type != clean_type:
                    type_changes.append({
                        'column': col,
                        'original': orig_type,
                        'cleaned': clean_type
                    })
        
        return {
            'name': 'Data Type Consistency',
            'passed': True,
            'message': f"{len(type_changes)} type changes detected",
            'type_changes': type_changes
        }
    
    def _validate_missing_values(
        self,
        original_df: pd.DataFrame,
        cleaned_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """Validate that missing values were reduced or handled."""
        original_missing = original_df.isnull().sum().sum()
        cleaned_missing = cleaned_df.isnull().sum().sum()
        
        improvement = original_missing - cleaned_missing
        improvement_pct = (improvement / original_missing * 100) if original_missing > 0 else 0
        
        if cleaned_missing > original_missing:
            return {
                'name': 'Missing Value Handling',
                'passed': False,
                'message': f"Missing values increased from {original_missing} to {cleaned_missing}",
                'original_missing': int(original_missing),
                'cleaned_missing': int(cleaned_missing),
                'improvement': int(improvement)
            }
        
        return {
            'name': 'Missing Value Handling',
            'passed': True,
            'message': f"Missing values reduced by {improvement} ({improvement_pct:.1f}%)",
            'original_missing': int(original_missing),
            'cleaned_missing': int(cleaned_missing),
            'improvement': int(improvement)
        }
    
    def _validate_value_ranges(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate that numeric values are within reasonable ranges."""
        issues = []
        
        for col in df.select_dtypes(include=[np.number]).columns:
            # Check for infinite values
            if np.isinf(df[col]).any():
                issues.append(f"{col}: Contains infinite values")
            
            # Check for extremely large values (potential outliers)
            if df[col].max() > 1e10:
                issues.append(f"{col}: Contains extremely large values (>{1e10})")
            
            # Check for negative values in columns that shouldn't have them
            if 'count' in col.lower() or 'age' in col.lower() or 'price' in col.lower():
                if (df[col] < 0).any():
                    issues.append(f"{col}: Contains negative values")
        
        return {
            'name': 'Value Range Validation',
            'passed': len(issues) == 0,
            'message': f"Found {len(issues)} range issues" if issues else "All values within valid ranges",
            'issues': issues
        }
    
    def _validate_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check for duplicate rows."""
        duplicate_count = df.duplicated().sum()
        
        return {
            'name': 'Duplicate Check',
            'passed': duplicate_count == 0,
            'message': f"Found {duplicate_count} duplicate rows" if duplicate_count > 0 else "No duplicates found",
            'duplicate_count': int(duplicate_count)
        }
    
    def validate_business_rules(
        self,
        df: pd.DataFrame,
        rules: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validate custom business rules.
        
        Args:
            df: Dataframe to validate
            rules: List of rule dictionaries with 'name', 'condition', and 'message'
        
        Returns:
            Dictionary containing rule validation results
        """
        results = {
            'rules_checked': len(rules),
            'rules_passed': 0,
            'rules_failed': 0,
            'details': []
        }
        
        for rule in rules:
            try:
                # Evaluate the condition
                passed = eval(rule['condition'], {'df': df, 'pd': pd, 'np': np})
                
                if passed:
                    results['rules_passed'] += 1
                else:
                    results['rules_failed'] += 1
                
                results['details'].append({
                    'name': rule['name'],
                    'passed': bool(passed),
                    'message': rule.get('message', '')
                })
            except Exception as e:
                logger.error(f"Error evaluating rule '{rule['name']}': {e}")
                results['rules_failed'] += 1
                results['details'].append({
                    'name': rule['name'],
                    'passed': False,
                    'message': f"Error: {str(e)}"
                })
        
        return results
    
    def generate_validation_report(self, validation_results: Dict[str, Any]) -> str:
        """
        Generate a human-readable validation report.
        
        Args:
            validation_results: Results from validate_cleaned_data
        
        Returns:
            Formatted validation report string
        """
        report = []
        report.append("=" * 80)
        report.append(f"DATA VALIDATION REPORT: {validation_results['dataset_name']}")
        report.append("=" * 80)
        report.append("")
        
        # Overall status
        status = "✓ PASSED" if validation_results['is_valid'] else "✗ FAILED"
        report.append(f"Overall Status: {status}")
        report.append(f"Validation Score: {validation_results['validation_score']:.1f}%")
        report.append("")
        
        # Individual validations
        report.append("Validation Details:")
        report.append("-" * 80)
        for validation in validation_results['validations']:
            status_icon = "✓" if validation['passed'] else "✗"
            report.append(f"{status_icon} {validation['name']}: {validation['message']}")
        
        # Errors
        if validation_results['errors']:
            report.append("")
            report.append("ERRORS:")
            for error in validation_results['errors']:
                report.append(f"  ✗ {error}")
        
        # Warnings
        if validation_results['warnings']:
            report.append("")
            report.append("WARNINGS:")
            for warning in validation_results['warnings']:
                report.append(f"  ⚠ {warning}")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)


# Made with Bob