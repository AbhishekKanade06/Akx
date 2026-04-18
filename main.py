from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from datetime import datetime
from langchain_core.messages import HumanMessage, ToolMessage
from agent.graph import build_graph
from memory import get_memory
import config

console = Console()


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
            title="[bold cyan]Assistant[/bold cyan]",
            border_style="cyan",
            padding=(0, 1),
        )
    )


def format_timestamp(value: str | None) -> str:
    if not value:
        return "-"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime(
            "%Y-%m-%d %H:%M"
        )
    except ValueError:
        return value


def get_saved_sessions(memory, limit: int = 12) -> list[dict[str, str]]:
    sessions = []
    seen = set()
    try:
        for checkpoint in memory.list(None):
            config_data = checkpoint.config.get("configurable", {})
            thread_id = config_data.get("thread_id")
            if thread_id and thread_id not in seen:
                sessions.append(
                    {
                        "thread_id": thread_id,
                        "updated_at": checkpoint.checkpoint.get("ts", ""),
                    }
                )
                seen.add(thread_id)
            if len(sessions) >= limit:
                break
    except Exception:
        return []
    return sessions


def get_session_info(memory, thread_id: str) -> dict[str, str] | None:
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


def choose_session(memory, current_thread_id: str | None = None) -> str | None:
    sessions = get_saved_sessions(memory)
    if not sessions:
        console.print("[yellow]No saved sessions found.[/yellow]")
        return None

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
            session_id,
            format_timestamp(session.get("updated_at")),
            marker,
        )

    console.print(
        Panel(
            table,
            title="[bold magenta]Choose Session[/bold magenta]",
            border_style="magenta",
            padding=(0, 1),
        )
    )
    selection = IntPrompt.ask(
        "[bold blue]Resume session number[/bold blue]",
        default=1,
    )
    if 1 <= selection <= len(sessions):
        return sessions[selection - 1]

    console.print("[red]Invalid session number.[/red]")
    return None


def print_status(memory, thread_id: str):
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column(style="white")
    table.add_row("Provider", str(config.PROVIDER))
    table.add_row("Model", str(config.MODEL))
    table.add_row("Base URL", str(config.BASE_URL or "-"))
    table.add_row("Max Tokens", str(config.MAX_TOKENS))
    table.add_row("Auto Approve", str(config.AUTO_APPROVE))
    table.add_row("Thread ID", thread_id)
    current = get_session_info(memory, thread_id)
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
                session_id,
                format_timestamp(session.get("updated_at")),
                marker,
            )
        session_panel = Panel(
            session_table,
            title="[bold magenta]Saved Sessions[/bold magenta]",
            border_style="magenta",
            padding=(0, 1),
        )
        content = Columns(
            [
                Panel(
                    table,
                    title="[bold green]Status[/bold green]",
                    border_style="green",
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
            title="[bold green]Status[/bold green]",
            border_style="green",
            padding=(0, 1),
        )
    console.print(
        content
    )


def make_thread(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}


def resume_session(graph, memory, thread_id: str):
    thread = make_thread(thread_id)
    state = graph.get_state(thread)
    messages = state.values.get("messages", []) if state.values else []
    session = get_session_info(memory, thread_id)
    updated_at = format_timestamp(session.get("updated_at")) if session else "-"
    console.print(
        Panel(
            f"[bold]Session:[/bold] {thread_id}\n[bold]Saved messages:[/bold] {len(messages)}\n[bold]Updated:[/bold] {updated_at}",
            title="[bold magenta]Workspace[/bold magenta]",
            border_style="magenta",
            padding=(0, 1),
        )
    )
    return thread_id, thread


def print_welcome():
    title = Text("AKX CLI AGENT", style="bold white on blue")
    subtitle = Text("session-aware • tool-enabled • local-first", style="dim cyan")
    commands = Table.grid(expand=True)
    commands.add_column(style="bold yellow", ratio=1)
    commands.add_column(style="white", ratio=3)
    commands.add_row("/model", "show active model")
    commands.add_row("/status", "show runtime config")
    commands.add_row("/session", "show current session")
    commands.add_row("/resume", "pick a saved session")
    commands.add_row("/new", "start a fresh session")
    commands.add_row("/exit", "quit the CLI")
    console.print(
        Panel(
            commands,
            title=title,
            subtitle=subtitle,
            border_style="blue",
            padding=(1, 2),
        )
    )


def run():
    memory = get_memory()
    graph = build_graph(memory)
    print_welcome()
    latest = get_saved_sessions(memory, limit=1)
    session_id = latest[0]["thread_id"] if latest else next_session_id(memory)
    thread_id, thread = resume_session(graph, memory, session_id)

    while True:
        try:
            user_input = Prompt.ask(f"[bold green]{thread_id}[/bold green]").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if user_input.lower() in ("exit", "quit", "q"):
            break
        if not user_input:
            continue
        if user_input == "/exit":
            break
        if user_input == "/model":
            console.print(
                Panel(
                    f"[bold]Current model:[/bold] {config.MODEL}",
                    border_style="cyan",
                    padding=(0, 1),
                )
            )
            continue
        if user_input == "/session":
            console.print(
                Panel(
                    f"[bold]Current session:[/bold] {thread_id}",
                    border_style="magenta",
                    padding=(0, 1),
                )
            )
            continue
        if user_input == "/new":
            thread_id, thread = resume_session(graph, memory, next_session_id(memory))
            continue
        if user_input in {"/status", "/statu", "/help"}:
            print_status(memory, thread_id)
            continue
        if user_input.startswith("/resume"):
            parts = user_input.split(maxsplit=1)
            if len(parts) == 1:
                selected = choose_session(memory, thread_id)
                if not selected:
                    continue
                thread_id, thread = resume_session(graph, memory, selected)
                continue
            thread_id, thread = resume_session(graph, memory, parts[1].strip())
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
            if not state.next:
                break  # graph finished

            # ── Approval gate ──────────────────────────────────
            pending = state.values["messages"][-1]
            for tc in pending.tool_calls:
                console.print(
                    Panel(
                        f"[bold]Tool:[/bold] {tc['name']}\n[bold]Args:[/bold] {tc['args']}",
                        title="[bold yellow]Approval Required[/bold yellow]",
                        border_style="yellow",
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
