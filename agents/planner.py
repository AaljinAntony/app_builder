import os
import json
import re

from utils.gemini_client import generate_with_retry
from prompts.templates import PromptTemplates
from utils.logger import logger
from utils.file_ops import write_file


class Planner:
    """Creates detailed implementation plan for the project."""

    def run(self, task: str, project_path: str, context: dict) -> dict:
        """
        Generates a step-by-step implementation plan and writes PLAN.md.
        Robust against malformed JSON responses.

        Returns:
            dict: {"success": bool, "output": dict, "error": str | None}
        """
        language_config = context.get("language_config", {})
        prompt = PromptTemplates.planner(task, language_config)

        try:
            logger.info("Planner: Creating implementation plan")
            response = generate_with_retry(prompt, temperature=0.4)
            
            # Try to extract structured data
            plan_data = self._extract_plan_data(response, task)
            
            steps = plan_data.get("plan", [])
            logger.info(f"Planner: Created plan with {len(steps)} steps")

            # Build PLAN.md
            plan_md = self._build_plan_markdown(plan_data, task)
            
            # Write to current directory
            plan_path = "PLAN.md"
            ok = write_file(plan_path, plan_md)
            if not ok:
                raise RuntimeError("Failed to write PLAN.md")

            return {"success": True, "output": plan_data, "error": None}

        except Exception as e:
            logger.error(f"Planner error: {e}")
            return {"success": False, "output": {}, "error": str(e)}
    
    def _extract_plan_data(self, response: str, task: str) -> dict:
        """
        Extract plan data from response with robust error handling.
        """
        # Try JSON extraction first
        try:
            # Remove markdown code blocks
            cleaned = response.replace("```json", "").replace("```", "").strip()
            
            # Find JSON object
            start_idx = cleaned.find('{')
            end_idx = cleaned.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                json_str = cleaned[start_idx:end_idx + 1]
                # Clean control characters
                json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', json_str)
                parsed = json.loads(json_str)
                logger.info("Successfully parsed JSON response")
                return parsed
        except Exception as e:
            logger.warning(f"JSON parsing failed ({e}), using text extraction")
        
        # Fallback: Use the entire response as overview
        return {
            "plan": [{"description": f"Implement {task}"}],
            "overview": response[:500] if response else f"Build {task} application",
            "file_structure": "Project structure to be determined",
            "frontend_architecture": "Frontend to be implemented",
            "backend_architecture": "Backend to be implemented",
            "api_endpoints": "Endpoints to be defined",
            "dependencies": ["To be determined"],
            "build_commands": ["npm install", "npm start"]
        }
    
    def _build_plan_markdown(self, data: dict, task: str) -> str:
        """Build PLAN.md from extracted data."""
        overview = data.get("overview", f"Implementation plan for: {task}")
        file_structure = data.get("file_structure", "File structure to be determined")
        frontend_arch = data.get("frontend_architecture", "Frontend architecture to be designed")
        backend_arch = data.get("backend_architecture", "Backend architecture to be designed")
        api_endpoints = data.get("api_endpoints", "API endpoints to be defined")
        dependencies = data.get("dependencies", [])
        build_commands = data.get("build_commands", [])
        
        # Format dependencies
        if isinstance(dependencies, list):
            deps_str = "\n".join(f"- {dep}" for dep in dependencies)
        else:
            deps_str = str(dependencies)
        if not deps_str or deps_str == "[]":
            deps_str = "- Dependencies to be determined"
        
        # Format build commands
        if isinstance(build_commands, list):
            build_str = "\n".join(build_commands)
        else:
            build_str = str(build_commands)
        if not build_str or build_str == "[]":
            build_str = "# Build commands to be determined"
        
        plan_md = f"""# Architecture Plan

## 1. Overview
{overview}

## 2. File Structure
```
{file_structure}
```

## 3. Frontend Architecture
{frontend_arch}

## 4. Backend Architecture
{backend_arch}

## 5. API Endpoints
{api_endpoints}

## 6. Dependencies
{deps_str}

## 7. Build Commands
```bash
{build_str}
```
"""
        return plan_md
