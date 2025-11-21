# Multi-Agent App Builder

An AI-powered multi-agent system that automatically builds software projects using **gemini-2.5-flash** - Google's fastest and lowest-latency generative AI model.

## Model Information

- **Model**: `gemini-2.5-flash`
- **Provider**: Google Generative AI
- **Python SDK**: `google-generativeai`
- **Advantages**: Fastest response times, lowest latency, optimized for rapid code generation

## System Architecture

This builder uses 8 specialized AI agents orchestrated by an AgentManager:

1. **LanguageSelector** - Chooses optimal tech stack
2. **Planner** - Creates implementation roadmap
3. **FrontendCoder** - Generates UI code
4. **BackendCoder** - Generates API/backend code
5. **TerminalAgent** - Executes installation commands
6. **Tester** - Generates test suites
7. **Debugger** - Analyzes and fixes errors
8. **DocumentationAgent** - Creates project docs

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/AaljinAntony/app_builder.git
cd app_builder
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure API Key

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
MAX_LOOPS=50
MAX_ERRORS=3
LOG_LEVEL=INFO
```

Get your API key from: https://aistudio.google.com/app/apikey

## Usage

### Basic Usage
```bash
python main.py "Build a todo app with Flask"
```

### Interactive Mode
```bash
python main.py
```
Then enter your prompt when asked.

### Examples
```bash
# Web application
python main.py "Create a blog platform with user authentication"

# API service
python main.py "Build a REST API for task management with SQLite"

# Simple tool
python main.py "Make a command-line calculator in Python"
```

## Output Structure

Generated projects are created in: `project/<sanitized_project_name>/`

Example for "Build a TODO app":
```
project/
└── build_a_todo_app/
    ├── PLAN.md              # Implementation plan
    ├── frontend/            # UI files
    ├── backend/             # API/server files
    ├── tests/               # Test files
    ├── TEST_REPORT.md       # Test results
    └── README.md            # Project documentation
```

## How It Works

1. **User provides prompt** describing what to build
2. **Project initialization** - Creates folder under `project/`
3. **Language selection** - AI selects optimal tech stack
4. **Planning** - AI creates detailed implementation plan
5. **Code generation** - Frontend and backend code generated
6. **Dependency installation** - Required packages installed
7. **Testing** - Tests generated and executed
8. **Documentation** - README and docs created
9. **Debugging** (if needed) - Errors analyzed and fixed

## Configuration

### Environment Variables (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | (required) | Your Google Gemini API key |
| `MAX_LOOPS` | `50` | Maximum agent iterations |
| `MAX_ERRORS` | `3` | Max consecutive errors before stopping |
| `LOG_LEVEL` | `INFO` | Logging verbosity (DEBUG/INFO/WARNING) |

### Temperature Settings (Optimized for gemini-2.5-flash)

- **Commands** (TerminalAgent): 0.2 - Highly deterministic
- **Code** (Frontend/Backend/Tester): 0.3 - Consistent output
- **Planning** (Planner/Debugger): 0.4 - Balanced creativity

## Logs

- **Console**: Real-time progress with color-coded messages
- **File**: `builder.log` (detailed logs in project root)

## Troubleshooting

### API Key Issues
```
Error: GEMINI_API_KEY not found
```
**Solution**: Add your API key to `.env` file

### Rate Limits
```
Error: 429 Too Many Requests
```
**Solution**: Wait a moment and retry, or upgrade your API plan

### Max Loops Reached
```
Warning: Max loops (50) reached
```
**Solution**: Increase `MAX_LOOPS` in `.env` or simplify project scope

## Requirements

- Python 3.8+
- `google-generativeai` SDK
- Active internet connection
- Valid Gemini API key

## Dependencies

```
google-generativeai>=0.3.0
python-dotenv>=1.0.0
```

## Project Structure

```
mutliagent_app_builder_using-antigravity/
├── agents/              # AI agent implementations
│   ├── agent_manager.py
│   ├── language_selector.py
│   ├── planner.py
│   ├── frontend_coder.py
│   ├── backend_coder.py
│   ├── terminal_agent.py
│   ├── tester.py
│   ├── debugger.py
│   └── documentation.py
├── prompts/             # Agent prompt templates
│   └── templates.py
├── utils/               # Utility functions
│   ├── file_ops.py
│   ├── command_executor.py
│   ├── logger.py
│   └── gemini_client.py
├── project/             # Generated projects (output)
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── .env                 # Configuration (create this)
└── README.md           # This file
```

## Why gemini-2.5-flash?

- **Speed**: 2-3x faster than standard models
- **Latency**: Sub-second response times
- **Cost**: More economical for high-volume generation
- **Quality**: Maintains high code quality while being faster
- **Optimized**: Built specifically for code generation tasks

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues or questions:
- Check `builder.log` for detailed error messages
- Review the generated `PLAN.md` in your project folder
- Ensure your `.env` file is configured correctly

---

Built with ❤️ using Google's gemini-2.5-flash
