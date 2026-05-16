"""
Data Quality Checker Module
Identifies data quality issues and assigns severity levels.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from enum import Enum
from src.utils.logger import get_logger
from src.utils.config_loader import get_config

logger = get_logger("profiling.quality_checker")


class IssueSeverity(Enum):
    """Severity levels for data quality issues."""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class QualityIssue:
    """Represents a data quality issue."""
    
    def __init__(self, severity: IssueSeverity, category: str, description: str,
                 affected_columns: List[str] | None = None, count: int = 0):
        self.severity = severity
        self.category = category
        self.description = description
        self.affected_columns = affected_columns or []
        self.count = count
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'severity': self.severity.value,
            'category': self.category,
            'description': self.description,
            'affected_columns': self.affected_columns,
            'count': self.count
        }


class QualityChecker:
    """Checks data quality and identifies issues."""
    
    def __init__(self):
        self.logger = logger
        self.config = get_config()
        self.issues: List[QualityIssue] = []
    
    def check_quality(self, df: pd.DataFrame, dataset_name: str = "dataset") -> Dict[str, Any]:
        """
        Perform comprehensive quality checks.
        
        Args:
            df: DataFrame to check
            dataset_name: Name of the dataset
            
        Returns:
            Dictionary with quality check results
        """
        self.logger.info(f"Checking data quality for: {dataset_name}")
        self.issues = []
        
        # Run all quality checks
        self._check_missing_values(df)
        self._check_duplicates(df)
        self._check_outliers(df)
        self._check_data_types(df)
        self._check_inconsistencies(df)
        self._check_value_ranges(df)
        self._check_text_quality(df)
        
        # Categorize issues by severity
        critical_issues = [i for i in self.issues if i.severity == IssueSeverity.CRITICAL]
        warning_issues = [i for i in self.issues if i.severity == IssueSeverity.WARNING]
        info_issues = [i for i in self.issues if i.severity == IssueSeverity.INFO]
        
        # Calculate quality score (0-100)
        quality_score = self._calculate_quality_score(df, len(critical_issues), len(warning_issues))
        
        result = {
            'dataset_name': dataset_name,
            'quality_score': quality_score,
            'total_issues': len(self.issues),
            'critical_issues': len(critical_issues),
            'warning_issues': len(warning_issues),
            'info_issues': len(info_issues),
            'issues': [
                {
                    'severity': issue.severity.value,
                    'category': issue.category,
                    'description': issue.description,
                    'affected_columns': issue.affected_columns,
                    'count': issue.count
                }
                for issue in self.issues
            ],
            'recommendations': self._generate_recommendations()
        }
        
        self.logger.info(f"Quality check complete. Score: {quality_score}/100")
        return result
    
    def _check_missing_values(self, df: pd.DataFrame):
        """Check for missing values."""
        threshold = self.config.get('quality.missing_value_threshold', 0.5)
        
        missing_counts = df.isnull().sum()
        missing_percentages = missing_counts / len(df)
        
        for col in df.columns:
            missing_pct = missing_percentages[col]
            missing_count = missing_counts[col]
            
            if missing_pct > threshold:
                self.issues.append(QualityIssue(
                    severity=IssueSeverity.CRITICAL,
                    category="missing_values",
                    description=f"Column has {missing_pct*100:.1f}% missing values (>{threshold*100}% threshold)",
                    affected_columns=[col],
                    count=int(missing_count)
                ))
            elif missing_pct > 0.1:
                self.issues.append(QualityIssue(
                    severity=IssueSeverity.WARNING,
                    category="missing_values",
                    description=f"Column has {missing_pct*100:.1f}% missing values",
                    affected_columns=[col],
                    count=int(missing_count)
                ))
            elif missing_count > 0:
                self.issues.append(QualityIssue(
                    severity=IssueSeverity.INFO,
                    category="missing_values",
                    description=f"Column has {missing_count} missing values",
                    affected_columns=[col],
                    count=int(missing_count)
                ))
    
    def _check_duplicates(self, df: pd.DataFrame):
        """Check for duplicate rows."""
        threshold = self.config.get('quality.duplicate_threshold', 0.1)
        
        duplicate_count = df.duplicated().sum()
        duplicate_pct = duplicate_count / len(df)
        
        if duplicate_pct > threshold:
            self.issues.append(QualityIssue(
                severity=IssueSeverity.WARNING,
                category="duplicates",
                description=f"Dataset has {duplicate_pct*100:.1f}% duplicate rows (>{threshold*100}% threshold)",
                affected_columns=[],
                count=int(duplicate_count)
            ))
        elif duplicate_count > 0:
            self.issues.append(QualityIssue(
                severity=IssueSeverity.INFO,
                category="duplicates",
                description=f"Dataset has {duplicate_count} duplicate rows",
                affected_columns=[],
                count=int(duplicate_count)
            ))
    
    def _check_outliers(self, df: pd.DataFrame):
        """Check for outliers in numeric columns."""
        std_threshold = self.config.get('quality.outlier_std_threshold', 3)
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            clean_series = df[col].dropna()
            
            if len(clean_series) < 10:  # Skip if too few values
                continue
            
            # IQR method
            q1 = clean_series.quantile(0.25)
            q3 = clean_series.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            outliers = clean_series[(clean_series < lower_bound) | (clean_series > upper_bound)]
            outlier_pct = len(outliers) / len(clean_series)
            
            if outlier_pct > 0.05:  # More than 5% outliers
                self.issues.append(QualityIssue(
                    severity=IssueSeverity.WARNING,
                    category="outliers",
                    description=f"Column has {outlier_pct*100:.1f}% outliers (IQR method)",
                    affected_columns=[col],
                    count=len(outliers)
                ))
    
    def _check_data_types(self, df: pd.DataFrame):
        """Check for data type issues."""
        for col in df.columns:
            # Check if numeric column stored as object
            if df[col].dtype == 'object':
                # Try to convert to numeric
                try:
                    pd.to_numeric(df[col], errors='raise')
                    self.issues.append(QualityIssue(
                        severity=IssueSeverity.INFO,
                        category="data_types",
                        description=f"Column appears numeric but stored as text",
                        affected_columns=[col],
                        count=0
                    ))
                except (ValueError, TypeError):
                    pass
            
            # Check for mixed types in object columns
            if df[col].dtype == 'object':
                non_null = df[col].dropna()
                if len(non_null) > 0:
                    types = non_null.apply(type).unique()
                    if len(types) > 1:
                        self.issues.append(QualityIssue(
                            severity=IssueSeverity.WARNING,
                            category="data_types",
                            description=f"Column has mixed data types: {[t.__name__ for t in types]}",
                            affected_columns=[col],
                            count=len(types)
                        ))
    
    def _check_inconsistencies(self, df: pd.DataFrame):
        """Check for data inconsistencies."""
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check for inconsistent string formatting
                non_null = df[col].dropna().astype(str)
                
                if len(non_null) == 0:
                    continue
                
                # Check for leading/trailing whitespace
                has_whitespace = non_null.str.strip() != non_null
                if has_whitespace.any():
                    self.issues.append(QualityIssue(
                        severity=IssueSeverity.INFO,
                        category="inconsistencies",
                        description=f"Column has values with leading/trailing whitespace",
                        affected_columns=[col],
                        count=int(has_whitespace.sum())
                    ))
                
                # Check for mixed case
                has_lower = non_null.str.islower().any()
                has_upper = non_null.str.isupper().any()
                if has_lower and has_upper:
                    self.issues.append(QualityIssue(
                        severity=IssueSeverity.INFO,
                        category="inconsistencies",
                        description=f"Column has mixed case values",
                        affected_columns=[col],
                        count=0
                    ))
                
                # Check for empty strings
                empty_count = (non_null == '').sum()
                if empty_count > 0:
                    self.issues.append(QualityIssue(
                        severity=IssueSeverity.WARNING,
                        category="inconsistencies",
                        description=f"Column has {empty_count} empty strings",
                        affected_columns=[col],
                        count=int(empty_count)
                    ))
    
    def _check_value_ranges(self, df: pd.DataFrame):
        """Check for invalid value ranges."""
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                clean_series = df[col].dropna()
                
                if len(clean_series) == 0:
                    continue
                
                # Check for negative values in potentially positive-only columns
                if 'age' in col.lower() or 'count' in col.lower() or 'quantity' in col.lower():
                    negative_count = (clean_series < 0).sum()
                    if negative_count > 0:
                        self.issues.append(QualityIssue(
                            severity=IssueSeverity.CRITICAL,
                            category="value_ranges",
                            description=f"Column has {negative_count} negative values (should be positive)",
                            affected_columns=[col],
                            count=int(negative_count)
                        ))
                
                # Check for unrealistic age values
                if 'age' in col.lower():
                    invalid_age = ((clean_series < 0) | (clean_series > 150)).sum()
                    if invalid_age > 0:
                        self.issues.append(QualityIssue(
                            severity=IssueSeverity.CRITICAL,
                            category="value_ranges",
                            description=f"Column has {invalid_age} unrealistic age values",
                            affected_columns=[col],
                            count=int(invalid_age)
                        ))
    
    def _check_text_quality(self, df: pd.DataFrame):
        """Check text column quality."""
        for col in df.columns:
            if df[col].dtype == 'object':
                non_null = df[col].dropna().astype(str)
                
                if len(non_null) == 0:
                    continue
                
                # Check for very long text (potential data issues)
                max_length = non_null.str.len().max()
                if max_length > 1000:
                    self.issues.append(QualityIssue(
                        severity=IssueSeverity.INFO,
                        category="text_quality",
                        description=f"Column has very long text values (max: {max_length} chars)",
                        affected_columns=[col],
                        count=0
                    ))
                
                # Check for single character values (potential encoding issues)
                single_char = (non_null.str.len() == 1).sum()
                if single_char > len(non_null) * 0.1:  # More than 10%
                    self.issues.append(QualityIssue(
                        severity=IssueSeverity.WARNING,
                        category="text_quality",
                        description=f"Column has many single-character values ({single_char})",
                        affected_columns=[col],
                        count=int(single_char)
                    ))
    
    def _calculate_quality_score(self, df: pd.DataFrame, critical_count: int, warning_count: int) -> int:
        """Calculate overall quality score (0-100)."""
        # Start with perfect score
        score = 100
        
        # Deduct points for issues
        score -= critical_count * 10  # 10 points per critical issue
        score -= warning_count * 5    # 5 points per warning
        
        # Deduct for missing data
        missing_pct = df.isnull().sum().sum() / df.size
        score -= int(missing_pct * 20)  # Up to 20 points for missing data
        
        # Deduct for duplicates
        duplicate_pct = df.duplicated().sum() / len(df)
        score -= int(duplicate_pct * 10)  # Up to 10 points for duplicates
        
        # Ensure score is between 0 and 100
        return max(0, min(100, score))
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on issues found."""
        recommendations = []
        
        # Group issues by category
        issues_by_category = {}
        for issue in self.issues:
            if issue.category not in issues_by_category:
                issues_by_category[issue.category] = []
            issues_by_category[issue.category].append(issue)
        
        # Generate recommendations
        if 'missing_values' in issues_by_category:
            recommendations.append("Consider imputation strategies for missing values (mean, median, mode, or forward-fill)")
        
        if 'duplicates' in issues_by_category:
            recommendations.append("Remove duplicate rows or investigate why duplicates exist")
        
        if 'outliers' in issues_by_category:
            recommendations.append("Review outliers - consider capping, removal, or transformation")
        
        if 'data_types' in issues_by_category:
            recommendations.append("Convert columns to appropriate data types for better performance")
        
        if 'inconsistencies' in issues_by_category:
            recommendations.append("Standardize text formatting (trim whitespace, normalize case)")
        
        if 'value_ranges' in issues_by_category:
            recommendations.append("Investigate and correct invalid value ranges")
        
        return recommendations
    
    def generate_report(self, quality_result: Dict[str, Any]) -> str:
        """Generate human-readable quality report."""
        report = f"""
DATA QUALITY REPORT: {quality_result['dataset_name']}
{'=' * 80}

QUALITY SCORE: {quality_result['quality_score']}/100

ISSUES SUMMARY:
  - Total Issues: {quality_result['total_issues']}
  - Critical: {quality_result['critical_issues']}
  - Warnings: {quality_result['warning_issues']}
  - Info: {quality_result['info_issues']}

RECOMMENDATIONS:
"""
        for i, rec in enumerate(quality_result['recommendations'], 1):
            report += f"  {i}. {rec}\n"
        
        report += f"\n{'=' * 80}\n"
        
        return report


# Example usage
if __name__ == "__main__":
    # Create sample data with quality issues
    df = pd.DataFrame({
        'id': range(1, 101),
        'name': ['User' + str(i) if i % 10 != 0 else '  User' + str(i) + '  ' for i in range(1, 101)],
        'age': [np.random.randint(18, 80) if i % 15 != 0 else np.nan for i in range(100)],
        'score': [np.random.normal(75, 15) if i % 20 != 0 else np.nan for i in range(100)],
        'category': ['A' if i % 2 == 0 else 'a' for i in range(100)]  # Mixed case
    })
    
    # Add duplicates
    df = pd.concat([df, df.iloc[:5]], ignore_index=True)
    
    # Check quality
    checker = QualityChecker()
    result = checker.check_quality(df, "sample_data")
    
    # Print report
    print(checker.generate_report(result))

# Made with Bob
