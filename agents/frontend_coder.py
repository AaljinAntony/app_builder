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
        Validates content before writing to avoid placeholders.
        """
        files = []
        # Regex to find Filename: <name> followed by code block
        # Matches: Filename: index.html \n ```html \n <code> \n ```
        pattern = r"Filename:\s*(.+?)\s*\n```\w*\n(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)
        
        for filename, code in matches:
            filename = filename.strip()
            code = code.strip()
            
            # Validation: Check if content is a placeholder
            if not self._is_valid_code(code, filename):
                logger.warning(f"FrontendCoder: Skipping {filename} - appears to be placeholder/comment-only")
                continue
            
            # Write file
            if write_file(filename, code):
                files.append(filename)
                logger.info(f"FrontendCoder: Wrote {filename} ({len(code)} chars)")
            else:
                logger.error(f"FrontendCoder: Failed to write {filename}")
                
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

