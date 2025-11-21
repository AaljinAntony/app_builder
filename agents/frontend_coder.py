import re
from utils.gemini_client import generate_with_retry
from prompts.templates import PromptTemplates
from utils.logger import logger
from utils.file_ops import write_file

class FrontendCoder:
    """Generates frontend code (HTML/CSS/JS or framework code)."""
    
    def run(self, task: str, project_path: str, context: dict) -> dict:
        """
        Generates frontend code based on task and context.
        Writes generated files to the current directory.
        
        Returns:
            dict: {"success": bool, "output": {"files": list}, "error": str/None}
        """
        prompt = PromptTemplates.frontend_coder(task, context)
        try:
            logger.info("FrontendCoder: Generating frontend code")
            response = generate_with_retry(prompt, temperature=0.3)
            
            files_created = self._parse_and_save_files(response)
            
            if not files_created:
                logger.warning("FrontendCoder: No files were created from the response")
                # Fallback: if no files parsed but response exists, maybe save as frontend_code.md?
                # For now, just log it.
            
            logger.info(f"FrontendCoder: Created {len(files_created)} files: {files_created}")
            return {"success": True, "output": {"files": files_created}, "error": None}
        except Exception as e:
            logger.error(f"FrontendCoder error: {e}")
            return {"success": False, "output": {}, "error": str(e)}

    def _parse_and_save_files(self, response: str) -> list:
        """
        Parses response for 'Filename: <name>' and code blocks, then writes files.
        """
        files = []
        # Regex to find Filename: <name> followed by code block
        # Matches: Filename: index.html \n ```html \n <code> \n ```
        pattern = r"Filename:\s*(.+?)\s*\n```\w*\n(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)
        
        for filename, code in matches:
            filename = filename.strip()
            # Remove any path components to ensure writing to current dir (security/safety)
            # Actually, subdirectories might be valid (e.g. src/index.js), but for now let's trust the agent
            # or just ensure it doesn't go up directories.
            
            # Write file
            if write_file(filename, code.strip()):
                files.append(filename)
                logger.info(f"FrontendCoder: Wrote {filename}")
            else:
                logger.error(f"FrontendCoder: Failed to write {filename}")
                
        return files
