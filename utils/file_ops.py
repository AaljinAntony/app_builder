import os
import logging
import asyncio
from typing import Optional

# MCP client integration (optional)
_mcp_client = None

def set_mcp_client(client):
    """Set the MCP client for file operations (optional)."""
    global _mcp_client
    _mcp_client = client
    if client:
        logging.info("file_ops: MCP client registered")

def _run_async(coro):
    """Helper to run async operations in sync context."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If event loop is running, we can't use it directly
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        # No event loop, create a new one
        return asyncio.run(coro)

def write_file(filepath: str, content: str) -> bool:
    """Writes content to a file, creating directories if necessary."""
    
    # Try MCP filesystem first if available
    if _mcp_client and _mcp_client.is_available('filesystem'):
        try:
            async def _mcp_write():
                return await _mcp_client.call_tool(
                    'filesystem',
                    'write_file',
                    {'path': filepath, 'content': content},
                    fallback_fn=None
                )
            result = _run_async(_mcp_write())
            logging.debug(f"Wrote {filepath} via MCP filesystem")
            return True
        except Exception as e:
            logging.warning(f"MCP write failed for {filepath}, using native: {e}")
    
    # Native fallback
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
    
    # Try MCP filesystem first if available
    if _mcp_client and _mcp_client.is_available('filesystem'):
        try:
            async def _mcp_read():
                return await _mcp_client.call_tool(
                    'filesystem',
                    'read_file',
                    {'path': filepath},
                    fallback_fn=None
                )
            content = _run_async(_mcp_read())
            logging.debug(f"Read {filepath} via MCP filesystem")
            return content
        except Exception as e:
            logging.warning(f"MCP read failed for {filepath}, using native: {e}")
    
    # Native fallback
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
