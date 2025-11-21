"""
Integration tests for the MultiAgentBuilder system.
Uses pytest with extensive mocking to avoid real API calls.
"""
import pytest
import os
import shutil
from unittest.mock import Mock, patch, MagicMock
from main import MultiAgentBuilder


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    yield str(project_dir)
    # Cleanup handled by tmp_path


@pytest.fixture
def mock_agent_manager():
    """Mock AgentManager to simulate a short workflow."""
    with patch('main.AgentManager') as MockAgentManager:
        mock_manager = Mock()
        
        # Simulate a simple workflow: LanguageSelector -> Planner -> FINISHED
        decision_sequence = [
            {"next_agent": "LanguageSelector", "reasoning": "Select tech stack"},
            {"next_agent": "Planner", "reasoning": "Create plan"},
            {"next_agent": "FINISHED", "reasoning": "All done"}
        ]
        
        mock_manager.decide_next_agent.side_effect = decision_sequence
        MockAgentManager.return_value = mock_manager
        
        yield mock_manager


@pytest.fixture
def mock_all_agents():
    """Mock all agent classes to avoid real API calls."""
    agents_to_mock = [
        'main.LanguageSelector',
        'main.Planner',
        'main.FrontendCoder',
        'main.BackendCoder',
        'main.TerminalAgent',
        'main.Tester',
        'main.Debugger',
        'main.DocumentationAgent'
    ]
    
    patches = []
    mocks = {}
    
    for agent_path in agents_to_mock:
        patcher = patch(agent_path)
        mock_class = patcher.start()
        
        # Mock instance and run method
        mock_instance = Mock()
        mock_instance.run.return_value = {
            "success": True,
            "output": {"data": "mocked"},
            "error": None
        }
        mock_class.return_value = mock_instance
        
        mocks[agent_path.split('.')[-1]] = mock_instance
        patches.append(patcher)
    
    yield mocks
    
    # Stop all patches
    for patcher in patches:
        patcher.stop()


class TestMultiAgentBuilder:
    """Test the MultiAgentBuilder orchestrator."""
    
    def test_initialization(self):
        """Test MultiAgentBuilder initializes correctly."""
        builder = MultiAgentBuilder()
        
        assert builder.project_name == ""
        assert builder.project_path == ""
        assert builder.goal == ""
        assert builder.language_config is None
        assert builder.loop_counter == 0
        assert builder.error_count == 0
        assert builder.max_loops > 0
        assert builder.max_errors > 0
        assert isinstance(builder.state, dict)
    
    def test_sanitize_project_name(self):
        """Test project name sanitization."""
        builder = MultiAgentBuilder()
        
        # Test normal case
        name1 = builder._sanitize_project_name("Build a TODO App!")
        assert name1 == "build_a_todo_app"
        
        # Test special characters removal
        name2 = builder._sanitize_project_name("API @#$ Service")
        assert "@" not in name2
        assert "#" not in name2
        assert "$" not in name2
        
        # Test empty string
        name3 = builder._sanitize_project_name("")
        assert name3 == "my_project"
    
    def test_get_project_context(self):
        """Test context building."""
        builder = MultiAgentBuilder()
        builder.project_name = "test_app"
        builder.project_path = "/test/path"
        builder.goal = "Build a test app"
        builder.language_config = {"language": "Python"}
        builder.state["last_action"] = "LanguageSelector"
        builder.loop_counter = 5
        
        context = builder._get_project_context()
        
        assert context["project_name"] == "test_app"
        assert context["project_path"] == "/test/path"
        assert context["goal"] == "Build a test app"
        assert context["language_config"]["language"] == "Python"
        assert context["last_action"] == "LanguageSelector"
        assert context["loop_counter"] == 5
    
    @patch('os.chdir')
    @patch('os.makedirs')
    def test_start_creates_project_folder(self, mock_makedirs, mock_chdir, 
                                         mock_agent_manager, mock_all_agents):
        """Test that start() creates project folder."""
        builder = MultiAgentBuilder()
        
        # Run with a simple goal
        builder.start("Build a simple app")
        
        # Verify project folder was created
        mock_makedirs.assert_called()
        assert builder.project_name != ""
        assert "project" in builder.project_path
    
    @patch('os.chdir')
    @patch('os.makedirs')
    def test_start_completes_without_exception(self, mock_makedirs, mock_chdir,
                                              mock_agent_manager, mock_all_agents):
        """Test that start() completes without exceptions."""
        builder = MultiAgentBuilder()
        
        # This should complete without raising exceptions
        try:
            builder.start("Build a todo app")
            success = True
        except Exception as e:
            success = False
            print(f"Exception: {e}")
        
        assert success is True
    
    @patch('os.chdir')
    @patch('os.makedirs')
    def test_agent_loop_stops_at_finished(self, mock_makedirs, mock_chdir,
                                         mock_agent_manager, mock_all_agents):
        """Test that agent loop stops when FINISHED."""
        builder = MultiAgentBuilder()
        builder.start("Build app")
        
        # Should have stopped at FINISHED, not hit max loops
        assert builder.loop_counter < builder.max_loops
    
    @patch('os.chdir')
    @patch('os.makedirs')
    def test_error_counting(self, mock_makedirs, mock_chdir):
        """Test that error counting works correctly."""
        with patch('main.AgentManager') as MockAgentManager:
            mock_manager = Mock()
            
            # Simulate errors until max_errors
            mock_manager.decide_next_agent.return_value = {
                "next_agent": "LanguageSelector",
                "reasoning": "Test"
            }
            MockAgentManager.return_value = mock_manager
            
            # Mock LanguageSelector to always fail
            with patch('main.LanguageSelector') as MockLangSel:
                mock_instance = Mock()
                mock_instance.run.return_value = {
                    "success": False,
                    "output": {},
                    "error": "Test error"
                }
                MockLangSel.return_value = mock_instance
                
                builder = MultiAgentBuilder()
                builder.max_errors = 3
                builder.start("Test app")
                
                # Should have stopped after 3 errors
                assert builder.error_count >= builder.max_errors
    
    def test_execute_agent_routes_correctly(self, mock_all_agents):
        """Test that _execute_agent routes to correct agent."""
        builder = MultiAgentBuilder()
        builder.project_path = "/test/path"
        
        # Test each agent routing
        agents_to_test = [
            "LanguageSelector",
            "Planner",
            "FrontendCoder",
            "BackendCoder",
            "TerminalAgent",
            "Tester",
            "Debugger",
            "DocumentationAgent"
        ]
        
        for agent_name in agents_to_test:
            result = builder._execute_agent(agent_name, "Test task")
            
            # Should return proper structure
            assert "success" in result
            assert "output" in result
            assert "error" in result
    
    def test_execute_agent_handles_unknown_agent(self):
        """Test handling of unknown agent name."""
        builder = MultiAgentBuilder()
        builder.project_path = "/test/path"
        
        result = builder._execute_agent("UnknownAgent", "Test task")
        
        assert result["success"] is False
        assert "Unknown agent" in result["error"]


class TestSystemIntegration:
    """Integration tests for the complete system."""
    
    @patch('os.chdir')
    @patch('os.makedirs')
    @patch('os.getcwd', return_value='/original/dir')
    def test_directory_handling(self, mock_getcwd, mock_makedirs, mock_chdir,
                               mock_agent_manager, mock_all_agents):
        """Test that system changes and restores directories correctly."""
        builder = MultiAgentBuilder()
        builder.start("Test app")
        
        # Should have changed directory and returned
        assert mock_chdir.call_count >= 2  # Change to project, change back
    
    @patch('os.chdir')
    @patch('os.makedirs')
    def test_state_tracking(self, mock_makedirs, mock_chdir,
                           mock_agent_manager, mock_all_agents):
        """Test that state is tracked correctly."""
        builder = MultiAgentBuilder()
        builder.start("Test app")
        
        # State should be updated
        assert "last_action" in builder.state
        assert "completed_steps" in builder.state
        assert isinstance(builder.state["completed_steps"], list)
