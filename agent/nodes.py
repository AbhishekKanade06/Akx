import re
from enum import Enum

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import END
from .state import AgentState
import config
from .llm_factory import make_llm


chat_llm = make_llm(enable_tools=False)
tool_llm = make_llm(enable_tools=True)


class Intent(str, Enum):
    CHAT = "chat"
    LOCAL_COMMAND = "local_command"
    TOOL_TASK = "tool_task"

ACTION_HINTS = (
    "read",
    "write",
    "edit",
    "update",
    "change",
    "fix",
    "create",
    "delete",
    "remove",
    "rename",
    "move",
    "list",
    "find",
    "search",
    "show",
    "open",
    "run",
    "execute",
    "install",
    "test",
    "build",
    "commit",
    "diff",
    "explain",
    "inspect",
    "analyze",
)

TARGET_HINTS = (
    "file",
    "folder",
    "directory",
    "command",
    "shell",
    "terminal",
    "python",
    "git",
    "uv",
    "pip",
    "npm",
)

PATH_PATTERN = re.compile(r"([~/]|\./|\.\./|[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")
FILE_EXT_PATTERN = re.compile(r"\.[a-zA-Z0-9]{1,8}\b")


def looks_like_action_request(text: str) -> bool:
    has_action = any(hint in text for hint in ACTION_HINTS)
    has_target = any(hint in text for hint in TARGET_HINTS)
    has_path = bool(PATH_PATTERN.search(text))
    has_file_ext = bool(FILE_EXT_PATTERN.search(text))
    has_code_marker = "`" in text or "\n" in text
    has_shell_shape = any(token in text for token in ("&&", "|", ">", "ls ", "cat ", "git "))

    if not has_action:
        return False

    return has_target or has_path or has_file_ext or has_code_marker or has_shell_shape


def classify_intent(state: AgentState) -> Intent:
    last = state["messages"][-1]
    if isinstance(last, ToolMessage):
        return Intent.TOOL_TASK
    if not isinstance(last, HumanMessage):
        return Intent.CHAT

    text = str(last.content).strip().lower()
    if not text:
        return Intent.CHAT
    if text.startswith("/"):
        return Intent.LOCAL_COMMAND
    if len(text.split()) <= 2:
        return Intent.CHAT
    if looks_like_action_request(text):
        return Intent.TOOL_TASK
    return Intent.CHAT


def should_enable_tools(state: AgentState) -> bool:
    return classify_intent(state) == Intent.TOOL_TASK

def call_llm(state: AgentState) -> dict:
    """The main LLM node — prepends system prompt, calls the model."""
    messages = [SystemMessage(content=config.SYSTEM_PROMPT)] + state["messages"]
    intent = classify_intent(state)
    llm = tool_llm if intent == Intent.TOOL_TASK else chat_llm
    response = llm.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    """Router: if the last message has tool calls → go to tools, else → END."""
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END
