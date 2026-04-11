import os
from pathlib import Path
from langchain_core.tools import tool

@tool
def read_file(path: str) -> str:
    """Read and return the contents of a file."""
    return Path(path).read_text()

@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file, creating it if it doesn't exist."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content)
    return f"Written {len(content)} chars to {path}"

@tool
def list_dir(path: str = ".") -> str:
    """List files and folders in a directory."""
    entries = os.listdir(path)
    return "\n".join(sorted(entries))