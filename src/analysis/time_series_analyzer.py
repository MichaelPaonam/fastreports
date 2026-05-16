"""
Time Series Analyzer for Soccer Data
Specialized analysis for time-series sports data
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class TimeSeriesAnalyzer:
    """
    Analyzer for time-series data, specifically optimized for soccer/sports data
    """

    def __init__(self, df: pd.DataFrame, date_column: Optional[str] = None):
        """
        Initialize time series analyzer
        
        Args:
            df: DataFrame with time series data
            date_column: Name of date column (auto-detected if None)
        """
        self.df = df.copy()
        self.date_column = date_column or self._detect_date_column()
        
        if self.date_column:
            self._prepare_time_series()

    def _detect_date_column(self) -> Optional[str]:
        """Detect date column in dataframe"""
        date_keywords = ['date', 'time', 'datetime', 'timestamp', 'match_date', 'game_date']
        
        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in date_keywords):
                return col
        
        # Check for datetime types
        for col in self.df.columns:
            if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                return col
        
        return None

    def _prepare_time_series(self):
        """Prepare dataframe for time series analysis"""
        if self.date_column:
            # Convert to datetime if not already
            if not pd.api.types.is_datetime64_any_dtype(self.df[self.date_column]):
                self.df[self.date_column] = pd.to_datetime(self.df[self.date_column], errors='coerce')
            
            # Sort by date
            self.df = self.df.sort_values(self.date_column)
            
            # Extract time features
            self.df['year'] = self.df[self.date_column].dt.year
            self.df['month'] = self.df[self.date_column].dt.month
            self.df['day_of_week'] = self.df[self.date_column].dt.dayofweek
            self.df['week_of_year'] = self.df[self.date_column].dt.isocalendar().week

    def analyze_trends(self, metric_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze trends over time for specified metrics
        
        Args:
            metric_columns: List of numeric columns to analyze
            
        Returns:
            Dictionary with trend analysis
        """
        if not self.date_column:
            return {"error": "No date column found"}
        
        trends = {}
        
        for col in metric_columns:
            if col not in self.df.columns or not pd.api.types.is_numeric_dtype(self.df[col]):
                continue
            
            # Calculate rolling statistics
            rolling_mean = self.df[col].rolling(window=5, min_periods=1).mean()
            rolling_std = self.df[col].rolling(window=5, min_periods=1).std()
            
            # Calculate trend direction
            if len(self.df) > 1:
                first_half = self.df[col].iloc[:len(self.df)//2].mean()
                second_half = self.df[col].iloc[len(self.df)//2:].mean()
                trend_direction = "increasing" if second_half > first_half else "decreasing"
                trend_magnitude = abs(second_half - first_half) / first_half * 100 if first_half != 0 else 0
            else:
                trend_direction = "stable"
                trend_magnitude = 0
            
            trends[col] = {
                "trend_direction": trend_direction,
                "trend_magnitude_percent": round(trend_magnitude, 2),
                "rolling_mean": rolling_mean.tolist(),
                "rolling_std": rolling_std.tolist(),
                "overall_mean": float(self.df[col].mean()),
                "overall_std": float(self.df[col].std()),
                "min_value": float(self.df[col].min()),
                "max_value": float(self.df[col].max())
            }
        
        return trends

    def analyze_seasonality(self, metric_column: str) -> Dict[str, Any]:
        """
        Analyze seasonal patterns in data
        
        Args:
            metric_column: Column to analyze for seasonality
            
        Returns:
            Dictionary with seasonality analysis
        """
        if not self.date_column or metric_column not in self.df.columns:
            return {"error": "Invalid column"}
        
        seasonality = {}
        
        # Monthly patterns
        if 'month' in self.df.columns:
            monthly_avg = self.df.groupby('month')[metric_column].agg(['mean', 'std', 'count'])
            seasonality['monthly'] = {
                int(month): {
                    'mean': float(row['mean']),
                    'std': float(row['std']),
                    'count': int(row['count'])
                }
                for month, row in monthly_avg.iterrows()
            }
        
        # Day of week patterns
        if 'day_of_week' in self.df.columns:
            dow_avg = self.df.groupby('day_of_week')[metric_column].agg(['mean', 'std', 'count'])
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            seasonality['day_of_week'] = {
                day_names[int(dow)]: {
                    'mean': float(row['mean']),
                    'std': float(row['std']),
                    'count': int(row['count'])
                }
                for dow, row in dow_avg.iterrows()
            }
        
        return seasonality

    def analyze_team_performance(
        self,
        team_column: str,
        metric_columns: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze team performance over time
        
        Args:
            team_column: Column containing team names
            metric_columns: Metrics to analyze
            
        Returns:
            Dictionary with team performance analysis
        """
        if team_column not in self.df.columns:
            return {"error": "Team column not found"}
        
        team_performance = {}
        
        for team in self.df[team_column].unique():
            team_data = self.df[self.df[team_column] == team]
            
            team_stats = {
                'total_matches': len(team_data),
                'metrics': {}
            }
            
            for metric in metric_columns:
                if metric in team_data.columns and pd.api.types.is_numeric_dtype(team_data[metric]):
                    team_stats['metrics'][metric] = {
                        'mean': float(team_data[metric].mean()),
                        'median': float(team_data[metric].median()),
                        'std': float(team_data[metric].std()),
                        'min': float(team_data[metric].min()),
                        'max': float(team_data[metric].max()),
                        'trend': self._calculate_simple_trend(team_data[metric])
                    }
            
            team_performance[str(team)] = team_stats
        
        return team_performance

    def _calculate_simple_trend(self, series: pd.Series) -> str:
        """Calculate simple trend direction"""
        if len(series) < 2:
            return "insufficient_data"
        
        first_half = series.iloc[:len(series)//2].mean()
        second_half = series.iloc[len(series)//2:].mean()
        
        if second_half > first_half * 1.05:
            return "improving"
        elif second_half < first_half * 0.95:
            return "declining"
        else:
            return "stable"

    def detect_anomalies(
        self,
        metric_column: str,
        threshold: float = 3.0
    ) -> Dict[str, Any]:
        """
        Detect anomalies using statistical methods
        
        Args:
            metric_column: Column to analyze
            threshold: Number of standard deviations for anomaly detection
            
        Returns:
            Dictionary with anomaly information
        """
        if metric_column not in self.df.columns:
            return {"error": "Column not found"}
        
        data = self.df[metric_column].dropna()
        mean = data.mean()
        std = data.std()
        
        # Z-score method
        z_scores = np.abs((data - mean) / std)
        anomalies = self.df[z_scores > threshold].copy()
        
        return {
            "total_anomalies": len(anomalies),
            "anomaly_percentage": round(len(anomalies) / len(self.df) * 100, 2),
            "threshold_used": threshold,
            "anomaly_indices": anomalies.index.tolist(),
            "anomaly_values": anomalies[metric_column].tolist() if len(anomalies) > 0 else []
        }

    def calculate_moving_averages(
        self,
        metric_column: str,
        windows: List[int] = [3, 5, 10]
    ) -> Dict[str, List[float]]:
        """
        Calculate moving averages for different window sizes
        
        Args:
            metric_column: Column to analyze
            windows: List of window sizes
            
        Returns:
            Dictionary with moving averages
        """
        if metric_column not in self.df.columns:
            return {"error": "Column not found"}
        
        moving_averages = {}
        
        for window in windows:
            ma = self.df[metric_column].rolling(window=window, min_periods=1).mean()
            moving_averages[f"ma_{window}"] = ma.tolist()
        
        return moving_averages

    def analyze_streaks(
        self,
        result_column: str,
        positive_value: Any = 'W'
    ) -> Dict[str, Any]:
        """
        Analyze winning/losing streaks
        
        Args:
            result_column: Column containing results (W/L/D)
            positive_value: Value representing positive outcome
            
        Returns:
            Dictionary with streak analysis
        """
        if result_column not in self.df.columns:
            return {"error": "Column not found"}
        
        results = self.df[result_column].tolist()
        
        current_streak = 0
        max_positive_streak = 0
        max_negative_streak = 0
        streaks = []
        
        for result in results:
            if result == positive_value:
                if current_streak >= 0:
                    current_streak += 1
                else:
                    streaks.append(current_streak)
                    current_streak = 1
                max_positive_streak = max(max_positive_streak, current_streak)
            else:
                if current_streak <= 0:
                    current_streak -= 1
                else:
                    streaks.append(current_streak)
                    current_streak = -1
                max_negative_streak = min(max_negative_streak, current_streak)
        
        if current_streak != 0:
            streaks.append(current_streak)
        
        return {
            "current_streak": current_streak,
            "max_positive_streak": max_positive_streak,
            "max_negative_streak": abs(max_negative_streak),
            "all_streaks": streaks,
            "average_positive_streak": np.mean([s for s in streaks if s > 0]) if any(s > 0 for s in streaks) else 0,
            "average_negative_streak": abs(np.mean([s for s in streaks if s < 0])) if any(s < 0 for s in streaks) else 0
        }

    def compare_periods(
        self,
        metric_column: str,
        period1_start: str,
        period1_end: str,
        period2_start: str,
        period2_end: str
    ) -> Dict[str, Any]:
        """
        Compare metrics between two time periods
        
        Args:
            metric_column: Column to compare
            period1_start: Start date of first period
            period1_end: End date of first period
            period2_start: Start date of second period
            period2_end: End date of second period
            
        Returns:
            Dictionary with comparison results
        """
        if not self.date_column or metric_column not in self.df.columns:
            return {"error": "Invalid columns"}
        
        # Convert dates
        p1_start = pd.to_datetime(period1_start)
        p1_end = pd.to_datetime(period1_end)
        p2_start = pd.to_datetime(period2_start)
        p2_end = pd.to_datetime(period2_end)
        
        # Filter data
        period1_data = self.df[
            (self.df[self.date_column] >= p1_start) &
            (self.df[self.date_column] <= p1_end)
        ][metric_column]
        
        period2_data = self.df[
            (self.df[self.date_column] >= p2_start) &
            (self.df[self.date_column] <= p2_end)
        ][metric_column]
        
        # Calculate statistics
        comparison = {
            "period1": {
                "mean": float(period1_data.mean()),
                "median": float(period1_data.median()),
                "std": float(period1_data.std()),
                "count": len(period1_data)
            },
            "period2": {
                "mean": float(period2_data.mean()),
                "median": float(period2_data.median()),
                "std": float(period2_data.std()),
                "count": len(period2_data)
            }
        }
        
        # Calculate change
        if comparison["period1"]["mean"] != 0:
            change_percent = (
                (comparison["period2"]["mean"] - comparison["period1"]["mean"]) /
                comparison["period1"]["mean"] * 100
            )
            comparison["change_percent"] = round(change_percent, 2)
        
        return comparison

    def generate_summary(self) -> Dict[str, Any]:
        """
        Generate comprehensive time series summary
        
        Returns:
            Dictionary with summary statistics
        """
        summary = {
            "date_range": {
                "start": str(self.df[self.date_column].min()) if self.date_column else None,
                "end": str(self.df[self.date_column].max()) if self.date_column else None,
                "total_days": (self.df[self.date_column].max() - self.df[self.date_column].min()).days if self.date_column else None
            },
            "data_points": len(self.df),
            "numeric_columns": []
        }
        
        # Analyze numeric columns
        for col in self.df.select_dtypes(include=[np.number]).columns:
            if col not in ['year', 'month', 'day_of_week', 'week_of_year']:
                summary["numeric_columns"].append({
                    "name": col,
                    "mean": float(self.df[col].mean()),
                    "std": float(self.df[col].std()),
                    "min": float(self.df[col].min()),
                    "max": float(self.df[col].max())
                })
        
        return summary


# Example usage for soccer data
def analyze_soccer_season(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Comprehensive analysis of soccer season data
    
    Args:
        df: DataFrame with soccer match data
        
    Returns:
        Dictionary with analysis results
    """
    analyzer = TimeSeriesAnalyzer(df)
    
    results = {
        "summary": analyzer.generate_summary()
    }
    
    # Detect common soccer columns
    goal_columns = [col for col in df.columns if 'goal' in col.lower() or 'score' in col.lower()]
    if goal_columns:
        results["goal_trends"] = analyzer.analyze_trends(goal_columns)
    
    # Team analysis
    team_columns = [col for col in df.columns if 'team' in col.lower()]
    if team_columns and goal_columns:
        results["team_performance"] = analyzer.analyze_team_performance(
            team_columns[0],
            goal_columns
        )
    
    return results


if __name__ == "__main__":
    # Example usage
    sample_data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=100),
        'team': ['Team A', 'Team B'] * 50,
        'goals_scored': np.random.randint(0, 5, 100),
        'goals_conceded': np.random.randint(0, 4, 100)
    })
    
    analyzer = TimeSeriesAnalyzer(sample_data)
    trends = analyzer.analyze_trends(['goals_scored', 'goals_conceded'])
    print("Trends:", trends)

# Made with Bob
