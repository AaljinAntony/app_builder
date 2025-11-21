import re
from utils.gemini_client import generate_with_retry
from prompts.templates import PromptTemplates
from utils.logger import logger
from utils.file_ops import write_file

class BackendCoder:
    """Generates backend code (API endpoints, business logic)."""
    
    def run(self, task: str, project_path: str, context: dict) -> dict:
        """
        Generates backend code based on task and context.
        Writes generated files to the current directory.
        
        Returns:
            dict: {"success": bool, "output": {"files": list}, "error": str/None}
        """
        prompt = PromptTemplates.backend_coder(task, context)
        try:
            logger.info("BackendCoder: Generating backend code")
            response = generate_with_retry(prompt, temperature=0.3)
            
            files_created = self._parse_and_save_files(response)
            
            if not files_created:
                logger.warning("BackendCoder: No files were created from the response")
            
            logger.info(f"BackendCoder: Created {len(files_created)} files: {files_created}")
            return {"success": True, "output": {"files": files_created}, "error": None}
        except Exception as e:
            logger.error(f"BackendCoder error: {e}")
            return {"success": False, "output": {}, "error": str(e)}

    def _parse_and_save_files(self, response: str) -> list:
        """
        Parses response for 'Filename: <name>' and code blocks, then writes files.
        """
        files = []
        # Regex to find Filename: <name> followed by code block
        pattern = r"Filename:\s*(.+?)\s*\n```\w*\n(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)
        
        for filename, code in matches:
            filename = filename.strip()
            # Write file
            if write_file(filename, code.strip()):
                files.append(filename)
                logger.info(f"BackendCoder: Wrote {filename}")
            else:
                logger.error(f"BackendCoder: Failed to write {filename}")
                
        return files
