import os
from utils.file_ops import file_exists, read_file
from utils.logger import logger

class AgentManager:
    """
    CEO/Controller for the multi-agent system.
    Orchestrates workflow by deciding which agent should act next.
    NO AI CALLS - Pure decision logic based on project state.
    """
    
    def decide_next_agent(self, context: dict) -> dict:
        """
        Decides the next agent to run based on the project state.
        
        Args:
            context: Current context containing:
                - language_config (dict, optional): Tech stack configuration
                - last_action (str, optional): Name of last agent that ran
                - project_path (str, optional): Project directory path
                
        Returns:
            dict: {"next_agent": str, "reasoning": str}
                - next_agent: Name of agent to run next or "FINISHED"
                - reasoning: Brief explanation of the decision
        """
        last_action = context.get("last_action")
        project_path = context.get("project_path", "")
        
        logger.info(f"AgentManager: Deciding next agent (last_action={last_action})")
        
        # 1. Language Selection
        if "language_config" not in context:
            logger.info("AgentManager: No language_config → LanguageSelector")
            next_agent = "LanguageSelector"
        
        # 2. Planning
        elif not self._check_file_exists(project_path, "PLAN.md"):
            logger.info("AgentManager: No PLAN.md → Planner")
            next_agent = "Planner"
        
        # 3. Frontend (state-based progression)
        elif last_action == "Planner":
            logger.info("AgentManager: After Planner → FrontendCoder")
            next_agent = "FrontendCoder"
        
        # 4. Backend (state-based progression)
        elif last_action == "FrontendCoder":
            logger.info("AgentManager: After FrontendCoder → BackendCoder")
            next_agent = "BackendCoder"
        
        # 5. Dependencies (state-based progression)
        elif last_action == "BackendCoder":
            logger.info("AgentManager: After BackendCoder → TerminalAgent")
            next_agent = "TerminalAgent"
        
        # 6. Testing
        elif not self._check_file_exists(project_path, "TEST_REPORT.md"):
            logger.info("AgentManager: No TEST_REPORT.md → Tester")
            next_agent = "Tester"
        
        # 7. Debugging (if tests failed)
        elif self._tests_failed(project_path):
            if last_action == "Debugger":
                # Re-run tests after debugging
                logger.info("AgentManager: After Debugger → Tester (retest)")
                next_agent = "Tester"
            elif last_action == "Tester":
                logger.info("AgentManager: Tests failed → Debugger")
                next_agent = "Debugger"
            else:
                next_agent = "Tester"
        
        # 8. Documentation
        elif not self._check_file_exists(project_path, "README.md"):
            logger.info("AgentManager: No README.md → DocumentationAgent")
            next_agent = "DocumentationAgent"
        
        # 9. Version Control (new with MCP integration)
        elif not self._check_git_initialized(project_path):
            logger.info("AgentManager: No .git → GitAgent")
            next_agent = "GitAgent"
        
        # 10. Completion
        else:
            logger.info("AgentManager: All steps complete → FINISHED")
            next_agent = "FINISHED"
        
        # Anti-loop protection: Prevent same agent from running twice
        if last_action and next_agent == last_action and next_agent != "FINISHED":
            logger.warning(f"AgentManager: Anti-loop detected - {next_agent} called twice")
            return {
                "next_agent": "FINISHED",
                "reasoning": f"Loop prevented: {next_agent} already ran."
            }
        
        # Map to reasoning
        reasoning_map = {
            "LanguageSelector": "Language configuration is missing.",
            "Planner": "Implementation plan (PLAN.md) is missing.",
            "FrontendCoder": "Plan complete, starting frontend development.",
            "BackendCoder": "Frontend complete, moving to backend.",
            "TerminalAgent": "Code complete, installing dependencies.",
            "Tester": "Test report is missing." if not self._tests_failed(project_path) else "Debugging applied, re-running tests.",
            "Debugger": "Tests failed, triggering debugger.",
            "DocumentationAgent": "Project documentation is missing.",
            "GitAgent": "Initializing version control for generated project.",
            "FINISHED": "All steps complete."
        }
        
        return {
            "next_agent": next_agent,
            "reasoning": reasoning_map.get(next_agent, "Proceeding to next step.")
        }


    
    def _check_file_exists(self, project_path: str, filename: str) -> bool:
        """
        Helper: Check if a file exists in the project directory.
        
        Args:
            project_path: Path to project directory
            filename: Name of file to check
            
        Returns:
            bool: True if file exists, False otherwise
        """

        if not project_path:
            return False
        
        # Since main.py changes CWD to project_path, we should check for the file 
        # in the current directory.
        # If we use os.path.join(project_path, filename), it creates a nested path
        # relative to CWD (e.g. project/app/project/app/PLAN.md).
        
        return os.path.exists(filename)
    
    def _tests_failed(self, project_path: str) -> bool:
        """
        Helper: Check if tests failed by inspecting TEST_REPORT.md.
        
        Args:
            project_path: Path to project directory
        
        Returns:
            bool: True if tests failed, False if passed or file missing
        """
        if not self._check_file_exists(project_path, "TEST_REPORT.md"):
            return False
        
        try:
            # We are already in the project directory, so just use the filename
            full_path = "TEST_REPORT.md"
            report_content = read_file(full_path)
            # Simple keyword check for failure indicators
            failure_keywords = ["FAIL", "FAILED", "Error", "ERROR", "Exception"]
            return any(keyword in report_content for keyword in failure_keywords)
        except Exception as e:
            logger.warning(f"AgentManager: Could not read TEST_REPORT.md: {e}")
            return False
    
    def _check_git_initialized(self, project_path: str) -> bool:
        """
        Helper: Check if git is initialized in the project directory.
        
        Args:
            project_path: Path to project directory
            
        Returns:
            bool: True if .git directory exists, False otherwise
        """
        if not project_path:
            return False
        
        # Check for .git directory (we're in the project directory)
        return os.path.exists(".git") and os.path.isdir(".git")
