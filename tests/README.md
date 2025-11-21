# Test Suite

This directory contains tests for the Multi-Agent Builder system using pytest.

## Test Files

- **test_utils.py** - Unit tests for utilities (file operations, command executor)
- **test_agents.py** - Unit tests for all 8 AI agents (with mocked API calls)
- **test_system.py** - Integration tests for MultiAgentBuilder orchestrator

## Running Tests

### Install pytest
```bash
pip install pytest pytest-mock
```

### Run all tests
```bash
pytest tests/ -v
```

### Run specific test file
```bash
pytest tests/test_utils.py -v
pytest tests/test_agents.py -v
pytest tests/test_system.py -v
```

### Run with coverage
```bash
pip install pytest-cov
pytest tests/ --cov=. --cov-report=html
```

## Test Coverage

- **Utils**: File operations, command execution
- **Agents**: All 8 agents with mocked Gemini API
- **System**: Integration tests with complete mocking

## Notes

- All Gemini API calls are mocked to avoid actual API usage
- Tests use temporary directories for file operations
- Integration tests verify the complete workflow without real AI calls
