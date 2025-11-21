import logging
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def setup_logger():
    """Configures the global logger for the application."""
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    logger = logging.getLogger("MultiAgentBuilder")
    logger.setLevel(log_level)
    
    # Prevent adding handlers multiple times if called repeatedly
    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File Handler
    file_handler = logging.FileHandler("builder.log", encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# Initialize logger on module import
logger = setup_logger()
