import uuid
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from langchain_core.messages import HumanMessage, ToolMessage
from agent.graph import build_graph
from memory import get_memory

console = Console()

def print_response(text: str):
    console.print(Markdown(text))

def run():
    memory   = get_memory()
    graph    = build_graph(memory)
    thread   = {"configurable": {"thread_id": str(uuid.uuid4())}}

    console.print("[bold cyan]CLI Agent[/bold cyan] — type [bold]exit[/bold] to quit\n")

    while True:
        try:
            user_input = Prompt.ask("[bold green]>>>[/bold green]").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if user_input.lower() in ("exit", "quit", "q"):
            break
        if not user_input:
            continue

        inputs = {"messages": [HumanMessage(content=user_input)]}

        # ── Agentic loop ──────────────────────────────────────
        while True:
            # Stream events until graph pauses (interrupt) or ends
            final_text = ""
            for event in graph.stream(inputs, thread, stream_mode="values"):
                last = event["messages"][-1]

                # Stream LLM text responses
                if hasattr(last, "content") and last.content and not getattr(last, "tool_calls", None):
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
                console.print(f"\n[yellow]Tool:[/yellow] [bold]{tc['name']}[/bold]")
                console.print(f"[dim]{tc['args']}[/dim]")

            approved = Confirm.ask("[bold yellow]Run these tools?[/bold yellow]", default=True)
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