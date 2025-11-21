import os
import sys
import re
from dotenv import load_dotenv
from utils.logger import logger
from agents.agent_manager import AgentManager
from agents.language_selector import LanguageSelector
from agents.planner import Planner
from agents.frontend_coder import FrontendCoder
from agents.backend_coder import BackendCoder
from agents.terminal_agent import TerminalAgent
from agents.tester import Tester
from agents.debugger import Debugger
from agents.documentation import DocumentationAgent

load_dotenv()

class MultiAgentBuilder:
    """
    Main orchestrator for the multi-agent development system.
    Manages the workflow loop, error handling, and agent coordination.
    """
    
    def __init__(self):
        """Initialize the MultiAgentBuilder."""
        self.project_name = ""
        self.project_path = ""
        self.goal = ""
        self.language_config = None
        self.agent_manager = AgentManager()
        self.loop_counter = 0
        self.max_loops = int(os.getenv("MAX_LOOPS", "50"))
        self.error_count = 0
        self.max_errors = int(os.getenv("MAX_ERRORS", "3"))
        self.state = {
            "last_action": None,
            "last_error": None,
            "completed_steps": []
        }
        
        logger.info("MultiAgentBuilder initialized")
        logger.info(f"Max loops: {self.max_loops}, Max errors: {self.max_errors}")
    
    def start(self, user_prompt: str) -> None:
        """
        Start the multi-agent development process.
        
        Args:
            user_prompt: User's description of what to build
        """
        logger.info("=" * 70)
        logger.info("MULTI-AGENT BUILDER STARTING")
        logger.info("=" * 70)
        logger.info(f"User prompt: {user_prompt}")
        
        # Sanitize project name from prompt
        self.goal = user_prompt
        self.project_name = self._sanitize_project_name(user_prompt)
        
        # Create project folder
        self.project_path = os.path.join("project", self.project_name)
        os.makedirs(self.project_path, exist_ok=True)
        logger.info(f"Project path: {self.project_path}")
        
        # Change to project directory
        original_dir = os.getcwd()
        os.chdir(self.project_path)
        logger.info(f"Working directory: {os.getcwd()}")
        
        try:
            # Run the agent loop
            self._run_agent_loop()
        finally:
            # Return to original directory
            os.chdir(original_dir)
            logger.info(f"Returned to: {os.getcwd()}")
        
        logger.info("=" * 70)
        logger.info("MULTI-AGENT BUILDER FINISHED")
        logger.info("=" * 70)
    
    def _sanitize_project_name(self, prompt: str) -> str:
        """
        Create a safe project name from user prompt.
        
        Args:
            prompt: User prompt
            
        Returns:
            str: Sanitized project name
        """
        # Take first few words, remove special chars, lowercase
        name = prompt.lower()[:50]
        name = re.sub(r'[^a-z0-9\s]', '', name)
        name = re.sub(r'\s+', '_', name.strip())
        
        if not name:
            name = "my_project"
        
        logger.info(f"Project name: {name}")
        return name
    
    def _run_agent_loop(self) -> None:
        """
        Main agent execution loop.
        Continues until FINISHED or max loops/errors reached.
        """
        logger.info("\n" + "=" * 70)
        logger.info("STARTING AGENT LOOP")
        logger.info("=" * 70)
        
        while self.loop_counter < self.max_loops:
            self.loop_counter += 1
            logger.info(f"\n--- Loop {self.loop_counter}/{self.max_loops} ---")
            
            # Get current context
            context = self._get_project_context()
            
            # Decide next agent
            decision = self.agent_manager.decide_next_agent(context)
            next_agent = decision["next_agent"]
            reasoning = decision["reasoning"]
            
            logger.info(f"Decision: {next_agent}")
            logger.info(f"Reasoning: {reasoning}")
            
            # Check if finished
            if next_agent == "FINISHED":
                logger.info("\n" + "=" * 70)
                logger.info("PROJECT COMPLETE!")
                logger.info("=" * 70)
                break
            
            # Execute the agent
            task = self.goal  # Can be refined per agent
            result = self._execute_agent(next_agent, task)
            
            # Handle result with 3-strike error system (PROJECT_CONTEXT.md lines 998-1018)
            if result["success"]:
                logger.info(f"✓ {next_agent} completed successfully")
                self.state["last_action"] = next_agent
                self.state["completed_steps"].append(next_agent)
                self.error_count = 0  # Reset error count on success
            else:
                logger.error(f"✗ {next_agent} failed: {result['error']}")
                self.error_count += 1
                self.state["last_error"] = result["error"]
                
                # 3-Strike Error System
                if self.error_count == 1 or self.error_count == 2:
                    # Strike 1 & 2: Call Debugger (unless Debugger just ran)
                    if next_agent != "Debugger":
                        logger.warning(f"Strike {self.error_count}: Calling Debugger to fix error")
                        debug_task = f"Fix error from {next_agent}: {result['error']}"
                        debug_result = self._execute_agent("Debugger", debug_task)
                        
                        if debug_result["success"]:
                            logger.info("Debugger applied fix")
                            self.error_count = 0  # Reset if debugger succeeds
                            self.state["last_action"] = "Debugger"
                        else:
                            logger.error(f"Debugger also failed: {debug_result['error']}")
                    else:
                        logger.error(f"Strike {self.error_count}: Debugger itself failed")
                        
                elif self.error_count >= 3:
                    # Strike 3: Would call Researcher (not implemented)
                    logger.error("=" * 70)
                    logger.error("Max errors reached — stopping multi-agent workflow.")
                    logger.error("Researcher agent not implemented — terminating.")
                    logger.error("=" * 70)
                    break
        
        # Check if max loops reached
        if self.loop_counter >= self.max_loops:
            logger.warning(f"Max loops ({self.max_loops}) reached. Stopping.")
        
        logger.info(f"\nCompleted steps: {self.state['completed_steps']}")
    
    def _execute_agent(self, agent_name: str, task: str) -> dict:
        """
        Execute a specific agent.
        
        Args:
            agent_name: Name of the agent to execute
            task: Task description for the agent
            
        Returns:
            dict: Result from agent {"success": bool, "output": any, "error": str/None}
        """
        logger.info(f"Executing: {agent_name}")
        
        context = self._get_project_context()
        
        try:
            # Route to appropriate agent
            if agent_name == "LanguageSelector":
                agent = LanguageSelector()
                result = agent.run(task, self.project_path, context)
                # Save language config to state
                if result["success"]:
                    self.language_config = result["output"]
                    
            elif agent_name == "Planner":
                agent = Planner()
                result = agent.run(task, self.project_path, context)
                
            elif agent_name == "FrontendCoder":
                agent = FrontendCoder()
                result = agent.run(task, self.project_path, context)
                
            elif agent_name == "BackendCoder":
                agent = BackendCoder()
                result = agent.run(task, self.project_path, context)
                
            elif agent_name == "TerminalAgent":
                agent = TerminalAgent()
                result = agent.run(task, self.project_path, context)
                
            elif agent_name == "Tester":
                agent = Tester()
                result = agent.run(task, self.project_path, context)
                
            elif agent_name == "Debugger":
                agent = Debugger()
                result = agent.run(task, self.project_path, context)
                
            elif agent_name == "DocumentationAgent":
                agent = DocumentationAgent()
                result = agent.run(task, self.project_path, context)
                
            else:
                result = {
                    "success": False,
                    "output": {},
                    "error": f"Unknown agent: {agent_name}"
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Exception executing {agent_name}: {e}")
            return {
                "success": False,
                "output": {},
                "error": str(e)
            }
    
    def _get_project_context(self) -> dict:
        """
        Build context dictionary for agent decisions.
        
        Returns:
            dict: Context with current project state
        """
        context = {
            "project_name": self.project_name,
            "project_path": self.project_path,
            "goal": self.goal,
            "last_action": self.state["last_action"],
            "loop_counter": self.loop_counter,
            "completed_steps": self.state["completed_steps"]
        }
        
        # Add language config if available
        if self.language_config:
            context["language_config"] = self.language_config
        
        return context


def main():
    """CLI entry point for the MultiAgentBuilder."""
    print("=" * 70)
    print("MULTI-AGENT APP BUILDER")
    print("=" * 70)
    print()
    
    # Get user prompt
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
    else:
        user_prompt = input("What would you like to build? ")
    
    if not user_prompt or not user_prompt.strip():
        print("Error: Please provide a valid prompt.")
        sys.exit(1)
    
    # Create and start builder
    builder = MultiAgentBuilder()
    builder.start(user_prompt)
    
    print("\nProject created at:", builder.project_path)


if __name__ == "__main__":
    main()
