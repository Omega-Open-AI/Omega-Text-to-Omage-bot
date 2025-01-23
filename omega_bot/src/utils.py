import os
import requests
from pathlib import Path
from urllib.parse import urlparse
from typing import Union, Optional
import matplotlib.pyplot as plt
from .config_loader import ConfigLoader
from .exceptions import SecurityError

def sanitize_path(user_path: Union[str, Path]) -> Path:
    """Sanitize and validate file paths"""
    config = ConfigLoader().config
    safe_path = Path(user_path).resolve()
    output_dir = Path(config["output_dir"]).resolve()

    # Ensure path is within allowed directory
    try:
        safe_path.relative_to(output_dir)
    except ValueError:
        raise SecurityError(f"Path {safe_path} is outside allowed directory {output_dir}")

    # Validate file extension
    if safe_path.suffix.lower() not in config["allowed_extensions"]:
        raise SecurityError(f"Invalid file extension {safe_path.suffix}")

    return safe_path

def save_image(image_url: str, file_path: Union[str, Path]) -> None:
    sanitized_path = sanitize_path(file_path)
    sanitized_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(image_url)
    response.raise_for_status()

    with open(sanitized_path, 'wb') as f:
        f.write(response.content)

def display_image(image_path: Union[str, Path]) -> None:
    img = plt.imread(image_path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()
