from rich.console import Console
from rich import box
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from datetime import datetime
import ast
import hashlib
import random
import re
import sys
import termios
import tty
from langchain_core.messages import HumanMessage, ToolMessage
from agent.graph import build_graph
from memory import get_memory
import config

console = Console()
APP_ICON = "◈"
ASSISTANT_ICON = "✦"
WORKSPACE_ICON = "◉"
STATUS_ICON = "▣"
SESSION_ICON = "⌘"
TOOL_ICON = "⚙"
MODEL_ICON = "◌"
TIME_ICON = "◷"
APP_BORDER = "bright_cyan"
WORKSPACE_BORDER = "bright_magenta"
STATUS_BORDER = "bright_green"
ASSISTANT_BORDER = "deep_sky_blue1"
TOOL_BORDER = "bright_yellow"
MUTED_TEXT = "grey70"
HEADER_STYLE = "bold white on rgb(0,95,135)"
HEADER_SUBTITLE = "session-aware • tool-enabled • local-first"
PROMPT_ICON = "◈"
THEME_NAME = "Neon Grid"

THEMES = [
    {
        "name": "Neon Grid",
        "app_icon": "◈",
        "assistant_icon": "✦",
        "workspace_icon": "◉",
        "status_icon": "▣",
        "session_icon": "⌘",
        "tool_icon": "⚙",
        "model_icon": "◌",
        "time_icon": "◷",
        "app_border": "bright_cyan",
        "workspace_border": "bright_magenta",
        "status_border": "bright_green",
        "assistant_border": "deep_sky_blue1",
        "tool_border": "bright_yellow",
        "muted": "bright_black",
        "header_style": "bold white on rgb(0,95,135)",
        "subtitle": "neon shell • sharp edges • cool glow",
        "prompt_icon": "◈",
    },
    {
        "name": "Amber Terminal",
        "app_icon": "◬",
        "assistant_icon": "✶",
        "workspace_icon": "◎",
        "status_icon": "▤",
        "session_icon": "◭",
        "tool_icon": "⛭",
        "model_icon": "◍",
        "time_icon": "◴",
        "app_border": "bright_yellow",
        "workspace_border": "dark_orange",
        "status_border": "gold3",
        "assistant_border": "khaki1",
        "tool_border": "orange1",
        "muted": "bright_black",
        "header_style": "bold black on rgb(255,190,50)",
        "subtitle": "warm glass • brass accents • midnight desk",
        "prompt_icon": "◬",
    },
    {
        "name": "Ghost Signal",
        "app_icon": "◇",
        "assistant_icon": "✧",
        "workspace_icon": "◌",
        "status_icon": "▢",
        "session_icon": "⟡",
        "tool_icon": "⚚",
        "model_icon": "◎",
        "time_icon": "◵",
        "app_border": "bright_white",
        "workspace_border": "plum3",
        "status_border": "spring_green3",
        "assistant_border": "white",
        "tool_border": "thistle1",
        "muted": "bright_black",
        "header_style": "bold black on rgb(210,230,235)",
        "subtitle": "soft static • pale metal • quiet control room",
        "prompt_icon": "◇",
    },
    {
        "name": "Forge Mode",
        "app_icon": "⬢",
        "assistant_icon": "✹",
        "workspace_icon": "◍",
        "status_icon": "▥",
        "session_icon": "⎔",
        "tool_icon": "🛠",
        "model_icon": "◐",
        "time_icon": "◷",
        "app_border": "red3",
        "workspace_border": "bright_red",
        "status_border": "chartreuse3",
        "assistant_border": "salmon1",
        "tool_border": "orange_red1",
        "muted": "bright_black",
        "header_style": "bold white on rgb(120,25,25)",
        "subtitle": "industrial shell • hot metal • build bay",
        "prompt_icon": "⬢",
    },
]


def apply_theme(theme: dict) -> None:
    global APP_ICON, ASSISTANT_ICON, WORKSPACE_ICON, STATUS_ICON, SESSION_ICON
    global TOOL_ICON, MODEL_ICON, TIME_ICON, APP_BORDER, WORKSPACE_BORDER
    global STATUS_BORDER, ASSISTANT_BORDER, TOOL_BORDER, MUTED_TEXT
    global HEADER_STYLE, HEADER_SUBTITLE, PROMPT_ICON, THEME_NAME

    APP_ICON = theme["app_icon"]
    ASSISTANT_ICON = theme["assistant_icon"]
    WORKSPACE_ICON = theme["workspace_icon"]
    STATUS_ICON = theme["status_icon"]
    SESSION_ICON = theme["session_icon"]
    TOOL_ICON = theme["tool_icon"]
    MODEL_ICON = theme["model_icon"]
    TIME_ICON = theme["time_icon"]
    APP_BORDER = theme["app_border"]
    WORKSPACE_BORDER = theme["workspace_border"]
    STATUS_BORDER = theme["status_border"]
    ASSISTANT_BORDER = theme["assistant_border"]
    TOOL_BORDER = theme["tool_border"]
    MUTED_TEXT = theme["muted"]
    HEADER_STYLE = theme["header_style"]
    HEADER_SUBTITLE = theme["subtitle"]
    PROMPT_ICON = theme["prompt_icon"]
    THEME_NAME = theme["name"]


def normalize_text(text) -> str:
    if isinstance(text, list):
        parts = []
        for item in text:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
            else:
                parts.append(str(item))
        return "\n".join(part for part in parts if part)
    return str(text)


def print_response(text):
    text = normalize_text(text)
    console.print(
        Panel(
            Markdown(text),
            title=f"[bold {ASSISTANT_BORDER}]{ASSISTANT_ICON} Assistant[/bold {ASSISTANT_BORDER}]",
            border_style=ASSISTANT_BORDER,
            box=box.ROUNDED,
            padding=(0, 1),
        )
    )


def print_plain_panel(text: str, title: str, border_style: str, icon: str):
    console.print(
        Panel(
            text,
            title=f"[bold {border_style}]{icon} {title}[/bold {border_style}]",
            border_style=border_style,
            box=box.ROUNDED,
            padding=(0, 1),
        )
    )


def show_tools():
    tools_text = "\n".join(
        [
            "run_shell: execute a shell command and return its output",
            "read_file: read a file from disk",
            "write_file: create or overwrite a file",
            "list_dir: list files and folders in a directory",
        ]
    )
    print_plain_panel(tools_text, "Tools", STATUS_BORDER, TOOL_ICON)


def classify_local_input(text: str) -> str:
    normalized = " ".join(text.lower().strip().split())
    if normalized == "/exit":
        return "exit"
    if normalized == "/model":
        return "model"
    if normalized == "/tools":
        return "tools"
    if normalized == "/session":
        return "session"
    if normalized == "/new":
        return "new"
    if normalized in {"/status", "/statu", "/help"}:
        return "status"
    if normalized.startswith("/resume"):
        return "resume"
    if normalized in {
        "which tools do you have",
        "what tools do you have",
        "show tools",
        "list tools",
        "what can you do",
    }:
        return "tools"
    return "chat"


def format_timestamp(value: str | None) -> str:
    if not value:
        return "-"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime(
            "%Y-%m-%d %H:%M"
        )
    except ValueError:
        return value


def normalize_thread_id(value) -> str:
    if isinstance(value, dict):
        nested = value.get("thread_id")
        return normalize_thread_id(nested) if nested is not None else str(value)
    if value is None:
        return ""
    text = str(value).strip()
    if text.startswith("{") and text.endswith("}"):
        try:
            parsed = ast.literal_eval(text)
        except (ValueError, SyntaxError):
            return text
        if isinstance(parsed, dict):
            nested = parsed.get("thread_id")
            return normalize_thread_id(nested) if nested is not None else text
    return text


def make_session_display_name(thread_id: str, position: int | None = None) -> str:
    normalized = normalize_thread_id(thread_id)
    if normalized == "default":
        return "Home Base"

    adjectives = [
        "Amber",
        "Atomic",
        "Blue",
        "Carbon",
        "Crimson",
        "Echo",
        "Golden",
        "Granite",
        "Ivory",
        "Jade",
        "Midnight",
        "Nova",
        "Obsidian",
        "Silver",
        "Solar",
        "Velvet",
    ]
    nouns = [
        "Archive",
        "Beacon",
        "Circuit",
        "Compass",
        "Forge",
        "Harbor",
        "Horizon",
        "Lab",
        "Loom",
        "Nest",
        "Orbit",
        "Relay",
        "Studio",
        "Vault",
        "Workshop",
        "Yard",
    ]

    digest = hashlib.sha1(normalized.encode("utf-8")).digest()
    adjective = adjectives[digest[0] % len(adjectives)]
    noun = nouns[digest[1] % len(nouns)]

    match = re.fullmatch(r"session-(\d+)", normalized)
    if match:
        return f"{adjective} {noun} {match.group(1)}"
    if position is not None:
        return f"{adjective} {noun} {position}"
    return f"{adjective} {noun}"


def get_saved_sessions(memory, limit: int = 12) -> list[dict[str, str]]:
    sessions = []
    seen = set()
    try:
        for index, checkpoint in enumerate(memory.list(None), start=1):
            config_data = checkpoint.config.get("configurable", {})
            thread_id = normalize_thread_id(config_data.get("thread_id"))
            if thread_id and thread_id not in seen:
                sessions.append(
                    {
                        "thread_id": thread_id,
                        "updated_at": checkpoint.checkpoint.get("ts", ""),
                        "label": make_session_display_name(thread_id, index),
                    }
                )
                seen.add(thread_id)
            if len(sessions) >= limit:
                break
    except Exception:
        return []
    return sessions


def get_session_info(memory, thread_id: str) -> dict[str, str] | None:
    thread_id = normalize_thread_id(thread_id)
    for session in get_saved_sessions(memory, limit=100):
        if session["thread_id"] == thread_id:
            return session
    return None


def next_session_id(memory) -> str:
    existing = {session["thread_id"] for session in get_saved_sessions(memory, limit=100)}
    index = 1
    while True:
        candidate = f"session-{index}"
        if candidate not in existing:
            return candidate
        index += 1


def render_session_picker(sessions, current_index: int, current_thread_id: str | None):
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan", justify="right")
    table.add_column(style="bold magenta")
    table.add_column(style="dim white")
    table.add_column(style="white")

    for index, session in enumerate(sessions, start=1):
        session_id = session["thread_id"]
        marker = "current" if session_id == current_thread_id else ""
        label = session.get("label", session_id)
        timestamp = format_timestamp(session.get("updated_at"))
        if index - 1 == current_index:
            table.add_row(
                f"[bold green]>[/bold green] {index}",
                f"[reverse]{label}[/reverse]",
                f"[reverse]{timestamp}[/reverse]",
                f"[reverse]{marker}[/reverse]" if marker else "[reverse] [/reverse]",
            )
        else:
            table.add_row(str(index), label, timestamp, marker)

    return Panel(
        table,
        title=f"[bold {WORKSPACE_BORDER}]{SESSION_ICON} Session Deck[/bold {WORKSPACE_BORDER}]",
        subtitle=f"[{MUTED_TEXT}]↑/↓ move • Enter select • q cancel[/{MUTED_TEXT}]",
        border_style=WORKSPACE_BORDER,
        box=box.HEAVY,
        padding=(0, 1),
    )


def choose_session_with_arrows(sessions, current_thread_id: str | None = None) -> str | None:
    if not sys.stdin.isatty():
        return None

    current_index = 0
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            console.clear()
            console.print(render_session_picker(sessions, current_index, current_thread_id))
            key = sys.stdin.read(1)
            if key == "\x1b":
                next_chars = sys.stdin.read(2)
                if next_chars == "[A":
                    current_index = (current_index - 1) % len(sessions)
                elif next_chars == "[B":
                    current_index = (current_index + 1) % len(sessions)
            elif key in ("\r", "\n"):
                console.clear()
                return sessions[current_index]["thread_id"]
            elif key.lower() == "q":
                console.clear()
                return ""
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def choose_session(memory, current_thread_id: str | None = None) -> str | None:
    sessions = get_saved_sessions(memory)
    if not sessions:
        console.print("[yellow]No saved sessions found.[/yellow]")
        return None

    selected = choose_session_with_arrows(sessions, current_thread_id)
    if selected == "":
        return None
    if selected is not None:
        return selected

    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan", justify="right")
    table.add_column(style="bold magenta")
    table.add_column(style="dim white")
    table.add_column(style="white")
    for index, session in enumerate(sessions, start=1):
        session_id = session["thread_id"]
        marker = "current" if session_id == current_thread_id else ""
        table.add_row(
            str(index),
            session.get("label", session_id),
            format_timestamp(session.get("updated_at")),
            marker,
        )

    console.print(
        Panel(
            table,
            title=f"[bold {WORKSPACE_BORDER}]{SESSION_ICON} Session Deck[/bold {WORKSPACE_BORDER}]",
            border_style=WORKSPACE_BORDER,
            box=box.HEAVY,
            padding=(0, 1),
        )
    )
    selection = IntPrompt.ask(
        "[bold blue]Resume session number[/bold blue]",
        default=1,
    )
    if 1 <= selection <= len(sessions):
        return sessions[selection - 1]["thread_id"]

    console.print("[red]Invalid session number.[/red]")
    return None


def print_status(memory, thread_id: str):
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column(style="white")
    current = get_session_info(memory, thread_id)
    table.add_row("Provider", str(config.PROVIDER))
    table.add_row("Model", str(config.MODEL))
    table.add_row("Base URL", str(config.BASE_URL or "-"))
    table.add_row("Max Tokens", str(config.MAX_TOKENS))
    table.add_row("Auto Approve", str(config.AUTO_APPROVE))
    table.add_row("Session", current.get("label", thread_id) if current else thread_id)
    table.add_row("Thread ID", thread_id)
    table.add_row("Updated", format_timestamp(current.get("updated_at")) if current else "-")
    sessions = get_saved_sessions(memory)
    if sessions:
        session_table = Table.grid(padding=(0, 1))
        session_table.add_column(style="bold magenta")
        session_table.add_column(style="dim white")
        session_table.add_column(style="white")
        for session in sessions:
            session_id = session["thread_id"]
            marker = "current" if session_id == thread_id else ""
            session_table.add_row(
                session.get("label", session_id),
                format_timestamp(session.get("updated_at")),
                marker,
            )
        session_panel = Panel(
            session_table,
            title=f"[bold {WORKSPACE_BORDER}]{SESSION_ICON} Saved Sessions[/bold {WORKSPACE_BORDER}]",
            border_style=WORKSPACE_BORDER,
            box=box.ROUNDED,
            padding=(0, 1),
        )
        content = Columns(
            [
                Panel(
                    table,
                    title=f"[bold {STATUS_BORDER}]{STATUS_ICON} Status Matrix[/bold {STATUS_BORDER}]",
                    border_style=STATUS_BORDER,
                    box=box.ROUNDED,
                    padding=(0, 1),
                ),
                session_panel,
            ],
            equal=True,
            expand=True,
        )
    else:
        content = Panel(
            table,
            title=f"[bold {STATUS_BORDER}]{STATUS_ICON} Status Matrix[/bold {STATUS_BORDER}]",
            border_style=STATUS_BORDER,
            box=box.ROUNDED,
            padding=(0, 1),
        )
    console.print(
        content
    )


def make_thread(thread_id: str) -> dict:
    return {"configurable": {"thread_id": normalize_thread_id(thread_id)}}


def resume_session(graph, memory, thread_id: str):
    thread_id = normalize_thread_id(thread_id)
    thread = make_thread(thread_id)
    state = graph.get_state(thread)
    messages = state.values.get("messages", []) if state.values else []
    session = get_session_info(memory, thread_id)
    updated_at = format_timestamp(session.get("updated_at")) if session else "-"
    label = session.get("label", thread_id) if session else thread_id
    console.print(
        Panel(
            f"[bold]{SESSION_ICON} Session:[/bold] {label}\n[bold]Saved messages:[/bold] {len(messages)}\n[bold]{TIME_ICON} Updated:[/bold] {updated_at}",
            title=f"[bold {WORKSPACE_BORDER}]{WORKSPACE_ICON} Workspace[/bold {WORKSPACE_BORDER}]",
            border_style=WORKSPACE_BORDER,
            box=box.DOUBLE,
            padding=(0, 1),
        )
    )
    return thread_id, label, thread


def print_welcome():
    title = Text(f"{APP_ICON} AKX CLI AGENT", style=HEADER_STYLE)
    subtitle = Text(
        f"{HEADER_SUBTITLE} • {THEME_NAME}",
        style=f"italic {MUTED_TEXT}",
    )
    commands = Table.grid(expand=True)
    commands.add_column(style="bold bright_cyan", ratio=1)
    commands.add_column(style="white", ratio=3)
    commands.add_row(f"{MODEL_ICON} /model", "inspect active model")
    commands.add_row(f"{TOOL_ICON} /tools", "show available tools")
    commands.add_row(f"{STATUS_ICON} /status", "inspect runtime + sessions")
    commands.add_row(f"{SESSION_ICON} /session", "show current workspace")
    commands.add_row(f"{SESSION_ICON} /resume", "open session deck")
    commands.add_row(f"{WORKSPACE_ICON} /new", "spawn fresh workspace")
    commands.add_row("✕ /exit", "leave the console")
    console.print(
        Panel(
            commands,
            title=title,
            subtitle=subtitle,
            border_style=APP_BORDER,
            box=box.DOUBLE_EDGE,
            padding=(1, 2),
        )
    )


def run():
    apply_theme(random.choice(THEMES))
    memory = get_memory()
    graph = build_graph(memory)
    print_welcome()
    latest = get_saved_sessions(memory, limit=1)
    session_id = latest[0]["thread_id"] if latest else next_session_id(memory)
    thread_id, session_label, thread = resume_session(graph, memory, session_id)

    while True:
        try:
            user_input = Prompt.ask(
                f"[bold {APP_BORDER}]{PROMPT_ICON}[/bold {APP_BORDER}] [bold white]{session_label}[/bold white]"
            ).strip()
        except (KeyboardInterrupt, EOFError):
            break

        if user_input.lower() in ("exit", "quit", "q"):
            break
        if not user_input:
            continue
        local_intent = classify_local_input(user_input)

        if local_intent == "exit":
            break
        if local_intent == "model":
            console.print(
                Panel(
                    f"[bold]{MODEL_ICON} Current model:[/bold] {config.MODEL}",
                    border_style=ASSISTANT_BORDER,
                    box=box.ROUNDED,
                    padding=(0, 1),
                )
            )
            continue
        if local_intent == "tools":
            show_tools()
            continue
        if local_intent == "session":
            console.print(
                Panel(
                    f"[bold]{SESSION_ICON} Current session:[/bold] {session_label}\n[bold]Thread ID:[/bold] {thread_id}",
                    border_style=WORKSPACE_BORDER,
                    box=box.ROUNDED,
                    padding=(0, 1),
                )
            )
            continue
        if local_intent == "new":
            thread_id, session_label, thread = resume_session(
                graph, memory, next_session_id(memory)
            )
            continue
        if local_intent == "status":
            print_status(memory, thread_id)
            continue
        if local_intent == "resume":
            parts = user_input.split(maxsplit=1)
            if len(parts) == 1:
                selected = choose_session(memory, thread_id)
                if not selected:
                    continue
                thread_id, session_label, thread = resume_session(
                    graph, memory, selected
                )
                continue
            thread_id, session_label, thread = resume_session(
                graph, memory, parts[1].strip()
            )
            continue

        inputs = {"messages": [HumanMessage(content=user_input)]}

        # ── Agentic loop ──────────────────────────────────────
        while True:
            # Stream events until graph pauses (interrupt) or ends
            final_text = ""
            for event in graph.stream(inputs, thread, stream_mode="values"):
                last = event["messages"][-1]

                # Stream LLM text responses
                if (
                    hasattr(last, "content")
                    and last.content
                    and not getattr(last, "tool_calls", None)
                ):
                    final_text = last.content

            if final_text:
                print_response(final_text)

            # Check if graph is paused at approval gate
            state = graph.get_state(thread)
            refreshed = get_session_info(memory, thread_id)
            if refreshed:
                session_label = refreshed.get("label", session_label)
            if not state.next:
                break  # graph finished

            # ── Approval gate ──────────────────────────────────
            pending = state.values["messages"][-1]
            for tc in pending.tool_calls:
                console.print(
                    Panel(
                        f"[bold]{TOOL_ICON} Tool:[/bold] {tc['name']}\n[bold]Args:[/bold] {tc['args']}",
                        title="[bold yellow]Approval Required[/bold yellow]",
                        border_style=TOOL_BORDER,
                        box=box.HEAVY,
                        padding=(0, 1),
                    )
                )

            approved = Confirm.ask(
                "[bold yellow]Run these tools?[/bold yellow]", default=True
            )
            if not approved:
                # Inject a cancellation message and resume
                cancel_msgs = [
                    ToolMessage(content="Cancelled by user.", tool_call_id=tc["id"])
                    for tc in pending.tool_calls
                ]
                graph.update_state(thread, {"messages": cancel_msgs}, as_node="tools")

            inputs = None  # resume with no new input


if __name__ == "__main__":
    run()
