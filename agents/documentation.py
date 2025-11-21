from utils.gemini_client import generate_with_retry
from prompts.templates import PromptTemplates
from utils.logger import logger

class DocumentationAgent:
    """Generates project documentation."""
    
    def run(self, task: str, project_path: str, context: dict) -> dict:
        """
        Generates documentation (README, API docs, etc.).
        
        Returns:
            dict: {"success": bool, "output": {"documentation": str}, "error": str/None}
        """
        prompt = PromptTemplates.documentation_agent(task, context)
        try:
            logger.info("DocumentationAgent: Generating documentation")
            response = generate_with_retry(prompt, temperature=0.4)
            logger.info("DocumentationAgent: Documentation complete")
            return {"success": True, "output": {"documentation": response}, "error": None}
        except Exception as e:
            logger.error(f"DocumentationAgent error: {e}")
            return {"success": False, "output": {}, "error": str(e)}
