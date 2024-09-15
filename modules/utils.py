# src/utils.py

import os
import base64
import logging
from typing import List, Dict
from pathlib import Path
import dotenv

logger = logging.getLogger(__name__)

def load_environment(env_vars: List[str], env_path: str = '.env') -> Dict[str, str]:
    """Load specified environment variables and return them as a dictionary."""
    dotenv.load_dotenv(env_path)
    env_values = {var: os.getenv(var) for var in env_vars}
    missing_vars = [var for var, val in env_values.items() if not val]
    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")
    return env_values

def load_file_content(file_path: Path) -> str:
    """Load content from a file."""
    return file_path.read_text().strip()

def image_to_base64(image_path: Path) -> str:
    """Convert the image to a base64 string."""
    image_data = image_path.read_bytes()
    return base64.b64encode(image_data).decode("utf-8")

def get_media_type(image_path: Path, media_types: Dict[str, str]) -> str:
    """Get the media type based on the file extension."""
    media_type = media_types.get(image_path.suffix.lower())
    if not media_type:
        logger.error(f"Unsupported image format: {image_path.name}")
        raise ValueError(f"Unsupported image format: {image_path.name}")
    return media_type

