from utils.gemini_client import generate_with_retry
from prompts.templates import PromptTemplates
from utils.logger import logger

class Debugger:
    """Analyzes errors and proposes fixes."""
    
    def run(self, task: str, project_path: str, context: dict) -> dict:
        """
        Analyzes bugs and generates fixes.
        
        Returns:
            dict: {"success": bool, "output": {"analysis": str}, "error": str/None}
        """
        prompt = PromptTemplates.debugger(task, context)
        try:
            logger.info("Debugger: Analyzing error")
            response = generate_with_retry(prompt, temperature=0.4)
            logger.info("Debugger: Analysis complete")
            return {"success": True, "output": {"analysis": response}, "error": None}
        except Exception as e:
            logger.error(f"Debugger error: {e}")
            return {"success": False, "output": {}, "error": str(e)}
