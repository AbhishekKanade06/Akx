# ॐ
---

# AkX 0.0.0 — Custom CLI Agent 

A Codex-style CLI agent built with LangGraph, LangChain, and your own LLM. Supports local models via Ollama, remote APIs like Groq and OpenAI, and comes with a human approval gate, persistent memory, and built-in file + shell tools.

---

## Features

- LangGraph state machine with a clean agentic loop
- Human-in-the-loop approval gate before any tool runs
- Persistent memory across sessions via SQLite checkpointing
- Auto-resume into the latest saved session on startup
- Slash commands for model, status, resume, new session, and exit
- Built-in tools: shell executor, file read/write, directory listing
- Swap any LLM — Ollama, Mistral, LLaMA, GPT-4o, Groq, and more
- Rich terminal UI with panels, markdown rendering, and session timestamps

---

## Project Structure

```
Akx/
├── main.py               # CLI entry point
├── config.py             # Model settings and system prompt
├── memory.py             # SQLite checkpointer
├── pyproject.toml
└── agent/
    ├── __init__.py
    ├── graph.py           # LangGraph state machine
    ├── nodes.py           # LLM node + routing logic
    ├── state.py           # AgentState definition
    └── tools/
        ├── __init__.py
        ├── registry.py    # Tool registry
        ├── shell.py       # Shell executor tool
        └── files.py       # File read/write tools
```

---

## Requirements

- Python >= 3.13,<3.14
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- [Ollama](https://ollama.com) for local models

---

## Installation

```bash
# Clone the repo
git clone https://github.com/yourname/akx.git
cd akx

# Install dependencies
uv sync

# Or with pip
pip install -e .
```

---

## Usage

### With Ollama (local)

```bash
# Pull a model first
ollama pull mistral

# Run the agent
export AGENT_BASE_URL=http://localhost:11434/v1
export AGENT_MODEL=mistral
python main.py
```

### With OpenAI

```bash
export OPENAI_API_KEY=sk-...
export AGENT_PROVIDER=openai
export AGENT_MODEL=gpt-4o
python main.py
```

### With Groq

```bash
export AGENT_BASE_URL=https://api.groq.com/openai/v1
export OPENAI_API_KEY=gsk_...
export AGENT_PROVIDER=groq
export AGENT_MODEL=llama3-8b-8192
python main.py
```

---

## CLI Commands

| Command | Description |
|---|---|
| `/model` | Show the active model |
| `/status` | Show runtime config and saved sessions |
| `/session` | Show the current session |
| `/resume` | Open a numbered picker for saved sessions |
| `/new` | Start a fresh auto-named session |
| `/exit` | Quit the CLI |

---

## Session Behavior

- The CLI automatically resumes the latest saved session on startup
- Conversations are stored in `agent_memory.db` through LangGraph SQLite checkpoints
- `/status` shows saved sessions with their last-updated timestamps
- `/resume` lets you switch sessions without remembering ids
- `/new` creates a fresh session id like `session-1`, `session-2`, and so on

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `AGENT_PROVIDER` | `groq` | Provider name used by the app |
| `AGENT_MODEL` | `gpt-4o` | Model name to use |
| `AGENT_BASE_URL` | `None` | Custom API base URL (Ollama, vLLM, Groq) |
| `OPENAI_API_KEY` | `ollama` | API key |
| `AGENT_AUTO_APPROVE` | `false` | Skip tool approval prompts |
| `AGENT_MAX_TOKENS` | `4096` | Max tokens per response |

---

## Example Session

```
AKX CLI AGENT

Session: default
Saved messages: 18
Updated: 2026-04-18 23:58

default> /status

Provider      groq
Model         llama3-8b-8192
Base URL      https://api.groq.com/openai/v1
Max Tokens    4096
Auto Approve  False
Thread ID     default
Updated       2026-04-18 23:58

Saved Sessions
default       2026-04-18 23:58   current
session-1     2026-04-18 23:41

default> list the files in the current directory

Approval Required
Tool: list_dir
Args: {'path': '.'}
Run these tools? [Y/n]: y

main.py  config.py  memory.py  agent/  pyproject.toml

default> create a hello.py with a hello world script

Approval Required
Tool: write_file
Args: {'path': 'hello.py', 'content': 'print("Hello, world!")'}
Run these tools? [Y/n]: y

Done! hello.py has been created.

default> /resume

Resume session number: 2

session-1> run it

Approval Required
Tool: run_shell
Args: {'command': 'python hello.py'}
Run these tools? [Y/n]: y

Hello, world!
```

---

## Built-in Tools

| Tool | Description |
|---|---|
| `run_shell` | Run any bash/shell command |
| `read_file` | Read a file's contents |
| `write_file` | Write or create a file |
| `list_dir` | List files in a directory |

---

## Adding New Tools

Create a new file in `agent/tools/`, define a function with the `@tool` decorator, then add it to `registry.py`:

```python
# agent/tools/my_tool.py
from langchain_core.tools import tool

@tool
def my_tool(input: str) -> str:
    """Description of what this tool does."""
    return "result"
```

```python
# agent/tools/registry.py
from .my_tool import my_tool

ALL_TOOLS = [run_shell, read_file, write_file, list_dir, my_tool]
```

---

## Roadmap

- [ ] Streaming token output
- [ ] Web search tool
- [ ] Diff preview before file writes
- [ ] `--model` CLI flag to switch LLMs on the fly
- [ ] Token usage display

---

---
 
## Workflow
 
```mermaid
flowchart TD
    A([User Input]) --> B[AgentState]
    B --> C[call_llm node]
    C --> D{should_continue?}
    D -- has tool_calls --> E[Approval Gate]
    E -- approved --> F[ToolNode executor]
    E -- denied --> G[Inject cancel message]
    G --> C
    F --> C
    D -- no tool_calls --> H([END — print response])
 
    style A fill:#e1f5ee,stroke:#0f6e56
    style H fill:#e1f5ee,stroke:#0f6e56
    style E fill:#faeeda,stroke:#854f0b
    style F fill:#e1f5ee,stroke:#0f6e56
    style C fill:#e6f1fb,stroke:#185fa5
```
 
