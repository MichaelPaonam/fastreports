"""
Transaction Analyzer Module
Analyzes purchase patterns, customer behavior, and revenue metrics
Optimized for e-commerce and transaction data
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TransactionAnalyzer:
    """
    Analyzer for transaction and purchase data.
    Provides insights into customer behavior, revenue patterns, and purchase trends.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize transaction analyzer.
        
        Args:
            df: DataFrame with transaction data
        """
        self.df = df.copy()
        self.customer_col = self._detect_customer_column()
        self.amount_col = self._detect_amount_column()
        self.date_col = self._detect_date_column()
        self.product_col = self._detect_product_column()
        
        if self.date_col:
            self._prepare_temporal_features()
    
    def _detect_customer_column(self) -> Optional[str]:
        """Detect customer/user ID column."""
        keywords = ['customer', 'user', 'client', 'buyer', 'account', 'member']
        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in keywords):
                return col
        return None
    
    def _detect_amount_column(self) -> Optional[str]:
        """Detect amount/price/revenue column."""
        keywords = ['amount', 'price', 'total', 'revenue', 'cost', 'value', 'payment']
        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in keywords):
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    return col
        
        # Fallback: find first numeric column
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        return numeric_cols[0] if len(numeric_cols) > 0 else None
    
    def _detect_date_column(self) -> Optional[str]:
        """Detect date/timestamp column."""
        keywords = ['date', 'time', 'timestamp', 'created', 'purchased', 'order']
        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in keywords):
                return col
        
        # Check for datetime types
        for col in self.df.columns:
            if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                return col
        
        return None
    
    def _detect_product_column(self) -> Optional[str]:
        """Detect product/item column."""
        keywords = ['product', 'item', 'sku', 'article', 'goods', 'menu']
        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in keywords):
                return col
        return None
    
    def _prepare_temporal_features(self):
        """Prepare temporal features from date column."""
        if self.date_col:
            if not pd.api.types.is_datetime64_any_dtype(self.df[self.date_col]):
                self.df[self.date_col] = pd.to_datetime(self.df[self.date_col], errors='coerce')
            
            self.df = self.df.sort_values(self.date_col)
            self.df['year'] = self.df[self.date_col].dt.year
            self.df['month'] = self.df[self.date_col].dt.month
            self.df['day_of_week'] = self.df[self.date_col].dt.dayofweek
            self.df['hour'] = self.df[self.date_col].dt.hour
            self.df['day_name'] = self.df[self.date_col].dt.day_name()
            self.df['month_name'] = self.df[self.date_col].dt.month_name()
    
    def analyze_revenue(self) -> Dict[str, Any]:
        """
        Analyze revenue metrics.
        
        Returns:
            Dictionary with revenue analysis
        """
        if not self.amount_col:
            return {"error": "No amount column found"}
        
        amounts = self.df[self.amount_col].dropna()
        
        analysis = {
            "total_revenue": float(amounts.sum()),
            "average_transaction": float(amounts.mean()),
            "median_transaction": float(amounts.median()),
            "std_transaction": float(amounts.std()),
            "min_transaction": float(amounts.min()),
            "max_transaction": float(amounts.max()),
            "total_transactions": len(amounts),
            "revenue_distribution": {
                "q25": float(amounts.quantile(0.25)),
                "q50": float(amounts.quantile(0.50)),
                "q75": float(amounts.quantile(0.75)),
                "q90": float(amounts.quantile(0.90)),
                "q95": float(amounts.quantile(0.95))
            }
        }
        
        # Revenue concentration (top 20% of transactions)
        sorted_amounts = amounts.sort_values(ascending=False)
        top_20_pct = int(len(sorted_amounts) * 0.2)
        top_20_revenue = sorted_amounts.iloc[:top_20_pct].sum()
        analysis["revenue_concentration"] = {
            "top_20_percent_transactions": top_20_pct,
            "top_20_percent_revenue": float(top_20_revenue),
            "top_20_percent_share": round(top_20_revenue / amounts.sum() * 100, 2)
        }
        
        return analysis
    
    def analyze_customer_behavior(self) -> Dict[str, Any]:
        """
        Analyze customer purchase behavior.
        
        Returns:
            Dictionary with customer behavior analysis
        """
        if not self.customer_col:
            return {"error": "No customer column found"}
        
        customer_stats = self.df.groupby(self.customer_col).agg({
            self.customer_col: 'count'
        }).rename(columns={self.customer_col: 'transaction_count'})
        
        if self.amount_col:
            customer_revenue = self.df.groupby(self.customer_col)[self.amount_col].agg([
                'sum', 'mean', 'count'
            ]).rename(columns={'sum': 'total_spent', 'mean': 'avg_transaction', 'count': 'purchase_count'})
            customer_stats = customer_stats.join(customer_revenue)
        
        analysis = {
            "total_customers": len(customer_stats),
            "avg_transactions_per_customer": float(customer_stats['transaction_count'].mean()),
            "median_transactions_per_customer": float(customer_stats['transaction_count'].median()),
            "customer_distribution": {
                "one_time_buyers": int((customer_stats['transaction_count'] == 1).sum()),
                "repeat_customers": int((customer_stats['transaction_count'] > 1).sum()),
                "loyal_customers": int((customer_stats['transaction_count'] >= 5).sum()),
                "vip_customers": int((customer_stats['transaction_count'] >= 10).sum())
            }
        }
        
        if self.amount_col:
            analysis["revenue_per_customer"] = {
                "average": float(customer_stats['total_spent'].mean()),
                "median": float(customer_stats['total_spent'].median()),
                "top_10_percent": float(customer_stats['total_spent'].quantile(0.9))
            }
            
            # Customer lifetime value segments
            analysis["customer_segments"] = self._segment_customers(customer_stats)
        
        return analysis
    
    def _segment_customers(self, customer_stats: pd.DataFrame) -> Dict[str, Any]:
        """Segment customers based on spending and frequency."""
        if 'total_spent' not in customer_stats.columns:
            return {}
        
        # RFM-like segmentation
        spending_q75 = customer_stats['total_spent'].quantile(0.75)
        frequency_q75 = customer_stats['purchase_count'].quantile(0.75)
        
        segments = {
            "high_value": int(
                ((customer_stats['total_spent'] >= spending_q75) & 
                 (customer_stats['purchase_count'] >= frequency_q75)).sum()
            ),
            "high_spender_low_frequency": int(
                ((customer_stats['total_spent'] >= spending_q75) & 
                 (customer_stats['purchase_count'] < frequency_q75)).sum()
            ),
            "low_spender_high_frequency": int(
                ((customer_stats['total_spent'] < spending_q75) & 
                 (customer_stats['purchase_count'] >= frequency_q75)).sum()
            ),
            "low_value": int(
                ((customer_stats['total_spent'] < spending_q75) & 
                 (customer_stats['purchase_count'] < frequency_q75)).sum()
            )
        }
        
        return segments
    
    def analyze_purchase_patterns(self) -> Dict[str, Any]:
        """
        Analyze purchase patterns over time.
        
        Returns:
            Dictionary with purchase pattern analysis
        """
        if not self.date_col:
            return {"error": "No date column found"}
        
        analysis = {}
        
        # Daily patterns
        if 'day_name' in self.df.columns:
            daily_transactions = self.df.groupby('day_name').size()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_transactions = daily_transactions.reindex(day_order, fill_value=0)
            
            analysis["daily_patterns"] = {
                "transactions_by_day": daily_transactions.to_dict(),
                "busiest_day": daily_transactions.idxmax(),
                "slowest_day": daily_transactions.idxmin()
            }
            
            if self.amount_col:
                daily_revenue = self.df.groupby('day_name')[self.amount_col].sum()
                daily_revenue = daily_revenue.reindex(day_order, fill_value=0)
                analysis["daily_patterns"]["revenue_by_day"] = daily_revenue.to_dict()
        
        # Hourly patterns
        if 'hour' in self.df.columns:
            hourly_transactions = self.df.groupby('hour').size()
            analysis["hourly_patterns"] = {
                "transactions_by_hour": hourly_transactions.to_dict(),
                "peak_hour": int(hourly_transactions.idxmax()),
                "slowest_hour": int(hourly_transactions.idxmin())
            }
            
            if self.amount_col:
                hourly_revenue = self.df.groupby('hour')[self.amount_col].sum()
                analysis["hourly_patterns"]["revenue_by_hour"] = hourly_revenue.to_dict()
        
        # Monthly patterns
        if 'month_name' in self.df.columns:
            monthly_transactions = self.df.groupby('month_name').size()
            analysis["monthly_patterns"] = {
                "transactions_by_month": monthly_transactions.to_dict(),
                "busiest_month": monthly_transactions.idxmax(),
                "slowest_month": monthly_transactions.idxmin()
            }
            
            if self.amount_col:
                monthly_revenue = self.df.groupby('month_name')[self.amount_col].sum()
                analysis["monthly_patterns"]["revenue_by_month"] = monthly_revenue.to_dict()
        
        return analysis
    
    def analyze_product_performance(self) -> Dict[str, Any]:
        """
        Analyze product/item performance.
        
        Returns:
            Dictionary with product analysis
        """
        if not self.product_col:
            return {"error": "No product column found"}
        
        product_stats = self.df.groupby(self.product_col).agg({
            self.product_col: 'count'
        }).rename(columns={self.product_col: 'purchase_count'})
        
        if self.amount_col:
            product_revenue = self.df.groupby(self.product_col)[self.amount_col].agg([
                'sum', 'mean', 'count'
            ]).rename(columns={'sum': 'total_revenue', 'mean': 'avg_price', 'count': 'units_sold'})
            product_stats = product_stats.join(product_revenue)
        
        # Top products
        top_products = product_stats.nlargest(10, 'purchase_count')
        
        analysis = {
            "total_products": len(product_stats),
            "top_10_products": {
                str(product): {
                    "purchase_count": int(row['purchase_count']),
                    "total_revenue": float(row['total_revenue']) if 'total_revenue' in row else None,
                    "avg_price": float(row['avg_price']) if 'avg_price' in row else None
                }
                for product, row in top_products.iterrows()
            }
        }
        
        if self.amount_col:
            # Revenue contribution
            total_revenue = product_stats['total_revenue'].sum()
            top_20_pct = int(len(product_stats) * 0.2)
            top_products_revenue = product_stats.nlargest(top_20_pct, 'total_revenue')
            
            analysis["product_concentration"] = {
                "top_20_percent_products": top_20_pct,
                "top_20_percent_revenue_share": round(
                    top_products_revenue['total_revenue'].sum() / total_revenue * 100, 2
                )
            }
        
        return analysis
    
    def analyze_cohorts(self, cohort_period: str = 'M') -> Dict[str, Any]:
        """
        Analyze customer cohorts based on first purchase date.
        
        Args:
            cohort_period: Cohort period ('D', 'W', 'M', 'Q', 'Y')
            
        Returns:
            Dictionary with cohort analysis
        """
        if not self.customer_col or not self.date_col:
            return {"error": "Customer and date columns required"}
        
        # Get first purchase date for each customer
        first_purchase = self.df.groupby(self.customer_col)[self.date_col].min()
        first_purchase = first_purchase.dt.to_period(cohort_period)
        
        # Assign cohort to each transaction
        self.df['cohort'] = self.df[self.customer_col].map(first_purchase)
        self.df['transaction_period'] = self.df[self.date_col].dt.to_period(cohort_period)
        
        # Calculate cohort size
        cohort_sizes = self.df.groupby('cohort')[self.customer_col].nunique()
        
        # Calculate retention
        cohort_data = self.df.groupby(['cohort', 'transaction_period'])[self.customer_col].nunique()
        cohort_data = cohort_data.reset_index()
        
        analysis = {
            "cohort_sizes": {str(k): int(v) for k, v in cohort_sizes.items()},
            "total_cohorts": len(cohort_sizes),
            "cohort_period": cohort_period
        }
        
        return analysis
    
    def calculate_customer_lifetime_value(self) -> Dict[str, Any]:
        """
        Calculate customer lifetime value metrics.
        
        Returns:
            Dictionary with CLV analysis
        """
        if not self.customer_col or not self.amount_col:
            return {"error": "Customer and amount columns required"}
        
        customer_metrics = self.df.groupby(self.customer_col).agg({
            self.amount_col: ['sum', 'mean', 'count'],
            self.date_col: ['min', 'max'] if self.date_col else []
        })
        
        customer_metrics.columns = ['total_spent', 'avg_transaction', 'transaction_count', 
                                    'first_purchase', 'last_purchase'] if self.date_col else \
                                   ['total_spent', 'avg_transaction', 'transaction_count']
        
        if self.date_col:
            # Calculate customer lifespan in days
            customer_metrics['lifespan_days'] = (
                customer_metrics['last_purchase'] - customer_metrics['first_purchase']
            ).dt.days
            
            # Calculate purchase frequency (transactions per month)
            customer_metrics['purchase_frequency'] = (
                customer_metrics['transaction_count'] / 
                (customer_metrics['lifespan_days'] / 30 + 1)
            )
        
        analysis = {
            "average_clv": float(customer_metrics['total_spent'].mean()),
            "median_clv": float(customer_metrics['total_spent'].median()),
            "top_10_percent_clv": float(customer_metrics['total_spent'].quantile(0.9)),
            "clv_distribution": {
                "q25": float(customer_metrics['total_spent'].quantile(0.25)),
                "q50": float(customer_metrics['total_spent'].quantile(0.50)),
                "q75": float(customer_metrics['total_spent'].quantile(0.75)),
                "q90": float(customer_metrics['total_spent'].quantile(0.90))
            }
        }
        
        if self.date_col:
            analysis["average_customer_lifespan_days"] = float(customer_metrics['lifespan_days'].mean())
            analysis["average_purchase_frequency_per_month"] = float(customer_metrics['purchase_frequency'].mean())
        
        return analysis
    
    def detect_churn_risk(self, inactive_days: int = 90) -> Dict[str, Any]:
        """
        Detect customers at risk of churning.
        
        Args:
            inactive_days: Number of days of inactivity to consider churn risk
            
        Returns:
            Dictionary with churn risk analysis
        """
        if not self.customer_col or not self.date_col:
            return {"error": "Customer and date columns required"}
        
        # Get last purchase date for each customer
        last_purchase = self.df.groupby(self.customer_col)[self.date_col].max()
        current_date = self.df[self.date_col].max()
        
        # Calculate days since last purchase
        days_inactive = (current_date - last_purchase).dt.days
        
        # Categorize customers
        at_risk = (days_inactive >= inactive_days).sum()
        active = (days_inactive < inactive_days).sum()
        
        analysis = {
            "total_customers": len(days_inactive),
            "active_customers": int(active),
            "at_risk_customers": int(at_risk),
            "churn_risk_percentage": round(at_risk / len(days_inactive) * 100, 2),
            "average_days_inactive": float(days_inactive.mean()),
            "median_days_inactive": float(days_inactive.median()),
            "inactive_threshold_days": inactive_days
        }
        
        return analysis
    
    def generate_summary(self) -> Dict[str, Any]:
        """
        Generate comprehensive transaction analysis summary.
        
        Returns:
            Dictionary with complete analysis
        """
        logger.info("Generating comprehensive transaction analysis")
        
        summary = {
            "dataset_info": {
                "total_transactions": len(self.df),
                "date_range": {
                    "start": str(self.df[self.date_col].min()) if self.date_col else None,
                    "end": str(self.df[self.date_col].max()) if self.date_col else None
                } if self.date_col else None,
                "detected_columns": {
                    "customer": self.customer_col,
                    "amount": self.amount_col,
                    "date": self.date_col,
                    "product": self.product_col
                }
            }
        }
        
        # Add all analyses
        if self.amount_col:
            summary["revenue_analysis"] = self.analyze_revenue()
        
        if self.customer_col:
            summary["customer_behavior"] = self.analyze_customer_behavior()
            
            if self.amount_col:
                summary["customer_lifetime_value"] = self.calculate_customer_lifetime_value()
            
            if self.date_col:
                summary["churn_risk"] = self.detect_churn_risk()
        
        if self.date_col:
            summary["purchase_patterns"] = self.analyze_purchase_patterns()
        
        if self.product_col:
            summary["product_performance"] = self.analyze_product_performance()
        
        logger.info("Transaction analysis complete")
        return summary


# Example usage
if __name__ == "__main__":
    # Sample transaction data
    sample_data = pd.DataFrame({
        'transaction_id': range(1, 101),
        'customer_id': np.random.randint(1, 21, 100),
        'product': np.random.choice(['Pizza', 'Burger', 'Salad', 'Drink'], 100),
        'amount': np.random.uniform(5, 50, 100),
        'date': pd.date_range('2024-01-01', periods=100, freq='D')
    })
    
    analyzer = TransactionAnalyzer(sample_data)
    summary = analyzer.generate_summary()
    print("Transaction Analysis Summary:")
    print(json.dumps(summary, indent=2))


# Made with Bob