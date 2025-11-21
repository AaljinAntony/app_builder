import subprocess
import logging
from typing import List, Optional, Dict, Union

def execute(command: Union[str, List[str]], cwd: Optional[str] = None) -> Dict[str, Union[bool, str, int]]:
    """
    Executes a command safely using subprocess.run.
    
    Args:
        command: Command as list of arguments or space-separated string.
        cwd: Current working directory for the command.
        
    Returns:
        Dict containing success status, stdout, stderr, and exit_code.
    """
    try:
        # Convert string commands to list
        if isinstance(command, str):
            command = command.split()
        
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False, # We handle return codes manually
            timeout=300 # 5 minute timeout
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        logging.error(f"Command timed out: {command}")
        return {
            "success": False,
            "stdout": "",
            "stderr": "Command timed out",
            "exit_code": -1
        }
    except Exception as e:
        logging.error(f"Error executing command {command}: {e}")
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1
        }
