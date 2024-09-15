# src/claude_client.py

import logging
from typing import List, Dict
from pathlib import Path
from itertools import chain
import anthropic
from utils import get_media_type, image_to_base64

logger = logging.getLogger(__name__)

def create_image_object(image_path: Path, media_types: Dict[str, str]) -> Dict:
    """Create an image object from the image Path."""
    media_type = get_media_type(image_path, media_types)
    image_data = image_to_base64(image_path)
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": image_data,
        }
    }

def create_message_content(image_paths: List[Path], media_types: Dict[str, str]) -> List[Dict]:
    """Create message content from image Paths."""
    content_blocks = (
        [
            {"type": "text", "text": f"Image {i}:"},
            create_image_object(path, media_types)
        ]
        for i, path in enumerate(image_paths, 1)
    )
    return list(chain.from_iterable(content_blocks))

def prepare_claude_message(system_prompt: str, question: str, image_paths: List[Path], media_types: Dict[str, str]) -> List[Dict]:
    """Prepare message content for Claude."""
    message_content = create_message_content(image_paths, media_types)
    message_content.append({"type": "text", "text": question})
    return [{"type": "text", "text": system_prompt}] + message_content

def query_claude(client: anthropic.Anthropic, model: str, max_tokens: int, message_content: List[Dict]) -> str:
    """Query Claude API and return the response."""
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=message_content[0]["text"],  # System prompt
        messages=[{"role": "user", "content": message_content[1:]}]
    )
    return response.content[0].text

