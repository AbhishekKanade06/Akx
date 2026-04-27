from .shell import run_shell
from .files import read_file, write_file, list_dir
from .web_search import web_search

ALL_TOOLS = [run_shell, read_file, write_file, list_dir, web_search]
TOOL_MAP = {t.name: t for t in ALL_TOOLS}
