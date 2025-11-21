from utils.gemini_client import generate_with_retry
from prompts.templates import PromptTemplates
from utils.logger import logger

class Tester:
    """Generates test code for implemented features."""
    
    def run(self, task: str, project_path: str, context: dict) -> dict:
        """
        Generates unit or integration tests.
        
        Returns:
            dict: {"success": bool, "output": {"code": str}, "error": str/None}
        """
        prompt = PromptTemplates.tester(task, context)
        try:
            logger.info("Tester: Generating test code")
            response = generate_with_retry(prompt, temperature=0.3)
            logger.info("Tester: Test generation complete")
            return {"success": True, "output": {"code": response}, "error": None}
        except Exception as e:
            logger.error(f"Tester error: {e}")
            return {"success": False, "output": {}, "error": str(e)}
