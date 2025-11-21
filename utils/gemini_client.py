"""
Multi-Provider LLM Client (Gemini & Ollama)

This module supports switching between Google Gemini and Local Ollama using the LLM_PROVIDER environment variable.
- LLM_PROVIDER="gemini" (default): Uses google-generativeai with GEMINI_MODEL (default: gemini-2.5-flash)
- LLM_PROVIDER="ollama": Uses ollama with OLLAMA_MODEL (default: codegemma:7b)
"""

import os
import json
import time
import logging
from dotenv import load_dotenv

load_dotenv()

try:
    from utils.logger import logger
except Exception:
    logger = logging.getLogger("MultiAgentBuilder")
    logging.basicConfig(level=logging.INFO)

# Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "codegemma:7b")

# Provider Initialization
if LLM_PROVIDER == "gemini":
    import google.generativeai as genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=GEMINI_API_KEY)

elif LLM_PROVIDER == "ollama":
    import ollama
else:
    logger.warning(f"Unknown LLM_PROVIDER: {LLM_PROVIDER}. Defaulting to 'gemini' behavior if possible, or failing.")

def _generate_gemini(prompt: str, temperature: float, max_tokens: int) -> str:
    """Helper to generate text using Gemini."""
    model = genai.GenerativeModel(GEMINI_MODEL)
    generation_config = genai.GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_tokens
    )
    response = model.generate_content(prompt, generation_config=generation_config)
    return response.text

def _generate_ollama(prompt: str, temperature: float, max_tokens: int) -> str:
    """Helper to generate text using Ollama."""
    response = ollama.generate(
        model=OLLAMA_MODEL,
        prompt=prompt,
        stream=False,
        options={
            "temperature": temperature,
            "num_predict": max_tokens
        }
    )
    return response["response"]

def generate(prompt: str, temperature: float = 0.4, max_tokens: int = 4096) -> str:
    """
    Generates text using the configured LLM provider.
    
    Args:
        prompt: The input prompt.
        temperature: Controls randomness (0.0 to 1.0).
        max_tokens: Maximum number of tokens to generate.
        
    Returns:
        The generated text.
    """
    logger.info(f"Generating with {LLM_PROVIDER} (Model: {GEMINI_MODEL if LLM_PROVIDER == 'gemini' else OLLAMA_MODEL})")
    
    if LLM_PROVIDER == "gemini":
        return _generate_gemini(prompt, temperature, max_tokens)
    elif LLM_PROVIDER == "ollama":
        return _generate_ollama(prompt, temperature, max_tokens)
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}")

def extract_json(text: str) -> dict:
    """
    Extracts and parses JSON from text.
    
    Args:
        text: The text containing JSON.
        
    Returns:
        The parsed dictionary.
    """
    try:
        # Remove markdown code blocks
        cleaned_text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        try:
            # Try to find the first '{' and last '}'
            start_idx = text.find('{')
            end_idx = text.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = text[start_idx : end_idx + 1]
                return json.loads(json_str)
            else:
                raise ValueError("No JSON object found in text.")
        except Exception as e:
            logger.error(f"Error extracting JSON: {e}")
            raise

def generate_with_retry(prompt: str, max_retries: int = 3, **kwargs) -> str:
    """
    Generates text with retry logic for rate limits and errors.
    
    Args:
        prompt: The input prompt.
        max_retries: Number of retries.
        **kwargs: Arguments passed to generate.
        
    Returns:
        The generated text.
    """
    for attempt in range(1, max_retries + 1):
        try:
            return generate(prompt, **kwargs)
        except Exception as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(2 ** (attempt - 1)) # Exponential backoff
            else:
                logger.error(f"All {max_retries} attempts failed.")
                raise
