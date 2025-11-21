from agents.language_selector import LanguageSelector
from agents.planner import Planner
from agents.frontend_coder import FrontendCoder
from agents.backend_coder import BackendCoder
from agents.tester import Tester
from agents.debugger import Debugger
from agents.terminal_agent import TerminalAgent
from agents.documentation import DocumentationAgent
from utils.logger import logger
import os

def test_all_agents():
    logger.info("=" * 50)
    logger.info("Testing All Agent Implementations")
    logger.info("=" * 50)

    context = {
        "project_name": "test_app",
        "language_config": {"language": "Python", "framework": "Flask"}
    }
    project_path = os.getcwd()

    agents = [
        ("LanguageSelector", LanguageSelector(), "Build a web app"),
        ("Planner", Planner(), "Build a web app"),
        ("FrontendCoder", FrontendCoder(), "Create login page"),
        ("BackendCoder", BackendCoder(), "Create auth API"),
        ("Tester", Tester(), "Test auth API"),
        ("Debugger", Debugger(), "Fix TypeError in auth"),
        ("TerminalAgent", TerminalAgent(), "Install Flask"),
        ("DocumentationAgent", DocumentationAgent(), "Create README")
    ]

    for agent_name, agent, task in agents:
        logger.info(f"\n--- Testing {agent_name} ---")
        try:
            result = agent.run(task, project_path, context)
            if result["success"]:
                logger.info(f"✓ {agent_name}: SUCCESS")
            else:
                logger.warning(f"✗ {agent_name}: FAILED - {result['error']}")
        except Exception as e:
            logger.error(f"✗ {agent_name}: EXCEPTION - {e}")

    logger.info("\n" + "=" * 50)
    logger.info("Agent Testing Complete")
    logger.info("=" * 50)

if __name__ == "__main__":
    test_all_agents()
