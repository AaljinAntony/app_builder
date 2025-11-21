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
        Validates content before writing to avoid placeholders.
        """
        files = []
        # Regex to find Filename: <name> followed by code block
        pattern = r"Filename:\s*(.+?)\s*\n```\w*\n(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)
        
        for filename, code in matches:
            filename = filename.strip()
            code = code.strip()
            
            # Validation: Check if content is a placeholder
            if not self._is_valid_code(code, filename):
                logger.warning(f"BackendCoder: Skipping {filename} - appears to be placeholder/comment-only")
                continue
            
            # Write file
            if write_file(filename, code):
                files.append(filename)
                logger.info(f"BackendCoder: Wrote {filename} ({len(code)} chars)")
            else:
                logger.error(f"BackendCoder: Failed to write {filename}")
                
        return files
    
    def _is_valid_code(self, code: str, filename: str) -> bool:
        """
        Validates if code is real implementation or just placeholder.
        Returns False if it appears to be placeholder/comment-only.
        """
        # Check 1: Minimum length (too short = likely placeholder)
        if len(code) < 50:
            return False
        
        # Check 2: Look for placeholder patterns
        placeholder_patterns = [
            r"//\s*\.\.\.",  # // ...
            r"#\s*\.\.\.",   # # ...
            r"/\*.*\*/\s*$", # Only /* comment */
            r"<!--.*-->\s*$", # Only <!-- comment -->
        ]
        
        for pattern in placeholder_patterns:
            if re.search(pattern, code, re.DOTALL):
                # If entire content matches placeholder, reject
                non_comment = re.sub(pattern, "", code, flags=re.DOTALL).strip()
                if len(non_comment) < 20:
                    return False
        
        # Check 3: Check for common placeholder comments
        placeholder_keywords = [
            "rest of code",
            "implementation",
            "add your code here",
            "placeholder",
            "todo",
        ]
        
        code_lower = code.lower()
        # If code is mostly just these keywords, it's likely placeholder
        if any(keyword in code_lower for keyword in placeholder_keywords):
            # Count non-whitespace characters
            non_ws = len(code.replace(" ", "").replace("\n", "").replace("\t", ""))
            if non_ws < 100:  # Very short with placeholder keywords = bad
                return False
        
        return True

