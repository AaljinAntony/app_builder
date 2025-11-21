from utils.gemini_client import generate_with_retry, extract_json
from prompts.templates import PromptTemplates
from utils.command_executor import execute
from utils.logger import logger
import shlex

class TerminalAgent:
    """Executes terminal commands based on AI-generated command list."""
    
    def run(self, task: str, project_path: str, context: dict) -> dict:
        """
        Generates and executes terminal commands.
        
        Returns:
            dict: {"success": bool, "output": {"results": list}, "error": str/None}
        """
        prompt = PromptTemplates.terminal_agent(task, context)
        try:
            logger.info("TerminalAgent: Generating commands")
            response = generate_with_retry(prompt, temperature=0.2)
            result = extract_json(response)
            commands = result.get("commands", [])
            
            logger.info(f"TerminalAgent: Executing {len(commands)} commands")
            outputs = []
            for cmd in commands:
                logger.info(f"TerminalAgent: Running '{cmd}'")
                cmd_list = shlex.split(cmd, posix=False)
                exec_result = execute(cmd_list, cwd=project_path)
                outputs.append({
                    "command": cmd,
                    "result": exec_result
                })
                
            logger.info("TerminalAgent: All commands executed")
            return {"success": True, "output": {"results": outputs}, "error": None}
        except Exception as e:
            logger.error(f"TerminalAgent error: {e}")
            return {"success": False, "output": {}, "error": str(e)}
