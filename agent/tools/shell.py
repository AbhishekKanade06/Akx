import subprocess
from langchain_core.tools import tool


@tool
def run_shell(command: str) -> str:
    """Execute a shell/bash command and return its output. Use for running scripts, git, npm, etc."""
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, timeout=30
    )
    out = result.stdout.strip()
    err = result.stderr.strip()
    if result.returncode != 0:
        return f"[exit {result.returncode}]\n{err or out}"
    return out or "(no output)"
