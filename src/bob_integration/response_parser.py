"""
Response Parser for Bob Integration
Parses and validates responses from Bob AI assistant
"""

import re
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ParsedResponse:
    """Structured response from Bob"""
    success: bool
    response_type: str
    content: str
    code_blocks: List[Dict[str, str]]
    suggestions: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]
    raw_response: str


class ResponseParser:
    """
    Parser for Bob's responses
    Extracts code, suggestions, and structured information
    """

    def __init__(self):
        """Initialize response parser"""
        self.code_block_pattern = re.compile(
            r'```(\w+)?\n(.*?)```',
            re.DOTALL
        )
        self.json_pattern = re.compile(
            r'```json\n(.*?)```',
            re.DOTALL
        )
        self.python_pattern = re.compile(
            r'```python\n(.*?)```',
            re.DOTALL
        )

    def parse_response(self, response: str) -> ParsedResponse:
        """
        Parse Bob's response into structured format
        
        Args:
            response: Raw response text from Bob
            
        Returns:
            ParsedResponse object
        """
        try:
            # Extract code blocks
            code_blocks = self._extract_code_blocks(response)
            
            # Extract suggestions
            suggestions = self._extract_suggestions(response)
            
            # Extract warnings
            warnings = self._extract_warnings(response)
            
            # Determine response type
            response_type = self._determine_response_type(response, code_blocks)
            
            # Extract metadata
            metadata = self._extract_metadata(response)
            
            # Clean content (remove code blocks for main content)
            content = self._clean_content(response)
            
            return ParsedResponse(
                success=True,
                response_type=response_type,
                content=content,
                code_blocks=code_blocks,
                suggestions=suggestions,
                warnings=warnings,
                metadata=metadata,
                raw_response=response
            )
        
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            return ParsedResponse(
                success=False,
                response_type="error",
                content=response,
                code_blocks=[],
                suggestions=[],
                warnings=[f"Parse error: {str(e)}"],
                metadata={},
                raw_response=response
            )

    def _extract_code_blocks(self, response: str) -> List[Dict[str, str]]:
        """
        Extract all code blocks from response
        
        Args:
            response: Response text
            
        Returns:
            List of code blocks with language and content
        """
        code_blocks = []
        
        for match in self.code_block_pattern.finditer(response):
            language = match.group(1) or 'text'
            code = match.group(2).strip()
            
            code_blocks.append({
                'language': language,
                'code': code,
                'start_pos': match.start(),
                'end_pos': match.end()
            })
        
        return code_blocks

    def _extract_suggestions(self, response: str) -> List[str]:
        """
        Extract suggestions from response
        
        Args:
            response: Response text
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        # Look for common suggestion patterns
        patterns = [
            r'(?:I suggest|I recommend|Consider|You should|You could)\s+(.+?)(?:\.|$)',
            r'(?:Suggestion|Recommendation):\s*(.+?)(?:\n|$)',
            r'(?:💡|🔍|✨)\s*(.+?)(?:\n|$)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, response, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                suggestion = match.group(1).strip()
                if suggestion and len(suggestion) > 10:
                    suggestions.append(suggestion)
        
        return list(set(suggestions))  # Remove duplicates

    def _extract_warnings(self, response: str) -> List[str]:
        """
        Extract warnings from response
        
        Args:
            response: Response text
            
        Returns:
            List of warnings
        """
        warnings = []
        
        # Look for warning patterns
        patterns = [
            r'(?:Warning|Caution|Note|Important):\s*(.+?)(?:\n|$)',
            r'(?:⚠️|❗|🚨)\s*(.+?)(?:\n|$)',
            r'(?:Be careful|Watch out|Pay attention)\s+(.+?)(?:\.|$)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, response, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                warning = match.group(1).strip()
                if warning and len(warning) > 10:
                    warnings.append(warning)
        
        return list(set(warnings))

    def _determine_response_type(
        self,
        response: str,
        code_blocks: List[Dict[str, str]]
    ) -> str:
        """
        Determine the type of response
        
        Args:
            response: Response text
            code_blocks: Extracted code blocks
            
        Returns:
            Response type string
        """
        response_lower = response.lower()
        
        # Check for specific response types
        if any(lang in ['python', 'py'] for block in code_blocks for lang in [block['language']]):
            return 'code_generation'
        
        if 'strategy' in response_lower or 'approach' in response_lower:
            return 'strategy'
        
        if 'analysis' in response_lower or 'insight' in response_lower:
            return 'analysis'
        
        if 'error' in response_lower or 'issue' in response_lower:
            return 'error_report'
        
        if 'recommendation' in response_lower or 'suggest' in response_lower:
            return 'recommendation'
        
        if any(lang == 'json' for block in code_blocks for lang in [block['language']]):
            return 'configuration'
        
        return 'general'

    def _extract_metadata(self, response: str) -> Dict[str, Any]:
        """
        Extract metadata from response
        
        Args:
            response: Response text
            
        Returns:
            Metadata dictionary
        """
        metadata = {}
        
        # Extract JSON blocks as metadata
        json_matches = self.json_pattern.finditer(response)
        for match in json_matches:
            try:
                json_data = json.loads(match.group(1))
                metadata['json_data'] = json_data
            except json.JSONDecodeError:
                pass
        
        # Extract key-value pairs
        kv_pattern = r'(\w+):\s*([^\n]+)'
        for match in re.finditer(kv_pattern, response):
            key = match.group(1).lower()
            value = match.group(2).strip()
            
            # Only add if it looks like metadata
            if key in ['priority', 'complexity', 'confidence', 'status', 'type']:
                metadata[key] = value
        
        return metadata

    def _clean_content(self, response: str) -> str:
        """
        Clean response content by removing code blocks
        
        Args:
            response: Response text
            
        Returns:
            Cleaned content
        """
        # Remove code blocks
        content = self.code_block_pattern.sub('', response)
        
        # Remove excessive whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = content.strip()
        
        return content

    def extract_python_code(self, response: str) -> List[str]:
        """
        Extract only Python code blocks
        
        Args:
            response: Response text
            
        Returns:
            List of Python code strings
        """
        python_code = []
        
        for match in self.python_pattern.finditer(response):
            code = match.group(1).strip()
            python_code.append(code)
        
        return python_code

    def extract_json_data(self, response: str) -> List[Dict[str, Any]]:
        """
        Extract and parse JSON blocks
        
        Args:
            response: Response text
            
        Returns:
            List of parsed JSON objects
        """
        json_data = []
        
        for match in self.json_pattern.finditer(response):
            try:
                data = json.loads(match.group(1))
                json_data.append(data)
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON: {e}")
        
        return json_data

    def validate_code_syntax(self, code: str, language: str = 'python') -> Tuple[bool, Optional[str]]:
        """
        Validate syntax of code block
        
        Args:
            code: Code to validate
            language: Programming language
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if language.lower() in ['python', 'py']:
            try:
                compile(code, '<string>', 'exec')
                return True, None
            except SyntaxError as e:
                return False, f"Syntax error at line {e.lineno}: {e.msg}"
        
        elif language.lower() == 'json':
            try:
                json.loads(code)
                return True, None
            except json.JSONDecodeError as e:
                return False, f"JSON error: {e.msg}"
        
        # For other languages, just check if not empty
        return len(code.strip()) > 0, None

    def extract_function_definitions(self, code: str) -> List[Dict[str, Any]]:
        """
        Extract function definitions from Python code
        
        Args:
            code: Python code
            
        Returns:
            List of function information
        """
        functions = []
        
        # Pattern for function definitions
        func_pattern = re.compile(
            r'def\s+(\w+)\s*\((.*?)\)\s*(?:->\s*(.+?))?\s*:',
            re.MULTILINE
        )
        
        for match in func_pattern.finditer(code):
            func_name = match.group(1)
            params = match.group(2).strip()
            return_type = match.group(3).strip() if match.group(3) else None
            
            # Extract docstring
            docstring = None
            start_pos = match.end()
            remaining_code = code[start_pos:]
            docstring_match = re.match(r'\s*"""(.*?)"""', remaining_code, re.DOTALL)
            if docstring_match:
                docstring = docstring_match.group(1).strip()
            
            functions.append({
                'name': func_name,
                'parameters': params,
                'return_type': return_type,
                'docstring': docstring,
                'start_pos': match.start()
            })
        
        return functions

    def extract_class_definitions(self, code: str) -> List[Dict[str, Any]]:
        """
        Extract class definitions from Python code
        
        Args:
            code: Python code
            
        Returns:
            List of class information
        """
        classes = []
        
        # Pattern for class definitions
        class_pattern = re.compile(
            r'class\s+(\w+)(?:\((.*?)\))?\s*:',
            re.MULTILINE
        )
        
        for match in class_pattern.finditer(code):
            class_name = match.group(1)
            base_classes = match.group(2).strip() if match.group(2) else None
            
            # Extract docstring
            docstring = None
            start_pos = match.end()
            remaining_code = code[start_pos:]
            docstring_match = re.match(r'\s*"""(.*?)"""', remaining_code, re.DOTALL)
            if docstring_match:
                docstring = docstring_match.group(1).strip()
            
            classes.append({
                'name': class_name,
                'base_classes': base_classes,
                'docstring': docstring,
                'start_pos': match.start()
            })
        
        return classes

    def format_response_summary(self, parsed: ParsedResponse) -> str:
        """
        Format a summary of parsed response
        
        Args:
            parsed: ParsedResponse object
            
        Returns:
            Formatted summary string
        """
        summary = []
        summary.append(f"Response Type: {parsed.response_type}")
        summary.append(f"Code Blocks: {len(parsed.code_blocks)}")
        
        if parsed.code_blocks:
            languages = [block['language'] for block in parsed.code_blocks]
            summary.append(f"Languages: {', '.join(set(languages))}")
        
        if parsed.suggestions:
            summary.append(f"Suggestions: {len(parsed.suggestions)}")
        
        if parsed.warnings:
            summary.append(f"Warnings: {len(parsed.warnings)}")
        
        if parsed.metadata:
            summary.append(f"Metadata: {', '.join(parsed.metadata.keys())}")
        
        return '\n'.join(summary)


# Example usage
def example_usage():
    """Example of using ResponseParser"""
    
    parser = ResponseParser()
    
    # Example Bob response
    response = """
    Here's a solution for data cleaning:
    
    I suggest using the following approach for handling missing values.
    
    ```python
    def clean_missing_values(df, strategy='mean'):
        \"\"\"Clean missing values in dataframe\"\"\"
        if strategy == 'mean':
            return df.fillna(df.mean())
        elif strategy == 'median':
            return df.fillna(df.median())
        return df.dropna()
    ```
    
    ⚠️ Warning: This approach may not work well with categorical data.
    
    Configuration:
    ```json
    {
        "strategy": "mean",
        "threshold": 0.5
    }
    ```
    """
    
    parsed = parser.parse_response(response)
    
    print("Parsed Response:")
    print(parser.format_response_summary(parsed))
    print("\nCode Blocks:")
    for block in parsed.code_blocks:
        print(f"  Language: {block['language']}")
        print(f"  Lines: {len(block['code'].split(chr(10)))}")
    
    print("\nSuggestions:")
    for suggestion in parsed.suggestions:
        print(f"  - {suggestion}")
    
    print("\nWarnings:")
    for warning in parsed.warnings:
        print(f"  - {warning}")


if __name__ == "__main__":
    example_usage()

# Made with Bob
