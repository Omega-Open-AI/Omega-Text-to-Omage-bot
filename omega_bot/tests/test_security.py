import pytest
from pathlib import Path
from src.utils import sanitize_path
from src.exceptions import SecurityError

def test_valid_path():
    path = sanitize_path("outputs/test.png")
    assert str(path).endswith("outputs/test.png")

def test_directory_traversal():
    with pytest.raises(SecurityError):
        sanitize_path("../../etc/passwd")

def test_invalid_extension():
    with pytest.raises(SecurityError):
        sanitize_path("outputs/test.txt")
