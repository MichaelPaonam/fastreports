"""
Bob Integration - Prompt Templates
Reusable prompt templates for IBM Bob interactions
"""

from typing import Dict, List, Any, Optional


class BobPromptTemplates:
    """Collection of prompt templates for IBM Bob."""
    
    @staticmethod
    def data_profiling_prompt(
        dataset_name: str,
        data_sample: str,
        column_info: Dict[str, Any]
    ) -> str:
        """
        Generate prompt for data profiling analysis.
        
        Args:
            dataset_name: Name of the dataset
            data_sample: Sample of the data
            column_info: Information about columns
        
        Returns:
            Formatted prompt string
        """
        return f"""Analyze this dataset and provide insights:

Dataset: {dataset_name}

Column Information:
{column_info}

Data Sample:
{data_sample}

Please identify:
1. Data quality issues (missing values, outliers, inconsistencies)
2. Column types and their appropriateness
3. Potential relationships between variables
4. Recommended data cleaning strategies
5. Any anomalies or patterns worth investigating

Provide a structured analysis with actionable recommendations."""
    
    @staticmethod
    def cleaning_strategy_prompt(
        dataset_name: str,
        quality_issues: List[Dict[str, Any]],
        column_types: Dict[str, str]
    ) -> str:
        """
        Generate prompt for cleaning strategy generation.
        
        Args:
            dataset_name: Name of the dataset
            quality_issues: List of identified quality issues
            column_types: Dictionary of column names to types
        
        Returns:
            Formatted prompt string
        """
        issues_text = "\n".join([
            f"- {issue.get('type', 'Unknown')}: {issue.get('description', '')}"
            for issue in quality_issues
        ])
        
        return f"""Generate Python code to clean this dataset:

Dataset: {dataset_name}

Quality Issues Identified:
{issues_text}

Column Types:
{column_types}

Requirements:
- Use pandas for all transformations
- Preserve original data structure where possible
- Log all changes made
- Handle edge cases gracefully
- Include comments explaining each transformation
- Return the cleaned dataframe

Generate complete, executable Python code for data cleaning."""
    
    @staticmethod
    def visualization_code_prompt(
        dataset_name: str,
        chart_type: str,
        columns: List[str],
        data_characteristics: Dict[str, Any]
    ) -> str:
        """
        Generate prompt for visualization code generation.
        
        Args:
            dataset_name: Name of the dataset
            chart_type: Type of chart to generate
            columns: Columns to visualize
            data_characteristics: Characteristics of the data
        
        Returns:
            Formatted prompt string
        """
        return f"""Generate Plotly visualization code:

Dataset: {dataset_name}
Chart Type: {chart_type}
Columns: {', '.join(columns)}

Data Characteristics:
{data_characteristics}

Requirements:
- Use Plotly for interactive visualizations
- Make the chart publication-ready
- Include appropriate titles, labels, and legends
- Use a professional color scheme
- Add hover information for interactivity
- Ensure the chart is responsive

Generate complete Python code using plotly.graph_objects or plotly.express."""
    
    @staticmethod
    def statistical_analysis_prompt(
        dataset_name: str,
        analysis_type: str,
        columns: List[str],
        context: Optional[str] = None
    ) -> str:
        """
        Generate prompt for statistical analysis.
        
        Args:
            dataset_name: Name of the dataset
            analysis_type: Type of analysis to perform
            columns: Columns to analyze
            context: Optional context information
        
        Returns:
            Formatted prompt string
        """
        context_text = f"\n\nContext: {context}" if context else ""
        
        return f"""Perform statistical analysis on this dataset:

Dataset: {dataset_name}
Analysis Type: {analysis_type}
Columns: {', '.join(columns)}{context_text}

Please provide:
1. Appropriate statistical tests
2. Interpretation of results
3. Significance levels and p-values
4. Practical implications
5. Recommendations for further analysis

Generate Python code using scipy.stats, pandas, and numpy as needed."""
    
    @staticmethod
    def insight_generation_prompt(
        dataset_name: str,
        statistics: Dict[str, Any],
        correlations: Dict[str, Any],
        quality_score: float
    ) -> str:
        """
        Generate prompt for insight generation.
        
        Args:
            dataset_name: Name of the dataset
            statistics: Statistical summary
            correlations: Correlation analysis results
            quality_score: Data quality score
        
        Returns:
            Formatted prompt string
        """
        return f"""Generate insights from this data analysis:

Dataset: {dataset_name}
Data Quality Score: {quality_score}/100

Statistical Summary:
{statistics}

Correlation Analysis:
{correlations}

Please provide:
1. Key findings and patterns
2. Interesting relationships discovered
3. Potential business implications
4. Recommendations for stakeholders
5. Areas requiring further investigation

Format the insights in a clear, business-friendly manner."""
    
    @staticmethod
    def report_generation_prompt(
        dataset_name: str,
        analysis_results: Dict[str, Any],
        target_audience: str = "data analysts"
    ) -> str:
        """
        Generate prompt for report generation.
        
        Args:
            dataset_name: Name of the dataset
            analysis_results: Complete analysis results
            target_audience: Target audience for the report
        
        Returns:
            Formatted prompt string
        """
        return f"""Generate a comprehensive data analysis report:

Dataset: {dataset_name}
Target Audience: {target_audience}

Analysis Results:
{analysis_results}

Report Requirements:
1. Executive Summary (2-3 paragraphs)
2. Data Overview and Quality Assessment
3. Key Findings with supporting evidence
4. Visualizations and their interpretations
5. Recommendations and Next Steps
6. Technical Appendix (methodology)

Format: Professional HTML report with embedded visualizations
Style: Clear, concise, and actionable

Generate the complete HTML report with inline CSS styling."""
    
    @staticmethod
    def code_review_prompt(
        code: str,
        purpose: str
    ) -> str:
        """
        Generate prompt for code review.
        
        Args:
            code: Code to review
            purpose: Purpose of the code
        
        Returns:
            Formatted prompt string
        """
        return f"""Review this Python code:

Purpose: {purpose}

Code:
```python
{code}
```

Please review for:
1. Correctness and logic errors
2. Performance optimization opportunities
3. Code style and best practices
4. Error handling
5. Documentation quality
6. Potential edge cases

Provide specific suggestions for improvement."""
    
    @staticmethod
    def data_transformation_prompt(
        transformation_type: str,
        column_name: str,
        current_state: str,
        desired_state: str
    ) -> str:
        """
        Generate prompt for data transformation.
        
        Args:
            transformation_type: Type of transformation
            column_name: Column to transform
            current_state: Current state description
            desired_state: Desired state description
        
        Returns:
            Formatted prompt string
        """
        return f"""Generate code for data transformation:

Transformation Type: {transformation_type}
Column: {column_name}

Current State:
{current_state}

Desired State:
{desired_state}

Requirements:
- Use pandas operations
- Handle missing values appropriately
- Preserve data integrity
- Include validation checks
- Add informative logging

Generate the transformation code with error handling."""
    
    @staticmethod
    def exploratory_question_prompt(
        dataset_name: str,
        question: str,
        available_columns: List[str]
    ) -> str:
        """
        Generate prompt for exploratory data questions.
        
        Args:
            dataset_name: Name of the dataset
            question: Question to answer
            available_columns: Available columns in dataset
        
        Returns:
            Formatted prompt string
        """
        return f"""Answer this exploratory data question:

Dataset: {dataset_name}
Question: {question}

Available Columns:
{', '.join(available_columns)}

Please provide:
1. Approach to answer the question
2. Python code to perform the analysis
3. Expected output format
4. Interpretation guidelines
5. Potential limitations

Generate executable code with clear explanations."""
    
    @staticmethod
    def optimization_prompt(
        current_code: str,
        performance_issue: str
    ) -> str:
        """
        Generate prompt for code optimization.
        
        Args:
            current_code: Current code to optimize
            performance_issue: Description of performance issue
        
        Returns:
            Formatted prompt string
        """
        return f"""Optimize this code for better performance:

Performance Issue:
{performance_issue}

Current Code:
```python
{current_code}
```

Please provide:
1. Identified bottlenecks
2. Optimized version of the code
3. Expected performance improvement
4. Trade-offs (if any)
5. Alternative approaches

Focus on pandas/numpy optimization techniques."""
    
    @staticmethod
    def documentation_prompt(
        code: str,
        module_name: str
    ) -> str:
        """
        Generate prompt for documentation generation.
        
        Args:
            code: Code to document
            module_name: Name of the module
        
        Returns:
            Formatted prompt string
        """
        return f"""Generate comprehensive documentation:

Module: {module_name}

Code:
```python
{code}
```

Please provide:
1. Module-level docstring
2. Function/class docstrings (Google style)
3. Usage examples
4. Parameter descriptions
5. Return value descriptions
6. Exception documentation

Follow Python documentation best practices."""
    
    @staticmethod
    def get_prompt_for_phase(
        phase: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Get appropriate prompt for a pipeline phase.
        
        Args:
            phase: Pipeline phase name
            context: Context information for the phase
        
        Returns:
            Formatted prompt string
        """
        prompt_map = {
            'profiling': lambda ctx: BobPromptTemplates.data_profiling_prompt(
                ctx.get('dataset_name', ''),
                ctx.get('data_sample', ''),
                ctx.get('column_info', {})
            ),
            'cleaning': lambda ctx: BobPromptTemplates.cleaning_strategy_prompt(
                ctx.get('dataset_name', ''),
                ctx.get('quality_issues', []),
                ctx.get('column_types', {})
            ),
            'visualization': lambda ctx: BobPromptTemplates.visualization_code_prompt(
                ctx.get('dataset_name', ''),
                ctx.get('chart_type', ''),
                ctx.get('columns', []),
                ctx.get('data_characteristics', {})
            ),
            'analysis': lambda ctx: BobPromptTemplates.statistical_analysis_prompt(
                ctx.get('dataset_name', ''),
                ctx.get('analysis_type', ''),
                ctx.get('columns', []),
                ctx.get('context')
            )
        }
        
        if phase in prompt_map:
            return prompt_map[phase](context)
        else:
            return f"Perform {phase} on the dataset with context: {context}"


# Made with Bob