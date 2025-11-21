import os
import logging

def write_file(filepath: str, content: str) -> bool:
    """Writes content to a file, creating directories if necessary."""
    try:
        dirname = os.path.dirname(filepath)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        logging.error(f"Error writing file {filepath}: {e}")
        return False

def read_file(filepath: str) -> str:
    """Reads content from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error reading file {filepath}: {e}")
        return ""

def list_files(directory: str) -> list[str]:
    """Lists files in a directory."""
    try:
        if not os.path.exists(directory):
            return []
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except Exception as e:
        logging.error(f"Error listing files in {directory}: {e}")
        return []

def file_exists(filepath: str) -> bool:
    """Checks if a file exists."""
    return os.path.exists(filepath) and os.path.isfile(filepath)

def append_to_knowledge_base(filename: str, content: str) -> None:
    """Appends content to a file in the agency_kb directory."""
    kb_dir = "agency_kb"
    filepath = os.path.join(kb_dir, filename)
    try:
        os.makedirs(kb_dir, exist_ok=True)
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(content + "\n")
    except Exception as e:
        logging.error(f"Error appending to knowledge base {filepath}: {e}")
