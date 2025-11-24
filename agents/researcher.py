"""
Researcher Agent - Searches for solutions to errors using web search.
Called on Strike-3 when debugging has failed 3 times.
Uses MCP fetch server when available, falls back to generic advice.
"""

import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger('MultiAgentBuilder')


class Researcher:
    """
    Agent responsible for researching error solutions via web search.
    Called when traditional debugging fails (Strike-3 system).
    """
    
    def __init__(self, mcp_client=None):
        """
        Initialize Researcher.
        
        Args:
            mcp_client: Optional MCP client for fetch operations
        """
        self.mcp = mcp_client
        
    def run(self, task: str, project_path: str, context: dict) -> Dict[str, Any]:
        """
        Research solutions for an error.
        
        Args:
            task: Task description (e.g., "Research solution for: ModuleNotFoundError")
            project_path: Path to the project directory
            context: Project context including last_error, language_config, etc.
            
        Returns:
            dict: {"success": bool, "output": {"solutions": [...], "summary": str}, "error": str/None}
        """
        try:
            logger.info(f"Researcher starting: {task}")
            
            # Extract error from context
            error_message = context.get('last_error', '')
            language_config = context.get('language_config', {})
            
            if not error_message:
                return {
                    "success": False,
                    "output": {},
                    "error": "No error message provided to research"
                }
            
            logger.info(f"Researching solution for error: {error_message[:100]}...")
            
            # Try web search via MCP fetch
            if self.mcp and self.mcp.is_available('fetch'):
                solutions = self._search_via_mcp(error_message, language_config)
            else:
                # Fallback to pattern-based generic advice
                solutions = self._generic_solutions(error_message, language_config)
            
            # Format summary
            summary = self._format_summary(error_message, solutions)
            
            return {
                "success": True,
                "output": {
                    "solutions": solutions,
                    "summary": summary,
                    "error_analyzed": error_message
                },
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Researcher error: {e}")
            return {
                "success": False,
                "output": {},
                "error": str(e)
            }
    
    def _search_via_mcp(self, error_message: str, language_config: dict) -> list:
        """
        Search for solutions using MCP fetch server.
        
        Args:
            error_message: The error to research
            language_config: Language configuration
            
        Returns:
            list: List of solution dictionaries
        """
        logger.info("Using MCP fetch for web search")
        
        # Placeholder for actual MCP fetch implementation
        # In production, this would:
        # 1. Search StackOverflow API
        # 2. Search official docs
        # 3. Search GitHub issues
        
        # For now, return structure that would come from MCP
        return self._generic_solutions(error_message, language_config)
    
    def _generic_solutions(self, error_message: str, language_config: dict) -> list:
        """
        Provide generic solutions based on error patterns.
        
        Args:
            error_message: The error to analyze
            language_config: Language configuration
            
        Returns:
            list: List of solution dictionaries
        """
        logger.info("Using pattern-based generic solutions (MCP unavailable)")
        
        solutions = []
        error_lower = error_message.lower()
        
        # Get language context
        backend_lang = language_config.get('backend', {}).get('language', 'python').lower()
        framework = language_config.get('backend', {}).get('framework', '').lower()
        
        # Python-specific errors
        if 'modulenotfounderror' in error_lower or 'no module named' in error_lower:
            module_name = self._extract_module_name(error_message)
            solutions.append({
                "type": "dependency",
                "title": f"Install missing module: {module_name}",
                "steps": [
                    f"Run: pip install {module_name}",
                    "Add to requirements.txt",
                    "Verify import after installation"
                ],
                "confidence": "high"
            })
        
        # Import errors
        elif 'importerror' in error_lower or 'cannot import' in error_lower:
            solutions.append({
                "type": "import",
                "title": "Fix import statement",
                "steps": [
                    "Check module name spelling",
                    "Verify module is installed",
                    "Check Python path and virtual environment",
                    "Try: from package import module"
                ],
                "confidence": "medium"
            })
        
        # Syntax errors
        elif 'syntaxerror' in error_lower:
            solutions.append({
                "type": "syntax",
                "title": "Fix syntax error",
                "steps": [
                    "Check for missing colons, parentheses, or brackets",
                    "Verify indentation is consistent",
                    "Look for unclosed strings or comments",
                    "Check for invalid characters"
                ],
                "confidence": "high"
            })
        
        # Indentation errors
        elif 'indentationerror' in error_lower:
            solutions.append({
                "type": "indentation",
                "title": "Fix indentation",
                "steps": [
                    "Use consistent indentation (4 spaces recommended)",
                    "Don't mix tabs and spaces",
                    "Check alignment in function definitions",
                    "Verify block structure"
                ],
                "confidence": "high"
            })
        
        # Name errors
        elif 'nameerror' in error_lower:
            var_name = self._extract_variable_name(error_message)
            solutions.append({
                "type": "undefined",
                "title": f"Define variable: {var_name}",
                "steps": [
                    f"Initialize {var_name} before use",
                    "Check for typos in variable name",
                    "Verify variable scope",
                    "Import if it's from a module"
                ],
                "confidence": "high"
            })
        
        # Type errors
        elif 'typeerror' in error_lower:
            solutions.append({
                "type": "type",
                "title": "Fix type mismatch",
                "steps": [
                    "Check argument types match function signature",
                    "Convert types explicitly if needed",
                    "Verify number of arguments",
                    "Check for None values"
                ],
                "confidence": "medium"
            })
        
        # Attribute errors
        elif 'attributeerror' in error_lower:
            solutions.append({
                "type": "attribute",
                "title": "Fix missing attribute",
                "steps": [
                    "Check spelling of attribute/method name",
                    "Verify object type is correct",
                    "Check documentation for correct API",
                    "Initialize object before use"
                ],
                "confidence": "medium"
            })
        
        # Connection/Network errors
        elif 'connectionrefusederror' in error_lower or 'connection refused' in error_lower:
            solutions.append({
                "type": "connection",
                "title": "Fix connection issue",
                "steps": [
                    "Start the server/service",
                    "Check if port is correct",
                    "Verify firewall settings",
                    "Check if service is listening on correct interface"
                ],
                "confidence": "high"
            })
        
        # Port in use
        elif 'address already in use' in error_lower or 'port' in error_lower:
            solutions.append({
                "type": "port",
                "title": "Port already in use",
                "steps": [
                    "Kill process using the port",
                    "Use a different port number",
                    "Check for zombie processes",
                    f"For {backend_lang}: change port in config"
                ],
                "confidence": "high"
            })
        
        # File not found
        elif 'filenotfounderror' in error_lower or 'no such file' in error_lower:
            solutions.append({
                "type": "file",
                "title": "File not found",
                "steps": [
                    "Check file path is correct",
                    "Use absolute paths or os.path.join()",
                    "Verify file exists in expected location",
                    "Check file permissions"
                ],
                "confidence": "high"
            })
        
        # Permission errors
        elif 'permissionerror' in error_lower or 'permission denied' in error_lower:
            solutions.append({
                "type": "permission",
                "title": "Fix permission issue",
                "steps": [
                    "Run with appropriate permissions",
                    "Check file/directory permissions",
                    "Close file handles before writing",
                    "Use sudo/admin if necessary (carefully)"
                ],
                "confidence": "medium"
            })
        
        # Generic fallback
        if not solutions:
            solutions.append({
                "type": "generic",
                "title": "General debugging steps",
                "steps": [
                    "Read the full error traceback carefully",
                    "Search exact error message online",
                    "Check documentation for the component",
                    "Add debug print statements",
                    "Verify all dependencies are installed",
                    "Check for version compatibility issues"
                ],
                "confidence": "low"
            })
        
        return solutions
    
    def _extract_module_name(self, error_message: str) -> str:
        """Extract module name from ModuleNotFoundError."""
        # Pattern: No module named 'modulename'
        import re
        match = re.search(r"No module named ['\"]([^'\"]+)['\"]", error_message)
        if match:
            return match.group(1)
        return "unknown"
    
    def _extract_variable_name(self, error_message: str) -> str:
        """Extract variable name from NameError."""
        import re
        match = re.search(r"name ['\"]([^'\"]+)['\"]", error_message)
        if match:
            return match.group(1)
        return "unknown"
    
    def _format_summary(self, error_message: str, solutions: list) -> str:
        """
        Format solutions into a readable summary.
        
        Args:
            error_message: The original error
            solutions: List of solution dictionaries
            
        Returns:
            str: Formatted summary string
        """
        summary_lines = []
        summary_lines.append("=" * 70)
        summary_lines.append("RESEARCHER: Error Analysis & Solutions")
        summary_lines.append("=" * 70)
        summary_lines.append(f"\nError: {error_message[:200]}...\n")
        
        for i, solution in enumerate(solutions, 1):
            summary_lines.append(f"\n### Solution {i}: {solution['title']}")
            summary_lines.append(f"Type: {solution['type']}")
            summary_lines.append(f"Confidence: {solution['confidence']}")
            summary_lines.append("\nSteps:")
            for step in solution['steps']:
                summary_lines.append(f"  • {step}")
        
        summary_lines.append("\n" + "=" * 70)
        summary_lines.append("End of research results")
        summary_lines.append("=" * 70)
        
        return "\n".join(summary_lines)
