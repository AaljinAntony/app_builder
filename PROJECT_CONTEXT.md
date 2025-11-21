# Multi-Agent App Builder - Python Implementation

 Context Document for AI-Powered Multi-Language Application Development System

Version 1.0 (Python Native)  
Date November 2025  
Status Production Ready  
Language Python 3.8+

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Directory Structure](#directory-structure)
4. [Component Details](#component-details)
5. [Workflow Execution](#workflow-execution)
6. [Data Flow](#data-flow)
7. [Agent Specifications](#agent-specifications)
8. [API Integration](#api-integration)
9. [File Operations](#file-operations)
10. [Error Handling](#error-handling)
11. [Configuration](#configuration)
12. [Usage Guide](#usage-guide)
13. [Troubleshooting](#troubleshooting)
14. [Extension Guide](#extension-guide)
15. [Comparison with n8n Version](#comparison-with-n8n-version)

---

## 1. Project Overview

### Purpose
Transform natural language project descriptions into complete, working software applications across 10+ programming languages without human intervention (except initial approval).

### Core Capabilities
- Language Selection Automatically chooses optimal programming language
- Architecture Planning Creates detailed technical specifications
- Code Generation Writes production-ready frontend and backend code
- Testing Creates and executes test suites
- Documentation Generates comprehensive README files
- Error Recovery Automatically debugs and fixes issues (3-strike system)
- Memory System Learns from past projects and errors

### Supported Languages
- Frontend HTML, CSS, JavaScript, TypeScript
- Backend Python, Node.js, Go, Java, C#, PHP, Ruby, Rust
- Databases SQLite, PostgreSQL, MongoDB (configurable)

### Key Differences from n8n Version
 Aspect  n8n Version  Python Version 
-------------------------------------
 Execution  Docker container required  Native Python on PC 
 Setup Time  1-2 hours  15-30 minutes 
 Dependencies  n8n + Docker + language runtimes  Python + pip packages 
 Debugging  Visual logs in n8n UI  Print statements, Python debugger 
 Performance  HTTP overhead between nodes  Direct function calls (faster) 
 Customization  Limited to n8n node system  Full Python code control 
 Deployment  docker-compose up  python main.py 

---

## 2. System Architecture

### High-Level Architecture
````
┌─────────────────────────────────────────────────────────────┐
│                     User Input Layer                         │
│  (Command Line  Web UI  API)                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Main Orchestrator                           │
│  (main.py - MultiAgentBuilder class)                        │
│  • Loop Management (max 50 iterations)                      │
│  • State Management (project context, errors)               │
│  • Agent Routing                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Agent Manager (CEO)                        │
│  (agentsagent_manager.py)                                  │
│  • Analyzes current project state                           │
│  • Decides next agent to call                               │
│  • Maintains workflow progression                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────┐          ┌──────────────┐
│  Specialist  │          │   Utility    │
│   Agents     │          │   Services   │
└──────────────┘          └──────────────┘
        │                         │
        ├─ Language Selector      ├─ Gemini Client
        ├─ Planner                ├─ File Operations
        ├─ Frontend Coder         ├─ Command Executor
        ├─ Backend Coder          └─ Prompt Templates
        ├─ Tester                 
        ├─ Debugger               
        ├─ Terminal Agent         
        └─ Documentation Agent    
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Output Layer                              │
│  • Generated Code Files (project)                          │
│  • Documentation (README.md, PLAN.md)                       │
│  • Test Reports (TEST_REPORT.md)                            │
│  • Knowledge Base (agency_kb)                              │
└─────────────────────────────────────────────────────────────┘
````

### Component Relationships
````
main.py (Orchestrator)
    │
    ├─→ agentsagent_manager.py (Decides next step)
    │       │
    │       ├─→ agentslanguage_selector.py
    │       ├─→ agentsplanner.py
    │       ├─→ agentsfrontend_coder.py
    │       ├─→ agentsbackend_coder.py
    │       ├─→ agentstester.py
    │       ├─→ agentsdebugger.py
    │       ├─→ agentsterminal_agent.py
    │       └─→ agentsdocumentation.py
    │
    ├─→ utilsgemini_client.py (AI API calls)
    ├─→ utilsfile_ops.py (File IO)
    ├─→ utilscommand_executor.py (Shell commands)
    └─→ promptstemplates.py (Agent prompts)
````

---

## 3. Directory Structure
````
multi-agent-builder
│
├── .env                          # API keys (KEEP SECRET!)
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── main.py                       # Entry point
├── PROJECT_CONTEXT.md            # This file
├── README.md                     # User documentation
├── builder.log                   # Execution logs
│
├── agents                       # AI Agent implementations
│   ├── __init__.py
│   ├── agent_manager.py          # CEO - orchestrates all agents
│   ├── language_selector.py      # Selects best programming language
│   ├── planner.py                # Creates PLAN.md
│   ├── frontend_coder.py         # Writes HTMLCSSJS
│   ├── backend_coder.py          # Writes server code
│   ├── tester.py                 # Creates test reports
│   ├── debugger.py               # Fixes errors
│   ├── terminal_agent.py         # Runs shell commands
│   └── documentation.py          # Writes README.md
│
├── utils                        # Utility modules
│   ├── __init__.py
│   ├── gemini_client.py          # Google Gemini API wrapper
│   ├── file_ops.py               # File readwrite operations
│   ├── command_executor.py       # Shell command execution
│   └── logger.py                 # Logging configuration
│
├── prompts                      # AI Prompt templates
│   ├── __init__.py
│   └── templates.py              # All agent prompts
│
├── project                      # Generated projects
│   ├── calculator-app
│   │   ├── app.py
│   │   ├── index.html
│   │   ├── styles.css
│   │   ├── script.js
│   │   ├── PLAN.md
│   │   ├── TEST_REPORT.md
│   │   └── README.md
│   │
│   └── todo-list
│       └── ...
│
├── agency_kb                    # Long-term memory
│   ├── debug_log.md              # Error solutions learned
│   ├── project_summaries.md      # Past project summaries
│   └── last_action.txt           # Most recent action
│
├── tests                        # Unit tests
│   ├── test_system.py
│   ├── test_agents.py
│   └── test_utils.py
│
└── venv                         # Virtual environment (not in git)
    └── ...
````

---

## 4. Component Details

### 4.1 Main Orchestrator (`main.py`)

Purpose Central control loop that manages the entire workflow.

Key Class `MultiAgentBuilder`

Properties
````python
self.project_name str          # Sanitized project name
self.project_path str          # Full path to project folder
self.goal str                  # User's project description
self.language_config dict      # Selected languages
self.agent_manager AgentManager # CEO agent instance
self.loop_counter int          # Current iteration
self.max_loops int = 50        # Safety limit
self.error_count int           # Consecutive errors
self.max_errors int = 3        # Error threshold
````

Key Methods
- `start(user_prompt)` - Initialize and begin workflow
- `_run_agent_loop()` - Main execution loop
- `_execute_agent(agent_name, task)` - Route to specific agent
- `_get_project_context()` - Gather current state

Workflow States
1. Initialization - Parse user input, create project folder
2. Loop Execution - Repeatedly call Agent Manager
3. Agent Routing - Execute decided agent
4. State Update - Update context for next iteration
5. Termination - FINISHED agent or error limit reached

---

### 4.2 Agent Manager (`agentsagent_manager.py`)

Purpose The CEO - analyzes context and decides next agent.

Decision Logic
````
IF no language selected
    → Call LanguageSelector

ELSE IF no PLAN.md exists
    → Call Planner (ONLY ONCE)

ELSE IF frontend files missing
    → Call FrontendCoder

ELSE IF backend file missing
    → Call BackendCoder

ELSE IF dependencies not installed
    → Call TerminalAgent (pip install  npm install)

ELSE IF no TEST_REPORT.md
    → Call Tester

ELSE IF tests failed
    → Call Debugger

ELSE IF no README.md
    → Call DocumentationAgent

ELSE
    → Call FINISHED
````

Anti-Loop Protection
- Checks `last_action` to prevent calling same agent twice
- Forces linear progression through workflow phases
- Validates file existence before agent calls

---

### 4.3 Specialist Agents

#### Language Selector (`agentslanguage_selector.py`)
Input Project description  
Output JSON with selected languages
````json
{
  frontend {
    language JavaScript,
    reasoning Browser-based interactivity
  },
  backend {
    language Python,
    framework Flask,
    reasoning Rapid development, extensive libraries
  },
  database SQLite,
  justification Overall reasoning
}
````

Selection Criteria
- CalculatorCRUD → Python (Flask) or Node.js
- Real-time apps → Node.js
- High performance → Go, Rust
- Enterprise → Java, C#
- Quick prototype → Python, Ruby

---

#### Planner (`agentsplanner.py`)
Input Project goal, selected languages  
Output PLAN.md file

PLAN.md Structure
````markdown
# Architecture Plan

## 1. Overview
[High-level description]

## 2. File Structure
project
├── index.html
├── app.py
└── README.md

## 3. Frontend Architecture
[HTMLCSSJS design]

## 4. Backend Architecture
[Server design, API endpoints]

## 5. API Endpoints
POST calculate
  Request {expression 2+2}
  Response {result 4}

## 6. Dependencies
- flask==3.0.0
- flask-cors==4.0.0

## 7. Build Commands
pip install -r requirements.txt
python app.py
````

---

#### Frontend Coder (`agentsfrontend_coder.py`)
Input Coding task, project path  
Output HTMLCSSJavaScript files

Code Requirements
- Modern HTML5 structure
- Responsive CSS (mobile-friendly)
- fetch() API calls to backend
- Error handling and loading states
- User-friendly error messages

Example Output
````javascript
 script.js
const API_URL = 'httplocalhost5000';

document.getElementById('calculate-btn').addEventListener('click', async () = {
    const expression = document.getElementById('expression').value;
    
    try {
        const response = await fetch(`${API_URL}calculate`, {
            method 'POST',
            headers {'Content-Type' 'applicationjson'},
            body JSON.stringify({expression})
        });
        
        const data = await response.json();
        document.getElementById('result').textContent = data.result;
    } catch (error) {
        document.getElementById('result').textContent = `Error ${error.message}`;
    }
});
````

---

#### Backend Coder (`agentsbackend_coder.py`)
Input Task, language, framework  
Output Server code file

Code Requirements
- CORS enabled for browser access
- Input validation on all endpoints
- Comprehensive error handling
- JSON responses with proper status codes
- Security best practices (no eval, SQL injection prevention)

Example Output (PythonFlask)
````python
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('calculate', methods=['POST'])
def calculate()
    try
        data = request.get_json()
        expression = data.get('expression', '')
        
        # Validate
        if not expression
            return jsonify({'error' 'No expression provided'}), 400
        
        # Process (safe evaluation)
        result = safe_eval(expression)
        
        return jsonify({'result' result, 'success' True}), 200
    
    except Exception as e
        return jsonify({'error' str(e)}), 500

if __name__ == '__main__'
    app.run(host='0.0.0.0', port=5000)
````

---

#### Terminal Agent (`agentsterminal_agent.py`)
Input Command task  
Output Executed command result

Capabilities
- Install packages `pip install`, `npm install`, `cargo install`, etc.
- Run compilers `python`, `node`, `go build`, `javac`, etc.
- Start servers
- Run tests

Safety Features
- 5-minute timeout per command
- Working directory isolation
- Captures stdout and stderr
- Returns successfailure status

---

#### Tester (`agentstester.py`)
Input Testing task, backend language  
Output TEST_REPORT.md

Test Report Structure
````markdown
# Test Report

## Environment
- Backend Python (Flask)
- Server httplocalhost5000

## API Endpoint Tests

### Test 1 POST calculate (Valid Input)
Command
```bash
curl -X POST httplocalhost5000calculate 
  -H Content-Type applicationjson 
  -d '{expression 2+2}'
```
Expected {result 4, success true}
Actual {result 4, success true}
Status ✅ PASS

### Test 2 POST calculate (Invalid Input)
Command
```bash
curl -X POST httplocalhost5000calculate 
  -H Content-Type applicationjson 
  -d '{expression }'
```
Expected {error No expression provided}
Status ✅ PASS

## Overall Result ✅ ALL TESTS PASSED (22)
````

---

#### Debugger (`agentsdebugger.py`)
Input Error message, task  
Output Fixed code OR dependency install command

Error Patterns Recognized
- `ModuleNotFoundError` → Install package
- `SyntaxError` → Fix syntax
- `NameError` → Define variable
- `TypeError` → Type conversion
- `IndentationError` → Fix indentation

3-Strike System
1. Strike 1 Debugger attempts fix
2. Strike 2 Debugger tries alternative fix
3. Strike 3 Researcher called (Google search for solution)

---

#### Documentation Agent (`agentsdocumentation.py`)
Input Project goal, languages  
Output README.md

README Sections
1. Project title and description
2. Features list
3. Tech stack
4. Prerequisites
5. Installation steps (language-specific)
6. Usage instructions
7. API documentation
8. Troubleshooting
9. Contributing guidelines

---

### 4.4 Utility Services

#### Gemini Client (`utilsgemini_client.py`)

Purpose Wrapper for Google Gemini API

Key Methods
````python
generate(prompt, temperature, max_tokens) → str
extract_json(text) → dict
generate_with_retry(prompt, max_retries) → str
````

JSON Extraction Logic
1. Remove markdown code blocks (```json```)
2. Strip whitespace
3. Try parsing
4. If fails, extract content between `{` and `}`
5. Fallback error handling

---

#### File Operations (`utilsfile_ops.py`)

Purpose All file IO operations

Key Methods
````python
write_file(filepath, content) → bool
read_file(filepath) → str
list_files(directory) → list
file_exists(filepath) → bool
append_to_knowledge_base(filename, content) → None
````

Safety Features
- Creates directories automatically
- UTF-8 encoding for all files
- Error handling with informative messages
- Relative path resolution

---

#### Command Executor (`utilscommand_executor.py`)

Purpose Execute shell commands safely

Key Method
````python
execute(command, cwd) → dict {
    'success' bool,
    'stdout' str,
    'stderr' str,
    'exit_code' int
}
````

Safety Features
- 5-minute timeout
- Working directory isolation
- Captures all output
- No shell injection vulnerabilities

---

## 5. Workflow Execution

### Complete Execution Flow
````
User Input Build me a calculator app
    ↓
┌──────────────────────────────────────┐
│ LOOP 1 Agent Manager Decision      │
├──────────────────────────────────────┤
│ Context No files yet                │
│ Decision Call LanguageSelector      │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ LanguageSelector Executes            │
├──────────────────────────────────────┤
│ Analysis Calculator needs           │
│   - Frontend JavaScript (UI)        │
│   - Backend Python (calculations)   │
│ Output Language config stored       │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ LOOP 2 Agent Manager Decision      │
├──────────────────────────────────────┤
│ Context Languages selected          │
│ Decision Call Planner               │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ Planner Executes                     │
├──────────────────────────────────────┤
│ Creates PLAN.md                     │
│   - Architecture overview            │
│   - File structure                   │
│   - API design                       │
│   - Dependencies                     │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ LOOP 3 Agent Manager Decision      │
├──────────────────────────────────────┤
│ Context PLAN.md exists              │
│ Decision Call FrontendCoder         │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ FrontendCoder Executes               │
├──────────────────────────────────────┤
│ Creates index.html                  │
│   - Calculator UI                    │
│   - Input field + buttons            │
│   - Result display                   │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ LOOP 4 FrontendCoder again          │
├──────────────────────────────────────┤
│ Creates styles.css                  │
│   - Modern, responsive design        │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ LOOP 5 FrontendCoder again          │
├──────────────────────────────────────┤
│ Creates script.js                   │
│   - fetch() calls to backend         │
│   - Error handling                   │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ LOOP 6 Agent Manager Decision      │
├──────────────────────────────────────┤
│ Context Frontend complete           │
│ Decision Call BackendCoder          │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ BackendCoder Executes                │
├──────────────────────────────────────┤
│ Creates app.py                      │
│   - Flask server                     │
│   - calculate endpoint              │
│   - CORS enabled                     │
│   - Input validation                 │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ LOOP 7 Agent Manager Decision      │
├──────────────────────────────────────┤
│ Context Code written                │
│ Decision Call TerminalAgent         │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ TerminalAgent Executes               │
├──────────────────────────────────────┤
│ Command pip install flask flask-cors│
│ Result ✅ Dependencies installed    │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ LOOP 8 Agent Manager Decision      │
├──────────────────────────────────────┤
│ Context Dependencies ready          │
│ Decision Call Tester                │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ Tester Executes                      │
├──────────────────────────────────────┤
│ Creates TEST_REPORT.md              │
│   - API endpoint tests               │
│   - curl commands                    │
│   - Expected results                 │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ LOOP 9 Agent Manager Decision      │
├──────────────────────────────────────┤
│ Context Tests documented            │
│ Decision Call DocumentationAgent    │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ DocumentationAgent Executes          │
├──────────────────────────────────────┤
│ Creates README.md                   │
│   - Installation guide               │
│   - Usage instructions               │
│   - API documentation                │
└───────────────┬──────────────────────┘
                ↓
┌──────────────────────────────────────┐
│ LOOP 10 Agent Manager Decision     │
├──────────────────────────────────────┤
│ Context All files present           │
│ Decision FINISHED                   │
└───────────────┬──────────────────────┘
                ↓
            🎉 COMPLETE!
            
Output Files
  projectcalculator-app
  ├── PLAN.md
  ├── index.html
  ├── styles.css
  ├── script.js
  ├── app.py
  ├── TEST_REPORT.md
  └── README.md
````

---

## 6. Data Flow

### State Management

Loop State Variables
````python
{
    'loop_counter' int,          # Current iteration (0-50)
    'error_count' int,           # Consecutive errors (0-3)
    'project_name' str,          # calculator-app
    'project_path' str,          # projectcalculator-app
    'goal' str,                  # Original user prompt
    'language_config' dict,      # Selected languages
    'last_action' str,           # Planner completed ...
    'last_error' str             # Most recent error message
}
````

### Agent InputOutput Format

All agents receive
````python
{
    'task' str,              # Specific instruction from Agent Manager
    'project_path' str,      # Where to save files
    'context' dict           # Additional context (languages, errors, etc.)
}
````

All agents return
````python
{
    'success' bool,          # Did the agent succeed
    'output' dict,           # Agent-specific output (varies)
    'error' str              # Error message if failed (optional)
}
````

---

## 7. Agent Specifications

### Agent Communication Protocol

All agents follow this pattern

1. Receive Task from Agent Manager
2. Create Prompt using template
3. Call Gemini API with prompt
4. Parse JSON Response
5. Execute Action (write file, run command, etc.)
6. Return Result to orchestrator

### Prompt Template Pattern
````python
def create_prompt(task, context)
    
    Standard prompt structure
    
    # Role [Agent Name]
    [Role description]
    
    ## Task
    [Specific task from Agent Manager]
    
    ## Context
    [Project state, files, errors, etc.]
    
    ## Instructions
    [What the agent should do]
    
    ## Output Format (JSON ONLY)
    {
      key value
    }
    
    ## Examples
    [2-3 concrete examples]
    
    ## Critical Rules
    - Rule 1
    - Rule 2
    
    return prompt
````

---

## 8. API Integration

### Google Gemini API

Model `gemini-2.5-flash`

Configuration
````python
{
    'temperature' 0.7,              # Creativity (0.0=deterministic, 1.0=creative)
'max_output_tokens': 4096,  # Response length limit
'top_p': 0.95,              # Nucleus sampling
'top_k': 40                 # Top-k sampling
}

**Rate Limits (Free Tier):**
- 60 requests per minute
- 1,500 requests per day
- ~1 million tokens per day

**Cost Estimation:**
Typical Project Token Usage:

Language Selection: ~500 tokens
Planning: ~2,000 tokens
Frontend Coding (3 files): ~6,000 tokens
Backend Coding: ~3,000 tokens
Testing: ~1,500 tokens
Documentation: ~2,000 tokens

Total: ~15,000 tokens per project
Daily Free Limit: ~66 projects per day

**Error Handling:**
````python
try:
    response = gemini.generate(prompt)
except google.api_core.exceptions.ResourceExhausted:
    # Rate limit hit
    time.sleep(60)  # Wait 1 minute
    response = gemini.generate(prompt)

except google.api_core.exceptions.InvalidArgument:
    # Prompt too long or invalid
    # Shorten prompt and retry
    
except Exception as e:
    # General error
    logger.error(f"Gemini API error: {e}")
    raise
````

---

## 9. File Operations

### File System Layout

**Base Paths:**
````python
BASE_PATH = "project/"              # Generated projects
KB_PATH = "agency_kb/"              # Long-term memory
LOGS_PATH = "./"                    # Log files
````

**File Naming Convention:**
project/
{project-name}/              # Lowercase, hyphens
PLAN.md                    # ALL CAPS for docs
README.md                  # ALL CAPS for docs
TEST_REPORT.md             # ALL CAPS for docs
{filename}.{ext}           # Code files lowercase

### File Templates

**Python Flask App:**
````python
# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/endpoint', methods=['POST'])
def endpoint():
    try:
        data = request.get_json()
        # Process data
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
````

**Frontend HTML:**
````html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Name</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <!-- UI elements -->
    </div>
    <script src="script.js"></script>
</body>
</html>
````

---

## 10. Error Handling

### Error Categories

**1. API Errors (Gemini):**
````python
try:
    response = gemini.generate(prompt)
except google.api_core.exceptions.ResourceExhausted:
    # Rate limit - wait and retry
    handle_rate_limit()
except google.api_core.exceptions.InvalidArgument:
    # Bad prompt - fix and retry
    handle_invalid_prompt()
````

**2. JSON Parsing Errors:**
````python
try:
    data = json.loads(response)
except json.JSONDecodeError:
    # Extract JSON from markdown
    data = extract_json_from_markdown(response)
````

**3. File System Errors:**
````python
try:
    file_ops.write_file(path, content)
except PermissionError:
    # No write permission
    logger.error(f"Cannot write to {path}")
except OSError as e:
    # Disk full, path too long, etc.
    logger.error(f"File system error: {e}")
````

**4. Command Execution Errors:**
````python
result = cmd_executor.execute(command)
if not result['success']:
    if 'ModuleNotFoundError' in result['stderr']:
        # Missing dependency
        install_dependency()
    elif 'SyntaxError' in result['stderr']:
        # Code syntax error
        call_debugger()
````

### 3-Strike Debug System
````python
# In main orchestrator
if not success:
    self.error_count += 1
    
    if self.error_count == 1:
        # Strike 1: Call Debugger
        self._execute_agent('Debugger', task)
    
    elif self.error_count == 2:
        # Strike 2: Call Debugger again
        self._execute_agent('Debugger', task)
    
    elif self.error_count >= 3:
        # Strike 3: Call Researcher (Google search)
        self._execute_agent('Researcher', task)
        self.error_count = 0  # Reset
else:
    self.error_count = 0  # Success - reset counter
````

---

## 11. Configuration

### Environment Variables (`.env`)
````bash
# Required
GEMINI_API_KEY=AIzaSyC_your_actual_key_here

# Optional
GOOGLE_SEARCH_API_KEY=your_search_key_here
GOOGLE_SEARCH_ENGINE_ID=your_engine_id_here

# System Configuration
MAX_LOOPS=50
MAX_ERRORS=3
DEFAULT_TEMPERATURE=0.7
MAX_TOKENS=4096

# File Paths
PROJECT_BASE_PATH=project/
KB_PATH=agency_kb/

# Logging
LOG_LEVEL=INFO
LOG_FILE=builder.log
````

### Loading Configuration
````python
# In main.py or any module
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MAX_LOOPS = int(os.getenv('MAX_LOOPS', '50'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
````

---

## 12. Usage Guide

### Basic Usage

**Command Line:**
````bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Run builder
python main.py build me a calculator app

# Or interactive mode
python main.py
# Then enter your prompt when asked
````

**Programmatic Usage:**
````python
from main import MultiAgentBuilder

builder = MultiAgentBuilder()
builder.start("Build me a todo list app")

# Check result
print(f"Project created at: {builder.project_path}")
````

### Advanced Usage

**Custom Configuration:**
````python
from main import MultiAgentBuilder

builder = MultiAgentBuilder()
builder.max_loops = 100  # Increase loop limit
builder.max_errors = 5   # More error tolerance

builder.start("Build a complex e-commerce platform")
````

**With Web UI:**
````bash
python web_ui.py
# Open browser: http://localhost:5000
````

---

## 13. Troubleshooting

### Common Issues and Solutions

#### Issue 1: "GEMINI_API_KEY not found"

**Symptoms:**
ValueError: GEMINI_API_KEY not found in .env file!

**Solutions:**
````bash
# Check .env file exists
ls -la .env

# Check content
cat .env

# Verify key format
echo $GEMINI_API_KEY  # Should show: AIzaSyC...

# Create if missing
echo "GEMINI_API_KEY=your_key_here" > .env
````

---

#### Issue 2: "No module named 'google.generativeai'"

**Symptoms:**
ModuleNotFoundError: No module named 'google.generativeai'

**Solutions:**
````bash
# Ensure virtual environment is active
which python  # Should show venv path

# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install google-generativeai
````

---

#### Issue 3: JSON Parsing Errors

**Symptoms:**
JSONDecodeError: Expecting property name enclosed in double quotes

**Root Cause:** Gemini sometimes wraps JSON in markdown

**Solution (already implemented in code):**
````python
def extract_json(text):
    # Remove markdown code blocks
    text = text.replace('```json', '').replace('```', '')
    
    # Try parsing
    try:
        return json.loads(text)
    except:
        # Fallback: extract between { }
        start = text.find('{')
        end = text.rfind('}') + 1
        return json.loads(text[start:end])
````

---

#### Issue 4: Agent Gets Stuck in Loop

**Symptoms:**
Agent Manager keeps calling Planner
Loop 10: Calling Planner
Loop 11: Calling Planner
...

**Root Cause:** Agent Manager not detecting PLAN.md exists

**Solution:**
````python
# Verify file operations work
from utils.file_ops import file_ops

# Test write
file_ops.write_file("test-project/test.txt", "Hello")

# Test read
content = file_ops.read_file("test-project/test.txt")
print(content)  # Should print "Hello"

# Test exists
exists = file_ops.file_exists("test-project/test.txt")
print(exists)  # Should print True
````

**Fix in Agent Manager prompt:**
- Ensure "Check if PLAN.md exists" logic is clear
- Add explicit file listing in context

---

#### Issue 5: Commands Fail with Permission Errors

**Symptoms:**
PermissionError: [Errno 13] Permission denied: 'project/app.py'

**Solutions:**
````bash
# Check file permissions
ls -la project/

# Fix permissions
chmod -R u+w project/

# On Windows, run as Administrator
# Right-click terminal → "Run as Administrator"
````

---

#### Issue 6: Virtual Environment Not Activating

**Symptoms:**
````bash
$ source venv/bin/activate
bash: venv/bin/activate: No such file or directory
````

**Solutions:**
````bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv

# Windows: Use backslashes
venv\Scripts\activate

# Mac with zsh: Use correct path
source venv/bin/activate
````

---

## 14. Extension Guide

### Adding a New Agent

**Step 1: Create Agent File**
````python
# agents/code_optimizer.py

from utils.gemini_client import gemini
from utils.file_ops import file_ops
from prompts.templates import prompts

class CodeOptimizer:
    """Optimizes generated code for performance"""
    
    def optimize(self, project_path):
        """
        Optimize all code files
        
        Args:
            project_path (str): Project directory
        
        Returns:
            bool: True if successful
        """
        try:
            print("\n🚀 CODE OPTIMIZER ANALYZING...")
            
            # Read all code files
            files = file_ops.list_files(project_path)
            
            for filename in files:
                if filename.endswith(('.py', '.js', '.go')):
                    content = file_ops.read_file(f"{project_path}/{filename}")
                    
                    # Create optimization prompt
                    prompt = f"""Optimize this code for performance:

File: {filename}
````
{content}
Return optimized code in JSON:
{{
"filename": "{project_path}/{filename}",
"content": "optimized code here"
}}
"""
                # Get optimized version
                response = gemini.generate(prompt, temperature=0.3)
                data = gemini.extract_json(response)
                
                # Write optimized code
                file_ops.write_file(
                    filepath=data['filename'],
                    content=data['content']
                )
                
                print(f"✅ Optimized: {filename}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error in Code Optimizer: {e}")
        return False
Create instance
code_optimizer = CodeOptimizer()

---

**Step 2: Add Prompt Template**
````python
# In prompts/templates.py

@staticmethod
def code_optimizer(code_content, filename, language):
    return f"""# Role: Code Optimizer

You are an expert at optimizing code for performance and efficiency.

## Code to Optimize:
**File:** {filename}
**Language:** {language}
````
{code_content}
Optimization Goals:

Reduce time complexity
Minimize memory usage
Remove redundant operations
Use efficient data structures
Apply language-specific optimizations

Output Format (JSON ONLY):
{{
"filename": "{filename}",
"content": "optimized code",
"improvements": ["improvement 1", "improvement 2"],
"performance_gain": "estimated % improvement"
}}
Keep the same functionality - only optimize, don't change behavior.
"""

---

**Step 3: Register in Agent Manager**
````python
# In agents/agent_manager.py

# Add to available agents list in prompt
## Available Agents:
- Planner
- FrontendCoder
- BackendCoder
- CodeOptimizer  # ← ADD THIS
- Tester
- DocumentationAgent
- FINISHED

# Add to decision logic
ELSE IF code written but not optimized:
    → Call CodeOptimizer
````

---

**Step 4: Add to Orchestrator**
````python
# In main.py

from agents.code_optimizer import code_optimizer

# In _execute_agent method, add:
elif agent_name == "CodeOptimizer":
    return self._run_code_optimizer(task)

# Add method:
def _run_code_optimizer(self, task):
    """Run Code Optimizer"""
    return code_optimizer.optimize(self.project_name)
````

---

### Adding a New Language

**Example: Adding Kotlin Support**

**Step 1: Update Language Selector**
````python
# In prompts/templates.py - language_selector prompt

## Available Languages:
...
- **Kotlin**: Android apps, backend (Ktor), multiplatform

## Selection Criteria:
...
- Android app → Kotlin or Java
````

---

**Step 2: Update Backend Coder**
````python
# In agents/backend_coder.py

# Add Kotlin template to prompt
elif language == "Kotlin":
    template = """
    import io.ktor.server.application.*
    import io.ktor.server.engine.*
    import io.ktor.server.netty.*
    import io.ktor.server.response.*
    import io.ktor.server.routing.*
    
    fun main() {
        embeddedServer(Netty, port = 8080) {
            routing {
                post("/calculate") {
                    // Handle request
                }
            }
        }.start(wait = true)
    }
    """
````

---

**Step 3: Update Terminal Agent**
````python
# In prompts/templates.py - terminal_agent prompt

## Language-Specific Commands:

**Kotlin:**
- Install: `sdk install kotlin`
- Compile: `kotlinc main.kt -include-runtime -d app.jar`
- Run: `java -jar app.jar`
- Dependencies: Use Gradle or Maven
````

---

**Step 4: Update Documentation**
````python
# In prompts/templates.py - documentation_agent prompt

**Kotlin:**
```bash
# Install Kotlin
sdk install kotlin

# Run application
java -jar app.jar
```
````

---

### Adding Error Recovery Patterns

**Example: Handle New Error Type**
````python
# In agents/debugger.py

# Add to error patterns
ERROR_PATTERNS = {
    'ModuleNotFoundError': 'pip install {module}',
    'SyntaxError': 'fix_syntax',
    'NameError': 'define_variable',
    'ConnectionRefusedError': 'start_server',  # ← NEW
    'PortAlreadyInUse': 'change_port',         # ← NEW
}

def fix_port_error(self, error_message, project_path):
    """Fix port already in use error"""
    
    # Extract port from error
    port_match = re.search(r'port (\d+)', error_message)
    old_port = port_match.group(1) if port_match else '5000'
    
    # Choose new port
    new_port = str(int(old_port) + 1)
    
    # Read server file
    content = file_ops.read_file(f"{project_path}/app.py")
    
    # Replace port
    new_content = content.replace(
        f"port={old_port}",
        f"port={new_port}"
    )
    
    # Write back
    file_ops.write_file(f"{project_path}/app.py", new_content)
    
    print(f"✅ Changed port from {old_port} to {new_port}")
````

---

## 15. Comparison with n8n Version

### Feature Comparison

| Feature | n8n Workflow | Python Implementation |
|---------|--------------|----------------------|
| **Setup Complexity** | High (Docker, n8n, containers) | Low (pip install) |
| **Installation Time** | 1-2 hours | 15-30 minutes |
| **Dependencies** | Docker, n8n, language runtimes | Python 3.8+, pip packages |
| **Disk Space** | 2-5 GB | 500 MB |
| **RAM Usage** | 1-2 GB | 200-500 MB |
| **Execution Speed** | Slower (HTTP overhead) | Faster (native calls) |
| **Debugging** | n8n UI logs | Python debugger, print() |
| **Customization** | Limited (node constraints) | Full (Python code) |
| **Visual Workflow** | ✅ Yes (drag-drop) | ❌ No (code-based) |
| **Learning Curve** | Low (visual) | Medium (Python basics) |
| **Version Control** | JSON export | Git-friendly files |
| **Deployment** | Docker Compose | Single Python command |
| **Cloud Deployment** | Need container hosting | Works on any Python host |
| **Cost** | Free (self-hosted) | Free |
| **Scalability** | Limited by Docker | Native OS performance |
| **Multi-user** | Requires setup | Add Flask auth |
| **API Access** | n8n API | Easy (Flask routes) |
| **Extensibility** | Add n8n nodes | Add Python modules |
| **Error Recovery** | Visual error nodes | Try-except blocks |
| **Testing** | Manual in UI | Automated unit tests |
| **Documentation** | n8n docs + custom | Inline docstrings |

---

### Code Equivalent Comparison

**n8n Node (Agent Manager):**
````json
{
  "parameters": {
    "promptType": "define",
    "text": "={{ $json.prompt_text }}"
  },
  "type": "@n8n/n8n-nodes-langchain.agent",
  "name": "Agent Manager"
}
````

**Python Equivalent:**
````python
class AgentManager:
    def decide_next_agent(self, context):
        prompt = prompts.agent_manager(context)
        response = gemini.generate(prompt)
        return gemini.extract_json(response)
````

---

**n8n File Write:**
````json
{
  "parameters": {
    "command": "cat << 'EOF' > {{ $json.filename }}\n{{ $json.content }}\nEOF"
  },
  "type": "n8n-nodes-base.executeCommand",
  "name": "Write File"
}
````

**Python Equivalent:**
````python
def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
````

---

### Migration Benefits

**From n8n to Python:**

✅ **Simpler Deployment**
````bash
# n8n
docker-compose build
docker-compose up -d
# Configure credentials in UI
# Import workflow JSON
# Connect nodes manually

# Python
pip install -r requirements.txt
echo "GEMINI_API_KEY=xxx" > .env
python main.py
````

✅ **Better Debugging**
````python
# Add anywhere in code
print(f"🐛 DEBUG: {variable}")
import pdb; pdb.set_trace()  # Breakpoint
````

✅ **Easier Testing**
````python
# Unit tests
import unittest

class TestAgent(unittest.TestCase):
    def test_planner(self):
        result = planner.create_plan(...)
        self.assertTrue(result)
````

✅ **Version Control**
````bash
git add agents/
git commit -m "Added code optimizer agent"
git push
````

---

### When to Use Each

**Use n8n if:**
- You prefer visual workflows
- You need to integrate many services (Slack, Email, etc.)
- You have no programming experience
- You want quick prototyping with drag-drop

**Use Python if:**
- You want better performance
- You need custom logic
- You prefer code over UI
- You want to learn Python
- You need version control
- You want automated testing
- You're deploying to cloud without Docker

---

## 16. Performance Optimization

### Execution Time Analysis

**Typical Project Timeline:**
Activity                  Time        Bottleneck
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Language Selection        5-10s       Gemini API call
Planning                  10-15s      Gemini API call
Frontend Coding (3 files) 30-45s      3× Gemini API calls
Backend Coding            15-20s      Gemini API call
Dependency Installation   10-30s      Network download
Testing                   10-15s      Gemini API call
Documentation             10-15s      Gemini API call
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total                     100-150s    (1.5-2.5 minutes)

### Optimization Techniques

**1. Response Caching:**
````python
# Cache Gemini responses
import hashlib

cache = {}

def generate_cached(prompt):
    key = hashlib.md5(prompt.encode()).hexdigest()
    
    if key in cache:
        return cache[key]
    
    response = gemini.generate(prompt)
    cache[key] = response
    return response
````

**2. Parallel Agent Execution:**
````python
# Run independent agents in parallel
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    future1 = executor.submit(frontend_coder.write_code, task1)
    future2 = executor.submit(backend_coder.write_code, task2)
    future3 = executor.submit(tester.create_tests, task3)
    
    results = [f.result() for f in [future1, future2, future3]]
````

**3. Reduce Token Usage:**
````python
# Shorter prompts = faster responses
def create_minimal_prompt(task):
    return f"""Role: {agent_name}
Task: {task}
Output JSON: {{"filename": "...", "content": "..."}}
"""
````

---

## 17. Security Considerations

### API Key Protection

**❌ NEVER:**
````python
# Don't hardcode keys
GEMINI_API_KEY = "AIzaSyC..."  # BAD!

# Don't commit .env
git add .env  # BAD!
````

**✅ ALWAYS:**
````python
# Use environment variables
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Add .env to .gitignore
echo ".env" >> .gitignore
````

---

### Code Execution Safety

**Dangerous:**
````python
# Never execute arbitrary code
eval(user_input)  # UNSAFE!
exec(ai_generated_code)  # UNSAFE!
os.system(user_command)  # UNSAFE!
````

**Safe:**
````python
# Use subprocess with arguments
import subprocess

subprocess.run(
    ['python', 'app.py'],  # Command as list
    check=True,
    timeout=300  # 5 minute limit
)
````

---

### Input Validation
````python
def validate_project_name(name):
    """Ensure safe project names"""
    
    # Allow only alphanumeric and hyphens
    if not re.match(r'^[a-z0-9-]+$', name):
        raise ValueError("Invalid project name")
    
    # Prevent directory traversal
    if '..' in name or '/' in name:
        raise ValueError("Invalid characters in project name")
    
    return name
````

---

## 18. Monitoring and Logging

### Logging Configuration
````python
# utils/logger.py

import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('builder.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('MultiAgentBuilder')

# Usage in agents
logger.info("Starting agent...")
logger.warning("Potential issue detected")
logger.error("Agent failed", exc_info=True)
````

---

### Metrics Collection
````python
# Track execution metrics
class MetricsCollector:
    def __init__(self):
        self.metrics = {
            'total_projects': 0,
            'successful_projects': 0,
            'failed_projects': 0,
            'avg_execution_time': 0,
            'total_api_calls': 0,
            'total_tokens_used': 0
        }
    
    def record_project(self, success, execution_time, api_calls):
        self.metrics['total_projects'] += 1
        
        if success:
            self.metrics['successful_projects'] += 1
        else:
            self.metrics['failed_projects'] += 1
        
        self.metrics['total_api_calls'] += api_calls
        
        # Update average
        n = self.metrics['total_projects']
        self.metrics['avg_execution_time'] = (
            (self.metrics['avg_execution_time'] * (n-1) + execution_time) / n
        )
    
    def get_report(self):
        success_rate = (
            self.metrics['successful_projects'] / 
            self.metrics['total_projects'] * 100
        )
        
        return f"""
        Metrics Report:
        ━━━━━━━━━━━━━━━━
        Total Projects: {self.metrics['total_projects']}
        Success Rate: {success_rate:.1f}%
        Avg Time: {self.metrics['avg_execution_time']:.1f}s
        Total API Calls: {self.metrics['total_api_calls']}
        """
````

---

## 19. Best Practices

### Code Organization

✅ **DO:**
- One class per file
- Clear file/function names
- Docstrings for all functions
- Type hints where helpful

❌ **DON'T:**
- Put everything in main.py
- Use vague names like `data`, `temp`
- Skip error handling
- Ignore PEP 8 style guide

---

### Prompt Engineering

✅ **Effective Prompts:**
````python
"""
# Role: Backend Coder

You are an expert Python developer.

## Task:
Create a Flask API with /calculate endpoint.

## Requirements:
- CORS enabled
- Input validation
- Error handling
- JSON responses

## Output (JSON ONLY):
{
  "filename": "app.py",
  "content": "complete code here"
}

## Example:
{
  "filename": "app.py",
  "content": "from flask import Flask..."
}
"""
````

❌ **Ineffective Prompts:**
````python
"Write code for a calculator"  # Too vague
````

---

### Error Recovery

✅ **Robust Error Handling:**
````python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Specific error: {e}")
    fallback_operation()
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise
````

❌ **Fragile Code:**
````python
result = risky_operation()  # No error handling
````

---

## 20. Future Enhancements

### Planned Features

**Phase 1 (Near-term):**
- [ ] Web UI with progress bars
- [ ] Real-time log streaming
- [ ] Project templates library
- [ ] One-click deployment to cloud

**Phase 2 (Medium-term):**
- [ ] Multi-user support with authentication
- [ ] Project version control integration
- [ ] Automated testing execution
- [ ] Performance profiling

**Phase 3 (Long-term):**
- [ ] Visual workflow editor (like n8n)
- [ ] Plugin system for custom agents
- [ ] Multi-language code translation
- [ ] AI pair programming mode

---

## Conclusion

This Python implementation provides a **simpler, faster, and more maintainable** alternative to the n8n workflow while preserving all core functionality.

**Key Advantages:**
1. **No Docker required** - runs natively on your PC
2. **Faster execution** - direct Python calls vs HTTP
3. **Easier debugging** - standard Python tools
4. **Full control** - modify any aspect
5. **Beginner-friendly** - learn Python while using it

**Getting Started:**
````bash
python main.py build me a calculator app
````

**For Support:**
- Check `troubleshooting` section
- Review agent logs in `builder.log`
- Examine generated files in `project/`

**Remember:** This is a learning tool as much as a builder. Explore the code, modify agents, and experiment!

---

*Document Version: 1.0*  
*Last Updated: November 2025*  
*Python Version: 3.8+*