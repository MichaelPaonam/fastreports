"""
Test script for HTML Report Generator and Transaction Analyzer
Tests both components with real data
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.reporting.html_generator import HTMLReportGenerator
from src.analysis.transaction_analyzer import TransactionAnalyzer
from src.profiling.profiler import DataProfiler
from src.visualization.plotly_charts import PlotlyChartBuilder
import plotly.graph_objects as go


def test_html_report_generator():
    """Test HTML Report Generator with sample data."""
    print("\n" + "="*80)
    print("Testing HTML Report Generator")
    print("="*80)
    
    # Create sample data
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'id': range(1, 101),
        'name': [f'User{i}' for i in range(1, 101)],
        'age': np.random.randint(18, 80, 100),
        'score': np.random.normal(75, 15, 100),
        'category': np.random.choice(['A', 'B', 'C'], 100),
        'active': np.random.choice([True, False], 100).astype(str),
        'revenue': np.random.uniform(100, 1000, 100)
    })
    
    # Add some missing values
    sample_data.loc[5:10, 'age'] = np.nan
    sample_data.loc[15:20, 'score'] = np.nan
    
    print(f"✓ Created sample dataset: {len(sample_data)} rows, {len(sample_data.columns)} columns")
    
    # Profile the data
    profiler = DataProfiler()
    profile = profiler.profile_dataframe(sample_data, "Sample Dataset")
    print(f"✓ Generated data profile")
    
    # Create some sample charts
    chart_builder = PlotlyChartBuilder()
    
    # Histogram
    fig1 = go.Figure()
    fig1.add_trace(go.Histogram(x=sample_data['age'].dropna(), nbinsx=20))
    fig1.update_layout(title="Age Distribution", xaxis_title="Age", yaxis_title="Count")
    
    # Bar chart
    fig2 = go.Figure()
    category_counts = sample_data['category'].value_counts()
    fig2.add_trace(go.Bar(x=category_counts.index, y=category_counts.values))
    fig2.update_layout(title="Category Distribution", xaxis_title="Category", yaxis_title="Count")
    
    # Scatter plot
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=sample_data['age'].dropna(),
        y=sample_data['score'].dropna(),
        mode='markers'
    ))
    fig3.update_layout(title="Age vs Score", xaxis_title="Age", yaxis_title="Score")
    
    charts = [fig1, fig2, fig3]
    print(f"✓ Created {len(charts)} sample charts")
    
    # Generate HTML report
    generator = HTMLReportGenerator()
    output_path = "output/test_report.html"
    
    analysis_results = {
        "statistical_summary": {
            "mean_age": float(sample_data['age'].mean()),
            "mean_score": float(sample_data['score'].mean()),
            "total_revenue": float(sample_data['revenue'].sum())
        }
    }
    
    report_path = generator.generate_report(
        profile=profile,
        charts=charts,
        analysis_results=analysis_results,
        output_path=output_path
    )
    
    print(f"✓ HTML report generated: {report_path}")
    print(f"✓ Report size: {Path(report_path).stat().st_size / 1024:.2f} KB")
    
    return True


def test_transaction_analyzer_with_sample_data():
    """Test Transaction Analyzer with sample transaction data."""
    print("\n" + "="*80)
    print("Testing Transaction Analyzer (Sample Data)")
    print("="*80)
    
    # Create sample transaction data
    np.random.seed(42)
    n_transactions = 500
    
    sample_transactions = pd.DataFrame({
        'transaction_id': range(1, n_transactions + 1),
        'customer_id': np.random.randint(1, 51, n_transactions),
        'product': np.random.choice(['Pizza Margherita', 'Pizza Pepperoni', 'Pizza Veggie', 
                                     'Burger', 'Salad', 'Drink'], n_transactions),
        'amount': np.random.uniform(5, 50, n_transactions),
        'date': pd.date_range('2024-01-01', periods=n_transactions, freq='h')
    })
    
    print(f"✓ Created sample transaction data: {len(sample_transactions)} transactions")
    print(f"  - Customers: {sample_transactions['customer_id'].nunique()}")
    print(f"  - Products: {sample_transactions['product'].nunique()}")
    print(f"  - Date range: {sample_transactions['date'].min()} to {sample_transactions['date'].max()}")
    
    # Initialize analyzer
    analyzer = TransactionAnalyzer(sample_transactions)
    print(f"✓ Initialized TransactionAnalyzer")
    print(f"  - Detected customer column: {analyzer.customer_col}")
    print(f"  - Detected amount column: {analyzer.amount_col}")
    print(f"  - Detected date column: {analyzer.date_col}")
    print(f"  - Detected product column: {analyzer.product_col}")
    
    # Test revenue analysis
    print("\n--- Revenue Analysis ---")
    revenue_analysis = analyzer.analyze_revenue()
    print(f"✓ Total Revenue: ${revenue_analysis['total_revenue']:,.2f}")
    print(f"✓ Average Transaction: ${revenue_analysis['average_transaction']:.2f}")
    print(f"✓ Total Transactions: {revenue_analysis['total_transactions']}")
    print(f"✓ Top 20% Revenue Share: {revenue_analysis['revenue_concentration']['top_20_percent_share']:.1f}%")
    
    # Test customer behavior analysis
    print("\n--- Customer Behavior Analysis ---")
    customer_behavior = analyzer.analyze_customer_behavior()
    print(f"✓ Total Customers: {customer_behavior['total_customers']}")
    print(f"✓ Avg Transactions per Customer: {customer_behavior['avg_transactions_per_customer']:.2f}")
    print(f"✓ One-time Buyers: {customer_behavior['customer_distribution']['one_time_buyers']}")
    print(f"✓ Repeat Customers: {customer_behavior['customer_distribution']['repeat_customers']}")
    print(f"✓ Loyal Customers (5+ purchases): {customer_behavior['customer_distribution']['loyal_customers']}")
    
    # Test purchase patterns
    print("\n--- Purchase Patterns ---")
    purchase_patterns = analyzer.analyze_purchase_patterns()
    if 'daily_patterns' in purchase_patterns:
        print(f"✓ Busiest Day: {purchase_patterns['daily_patterns']['busiest_day']}")
    if 'hourly_patterns' in purchase_patterns:
        print(f"✓ Peak Hour: {purchase_patterns['hourly_patterns']['peak_hour']}:00")
    
    # Test product performance
    print("\n--- Product Performance ---")
    product_performance = analyzer.analyze_product_performance()
    print(f"✓ Total Products: {product_performance['total_products']}")
    print(f"✓ Top 3 Products:")
    for i, (product, stats) in enumerate(list(product_performance['top_10_products'].items())[:3], 1):
        print(f"  {i}. {product}: {stats['purchase_count']} purchases, ${stats['total_revenue']:.2f} revenue")
    
    # Test customer lifetime value
    print("\n--- Customer Lifetime Value ---")
    clv_analysis = analyzer.calculate_customer_lifetime_value()
    print(f"✓ Average CLV: ${clv_analysis['average_clv']:.2f}")
    print(f"✓ Median CLV: ${clv_analysis['median_clv']:.2f}")
    print(f"✓ Top 10% CLV: ${clv_analysis['top_10_percent_clv']:.2f}")
    
    # Test churn risk
    print("\n--- Churn Risk Analysis ---")
    churn_risk = analyzer.detect_churn_risk(inactive_days=30)
    print(f"✓ Active Customers: {churn_risk['active_customers']}")
    print(f"✓ At-Risk Customers: {churn_risk['at_risk_customers']}")
    print(f"✓ Churn Risk: {churn_risk['churn_risk_percentage']:.1f}%")
    
    # Generate comprehensive summary
    print("\n--- Generating Comprehensive Summary ---")
    summary = analyzer.generate_summary()
    print(f"✓ Summary generated with {len(summary)} sections")
    
    return True


def test_transaction_analyzer_with_pizza_data():
    """Test Transaction Analyzer with actual pizza delivery data."""
    print("\n" + "="*80)
    print("Testing Transaction Analyzer (Pizza Delivery Data)")
    print("="*80)
    
    pizza_data_path = Path("data/pizza_delivery_app/purchase_log.xlsx")
    
    if not pizza_data_path.exists():
        print(f"⚠ Pizza delivery data not found at {pizza_data_path}")
        print("  Skipping pizza data test")
        return False
    
    try:
        # Load pizza delivery data
        df = pd.read_excel(pizza_data_path)
        print(f"✓ Loaded pizza delivery data: {len(df)} rows, {len(df.columns)} columns")
        print(f"  Columns: {', '.join(df.columns.tolist())}")
        
        # Initialize analyzer
        analyzer = TransactionAnalyzer(df)
        print(f"✓ Initialized TransactionAnalyzer")
        print(f"  - Detected customer column: {analyzer.customer_col}")
        print(f"  - Detected amount column: {analyzer.amount_col}")
        print(f"  - Detected date column: {analyzer.date_col}")
        print(f"  - Detected product column: {analyzer.product_col}")
        
        # Generate comprehensive analysis
        print("\n--- Generating Pizza Delivery Analysis ---")
        summary = analyzer.generate_summary()
        
        # Display key metrics
        if 'revenue_analysis' in summary:
            rev = summary['revenue_analysis']
            print(f"\n📊 Revenue Metrics:")
            print(f"  Total Revenue: ${rev['total_revenue']:,.2f}")
            print(f"  Average Order: ${rev['average_transaction']:.2f}")
            print(f"  Total Orders: {rev['total_transactions']}")
        
        if 'customer_behavior' in summary:
            cust = summary['customer_behavior']
            print(f"\n👥 Customer Metrics:")
            print(f"  Total Customers: {cust['total_customers']}")
            print(f"  Repeat Customers: {cust['customer_distribution']['repeat_customers']}")
            print(f"  Loyal Customers: {cust['customer_distribution']['loyal_customers']}")
        
        if 'product_performance' in summary:
            prod = summary['product_performance']
            print(f"\n🍕 Product Metrics:")
            print(f"  Total Products: {prod['total_products']}")
            print(f"  Top Products: {len(prod['top_10_products'])}")
        
        # Save analysis to file
        import json
        output_path = Path("output/pizza_delivery_analysis.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        print(f"\n✓ Analysis saved to: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error analyzing pizza data: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("TESTING NEW COMPONENTS")
    print("="*80)
    
    results = {}
    
    # Test HTML Report Generator
    try:
        results['html_generator'] = test_html_report_generator()
    except Exception as e:
        print(f"\n✗ HTML Report Generator test failed: {e}")
        import traceback
        traceback.print_exc()
        results['html_generator'] = False
    
    # Test Transaction Analyzer with sample data
    try:
        results['transaction_analyzer_sample'] = test_transaction_analyzer_with_sample_data()
    except Exception as e:
        print(f"\n✗ Transaction Analyzer (sample) test failed: {e}")
        import traceback
        traceback.print_exc()
        results['transaction_analyzer_sample'] = False
    
    # Test Transaction Analyzer with pizza data
    try:
        results['transaction_analyzer_pizza'] = test_transaction_analyzer_with_pizza_data()
    except Exception as e:
        print(f"\n✗ Transaction Analyzer (pizza) test failed: {e}")
        import traceback
        traceback.print_exc()
        results['transaction_analyzer_pizza'] = False
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠ {total_tests - passed_tests} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
