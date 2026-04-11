from .shell import run_shell
from .files import read_file, write_file, list_dir

ALL_TOOLS = [run_shell, read_file, write_file, list_dir]
TOOL_MAP  = {t.name: t for t in ALL_TOOLS}
