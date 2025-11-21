"""
Unit tests for all agent classes.
Uses pytest with mocking to avoid real API calls.
"""
import pytest
from unittest.mock import Mock, patch
from agents.language_selector import LanguageSelector
from agents.planner import Planner
from agents.frontend_coder import FrontendCoder
from agents.backend_coder import BackendCoder
from agents.terminal_agent import TerminalAgent
from agents.tester import Tester
from agents.debugger import Debugger
from agents.documentation import DocumentationAgent


@pytest.fixture
def mock_gemini_client():
    """Mock the gemini_client module to avoid real API calls."""
    with patch('utils.gemini_client.generate_with_retry') as mock_generate, \
         patch('utils.gemini_client.extract_json') as mock_extract:
        
        # Default mock responses
        mock_generate.return_value = '{"success": true, "data": "mocked response"}'
        mock_extract.return_value = {"success": True, "data": "mocked response"}
        
        yield {
            'generate': mock_generate,
            'extract_json': mock_extract
        }


@pytest.fixture
def dummy_context():
    """Provide a dummy context for agent testing."""
    return {
        "project_name": "test_project",
        "language_config": {
            "language": "Python",
            "framework": "Flask"
        },
        "last_action": None
    }


class TestLanguageSelector:
    """Test LanguageSelector agent."""
    
    def test_language_selector_run(self, mock_gemini_client, dummy_context):
        """Test LanguageSelector returns correct structure."""
        mock_gemini_client['extract_json'].return_value = {
            "language": "Python",
            "framework": "Flask",
            "reasoning": "Test"
        }
        
        agent = LanguageSelector()
        result = agent.run("Build a web app", "/test/path", dummy_context)
        
        assert "success" in result
        assert "output" in result
        assert "error" in result
        assert result["success"] is True
        assert result["error"] is None


class TestPlanner:
    """Test Planner agent."""
    
    def test_planner_run(self, mock_gemini_client, dummy_context, tmp_path):
        """Test Planner returns correct structure."""
        mock_gemini_client['extract_json'].return_value = {
            "plan": [
                {"step_id": 1, "description": "Setup", "files": ["main.py"]}
            ],
            "overview": "Test project overview",
            "file_structure": "project/\n├── main.py\n└── README.md",
            "frontend_architecture": "Simple HTML/CSS",
            "backend_architecture": "Flask API server",
            "api_endpoints": "GET /api/test",
            "dependencies": ["flask==3.0.0"],
            "build_commands": ["pip install -r requirements.txt", "python main.py"]
        }
        
        agent = Planner()
        result = agent.run("Build a web app", str(tmp_path), dummy_context)
        
        assert "success" in result
        assert "output" in result
        assert "error" in result
        assert result["success"] is True



class TestFrontendCoder:
    """Test FrontendCoder agent."""
    
    def test_frontend_coder_run(self, mock_gemini_client, dummy_context):
        """Test FrontendCoder returns correct structure."""
        mock_gemini_client['generate'].return_value = """
```html
<html><body>Test</body></html>
```
"""
        
        agent = FrontendCoder()
        result = agent.run("Create login page", "/test/path", dummy_context)
        
        assert "success" in result
        assert "output" in result
        assert "error" in result
        assert result["success"] is True
        assert "code" in result["output"]


class TestBackendCoder:
    """Test BackendCoder agent."""
    
    def test_backend_coder_run(self, mock_gemini_client, dummy_context):
        """Test BackendCoder returns correct structure."""
        mock_gemini_client['generate'].return_value = """
```python
def hello():
    return "Hello"
```
"""
        
        agent = BackendCoder()
        result = agent.run("Create API endpoint", "/test/path", dummy_context)
        
        assert "success" in result
        assert "output" in result
        assert "error" in result
        assert result["success"] is True
        assert "code" in result["output"]


class TestTerminalAgent:
    """Test TerminalAgent agent."""
    
    @patch('utils.command_executor.execute')
    def test_terminal_agent_run(self, mock_execute, mock_gemini_client, dummy_context):
        """Test TerminalAgent returns correct structure."""
        mock_gemini_client['extract_json'].return_value = {
            "commands": ["pip install flask"],
            "reasoning": "Install dependencies"
        }
        
        mock_execute.return_value = {
            "success": True,
            "stdout": "Successfully installed",
            "stderr": "",
            "exit_code": 0
        }
        
        agent = TerminalAgent()
        result = agent.run("Install Flask", "/test/path", dummy_context)
        
        assert "success" in result
        assert "output" in result
        assert "error" in result
        assert result["success"] is True
        assert "results" in result["output"]


class TestTester:
    """Test Tester agent."""
    
    def test_tester_run(self, mock_gemini_client, dummy_context):
        """Test Tester returns correct structure."""
        mock_gemini_client['generate'].return_value = """
```python
def test_example():
    assert True
```
"""
        
        agent = Tester()
        result = agent.run("Test the API", "/test/path", dummy_context)
        
        assert "success" in result
        assert "output" in result
        assert "error" in result
        assert result["success"] is True
        assert "code" in result["output"]


class TestDebugger:
    """Test Debugger agent."""
    
    def test_debugger_run(self, mock_gemini_client, dummy_context):
        """Test Debugger returns correct structure."""
        mock_gemini_client['generate'].return_value = """
# Bug Analysis
The error is caused by...

# Fix
```python
def fixed_function():
    return "fixed"
```
"""
        
        agent = Debugger()
        result = agent.run("Fix TypeError", "/test/path", dummy_context)
        
        assert "success" in result
        assert "output" in result
        assert "error" in result
        assert result["success"] is True
        assert "analysis" in result["output"]


class TestDocumentationAgent:
    """Test DocumentationAgent agent."""
    
    def test_documentation_agent_run(self, mock_gemini_client, dummy_context):
        """Test DocumentationAgent returns correct structure."""
        mock_gemini_client['generate'].return_value = """
# My Project

## Installation
pip install -r requirements.txt

## Usage
python main.py
"""
        
        agent = DocumentationAgent()
        result = agent.run("Create README", "/test/path", dummy_context)
        
        assert "success" in result
        assert "output" in result
        assert "error" in result
        assert result["success"] is True
        assert "documentation" in result["output"]


class TestAllAgentsErrorHandling:
    """Test that all agents handle errors gracefully."""
    
    @patch('utils.gemini_client.generate_with_retry')
    @patch('utils.command_executor.execute')  # Mock command executor for TerminalAgent
    def test_agents_handle_api_errors(self, mock_execute, mock_generate):
        """Test all agents handle API errors gracefully."""
        # Make the API call fail
        mock_generate.side_effect = Exception("API Error")
        
        # Mock command executor to succeed (won't be called due to API error)
        mock_execute.return_value = {"success": True, "stdout": "", "stderr": "", "exit_code": 0}
        
        agents = [
            LanguageSelector(),
            Planner(),
            FrontendCoder(),
            BackendCoder(),
            Tester(),
            Debugger(),
            DocumentationAgent(),
            TerminalAgent()  # Added TerminalAgent
        ]
        
        context = {"language_config": {}}
        
        for agent in agents:
            result = agent.run("Test task", "/test/path", context)
            
            # Should return error structure, not raise exception
            assert "success" in result
            assert result["success"] is False
            assert result["error"] is not None
            assert "API Error" in result["error"]
