from utils.gemini_client import generate_with_retry, extract_json
from prompts.templates import PromptTemplates
from utils.logger import logger

class LanguageSelector:
    """Selects the programming language and tech stack for the project."""
    
    def run(self, task: str, project_path: str, context: dict) -> dict:
        """
        Analyzes the task and selects appropriate tech stack.
        
        Returns:
            dict: {"success": bool, "output": dict, "error": str/None}
        """
        prompt = PromptTemplates.language_selector(task)
        try:
            logger.info("LanguageSelector: Analyzing task and selecting stack")
            response = generate_with_retry(prompt, temperature=0.4)
            result = extract_json(response)
            logger.info(f"LanguageSelector: Selected {result.get('language', 'unknown')}")
            return {"success": True, "output": result, "error": None}
        except Exception as e:
            logger.error(f"LanguageSelector error: {e}")
            return {"success": False, "output": {}, "error": str(e)}
