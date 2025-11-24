"""
GitAgent - Handles version control operations for generated projects.
Uses MCP github server when available, falls back to native git subprocess.
"""

import os
import logging
import subprocess
from typing import Dict, Any, Optional

logger = logging.getLogger('MultiAgentBuilder')


class GitAgent:
    """
    Agent responsible for version control operations.
    Initializes git repos, creates commits, and manages project history.
    """
    
    def __init__(self, mcp_client=None):
        """
        Initialize GitAgent.
        
        Args:
            mcp_client: Optional MCP client for github operations
        """
        self.mcp = mcp_client
        
    def run(self, task: str, project_path: str, context: dict) -> Dict[str, Any]:
        """
        Execute git operations on the project.
        
        Args:
            task: Task description (e.g., "Initialize git and commit project")
            project_path: Path to the project directory
            context: Project context including project_name, language_config, etc.
            
        Returns:
            dict: {"success": bool, "output": {...}, "error": str/None}
        """
        try:
            logger.info(f"GitAgent starting: {task}")
            
            # Check if git is already initialized
            git_dir = os.path.join(project_path, '.git')
            is_initialized = os.path.exists(git_dir)
            
            if not is_initialized:
                # Initialize repository
                init_result = self._init_repository(project_path, context)
                if not init_result["success"]:
                    return init_result
            
            # Create .gitignore if it doesn't exist
            gitignore_result = self._create_gitignore(project_path, context)
            if not gitignore_result["success"]:
                logger.warning(f".gitignore creation failed: {gitignore_result['error']}")
            
            # Commit all files
            commit_result = self._commit_all(project_path, context)
            
            return commit_result
            
        except Exception as e:
            logger.error(f"GitAgent error: {e}")
            return {
                "success": False,
                "output": {},
                "error": str(e)
            }
    
    def _init_repository(self, project_path: str, context: dict) -> Dict[str, Any]:
        """Initialize a git repository."""
        try:
            if self.mcp and self.mcp.is_available('github'):
                logger.info("Initializing git via MCP github")
                # MCP github initialization would go here
                # For now, fallthrough to native
                pass
            
            # Native git initialization
            logger.info("Initializing git via native subprocess")
            result = subprocess.run(
                ['git', 'init'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "output": {},
                    "error": f"git init failed: {result.stderr}"
                }
            
            logger.info("✓ Git repository initialized")
            return {
                "success": True,
                "output": {"initialized": True},
                "error": None
            }
            
        except FileNotFoundError:
            return {
                "success": False,
                "output": {},
                "error": "git command not found. Please install Git."
            }
        except Exception as e:
            return {
                "success": False,
                "output": {},
                "error": f"Failed to initialize git: {str(e)}"
            }
    
    def _create_gitignore(self, project_path: str, context: dict) -> Dict[str, Any]:
        """Create .gitignore file based on project language."""
        try:
            gitignore_path = os.path.join(project_path, '.gitignore')
            
            # Skip if .gitignore already exists
            if os.path.exists(gitignore_path):
                logger.debug(".gitignore already exists, skipping")
                return {"success": True, "output": {}, "error": None}
            
            # Get language-specific .gitignore template
            language_config = context.get('language_config', {})
            backend_lang = language_config.get('backend', {}).get('language', 'python').lower()
            
            gitignore_content = self._get_gitignore_template(backend_lang)
            
            # Write .gitignore
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            
            logger.info("✓ .gitignore created")
            return {"success": True, "output": {"gitignore_created": True}, "error": None}
            
        except Exception as e:
            logger.error(f"Failed to create .gitignore: {e}")
            return {
                "success": False,
                "output": {},
                "error": str(e)
            }
    
    def _get_gitignore_template(self, language: str) -> str:
        """Get .gitignore template for the given language."""
        templates = {
            'python': """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo
*.swn
.DS_Store

# Logs
*.log
builder.log

# Environment
.env
.env.local
""",
            'javascript': """# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*
.pnpm-store/

# Build
dist/
dist-ssr/
*.local

# IDE
.vscode/
.idea/
*.swp
.DS_Store

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
""",
            'java': """# Java
*.class
*.jar
*.war
*.ear
target/
.gradle/
build/

# IDE
.idea/
*.iml
.vscode/
.DS_Store

# Logs
*.log
""",
            'go': """# Go
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
vendor/
go.work

# IDE
.idea/
.vscode/
.DS_Store

# Logs
*.log
""",
        }
        
        # Default to Python template if language not found
        return templates.get(language, templates['python'])
    
    def _commit_all(self, project_path: str, context: dict) -> Dict[str, Any]:
        """Commit all files in the project."""
        try:
            project_name = context.get('project_name', 'app')
            commit_message = f"Generated project: {project_name}"
            
            if self.mcp and self.mcp.is_available('github'):
                logger.info("Committing via MCP github")
                # MCP github commit would go here
                # For now, fallthrough to native
                pass
            
            # Native git commit
            logger.info("Committing via native git")
            
            # Add all files
            add_result = subprocess.run(
                ['git', 'add', '.'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if add_result.returncode != 0:
                return {
                    "success": False,
                    "output": {},
                    "error": f"git add failed: {add_result.stderr}"
                }
            
            # Check if there are changes to commit
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if not status_result.stdout.strip():
                logger.info("No changes to commit")
                return {
                    "success": True,
                    "output": {"committed": False, "message": "No changes"},
                    "error": None
                }
            
            # Commit
            commit_result = subprocess.run(
                ['git', 'commit', '-m', commit_message],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if commit_result.returncode != 0:
                return {
                    "success": False,
                    "output": {},
                    "error": f"git commit failed: {commit_result.stderr}"
                }
            
            logger.info(f"✓ Committed: {commit_message}")
            return {
                "success": True,
                "output": {
                    "committed": True,
                    "message": commit_message
                },
                "error": None
            }
            
        except FileNotFoundError:
            return {
                "success": False,
                "output": {},
                "error": "git command not found. Please install Git."
            }
        except Exception as e:
            logger.error(f"Failed to commit: {e}")
            return {
                "success": False,
                "output": {},
                "error": str(e)
            }
