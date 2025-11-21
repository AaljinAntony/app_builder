import os
import sys

# Add project root to sys.path
sys.path.append(os.getcwd())

# Force provider to ollama
os.environ["LLM_PROVIDER"] = "ollama"
os.environ["OLLAMA_MODEL"] = "codegemma:7b"

try:
    from utils import gemini_client
    print("Attempting to generate with Ollama...")
    response = gemini_client.generate("Hello, are you working?", max_tokens=50)
    print(f"Response: {response}")
    print("Ollama connection successful.")
except Exception as e:
    print(f"Ollama connection failed: {e}")
    sys.exit(1)
