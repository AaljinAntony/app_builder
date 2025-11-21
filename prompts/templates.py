import json

class PromptTemplates:
    @staticmethod
    def agent_manager(context: dict) -> str:
        return f"""Role: Agent Manager
Task: Analyze project state, decide next agent.
Context: {json.dumps(context)}
Output (JSON ONLY):
{{"next_agent": "AgentName", "reasoning": "brief reason"}}
Rules: No work. Only delegate."""

    @staticmethod
    def language_selector(goal: str) -> str:
        return f"""Role: Language Selector
Task: Choose stack for: "{goal}"
Output (JSON ONLY):
{{"language": "lang", "framework": "framework", "reasoning": "why"}}
Rules: Standard tech. Be concise."""

    @staticmethod
    def planner(goal: str, language_config: dict) -> str:
        return f"""# Role: Planner
You are an expert software architect creating detailed implementation plans.

## Task
Create a comprehensive architecture plan for: "{goal}"

## Tech Stack
{json.dumps(language_config, indent=2)}

## Output Format (JSON ONLY)
Return a single JSON object with these exact keys:
{{
  "overview": "2-3 sentence high-level project description",
  "file_structure": "ASCII tree of all files (use ├──, └──)",
  "frontend_architecture": "Frontend design and components",
  "backend_architecture": "Server design, request flow, database schema",
  "api_endpoints": "All API endpoints with methods, requests, responses",
  "dependencies": ["dep1==version", "dep2==version"],
  "build_commands": ["command1", "command2"],
  "plan": [{{"step_id": 1, "description": "desc", "files": ["file.ext"]}}]
}}

## Critical Rules
- Include ALL 7 sections (overview through build_commands)
- File structure must be complete ASCII tree
- API endpoints: use format "POST /endpoint - description"
- Dependencies: include exact versions
- Plan steps: granular (each < 50 lines code)
"""

    @staticmethod
    def frontend_coder(task: str, context: dict) -> str:
        return f"""Role: Frontend Coder
Task: "{task}"
Context: {json.dumps(context)}
Output: Code in markdown blocks. IMPORTANT: Precede each code block with "Filename: <filename>" on a new line.
Example:
Filename: index.html
```html
...
```
Rules: 
1. Clean, semantic code. Modern practices.
2. NO PLACEHOLDERS. Write the FULL code.
3. Do not use comments like "// ... rest of code".
4. Ensure all tags are closed and syntax is correct."""

    @staticmethod
    def backend_coder(task: str, context: dict) -> str:
        return f"""Role: Backend Coder
Task: "{task}"
Context: {json.dumps(context)}
Output: Code in markdown blocks. IMPORTANT: Precede each code block with "Filename: <filename>" on a new line.
Example:
Filename: app.py
```python
...
```
Rules: 
1. Secure, efficient. Handle errors.
2. NO PLACEHOLDERS. Write the FULL code.
3. Do not use comments like "# ... implementation".
4. Ensure all imports are present."""

    @staticmethod
    def terminal_agent(task: str, context: dict) -> str:
        return f"""Role: Terminal Agent
Task: "{task}"
Context: {json.dumps(context)}
Output (JSON ONLY):
{{"commands": ["cmd1", "cmd2"], "reasoning": "why"}}
Rules: Safe commands. No interactive shells."""

    @staticmethod
    def tester(task: str, context: dict) -> str:
        return f"""Role: Tester
Task: "{task}"
Context: {json.dumps(context)}
Output: Test code in markdown blocks.
Rules: Independent tests. Cover success/failure."""

    @staticmethod
    def debugger(task: str, context: dict) -> str:
        return f"""Role: Debugger
Task: "{task}"
Context: {json.dumps(context)}
Output: Analysis + fix in markdown blocks.
Rules: Identify root cause. Verify fix."""

    @staticmethod
    def documentation_agent(task: str, context: dict) -> str:
        return f"""Role: Documentation Agent
Task: "{task}"
Context: {json.dumps(context)}
Output: Documentation in markdown.
Rules: Clear, concise. Setup + usage."""
