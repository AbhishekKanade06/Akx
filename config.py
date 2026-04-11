import os

MODEL        = os.getenv("AGENT_MODEL", "gpt-4o")
BASE_URL     = os.getenv("AGENT_BASE_URL", None)      # set for Ollama/vLLM/Groq
API_KEY      = os.getenv("OPENAI_API_KEY", "ollama")
AUTO_APPROVE = os.getenv("AGENT_AUTO_APPROVE", "false").lower() == "true"
MAX_TOKENS   = int(os.getenv("AGENT_MAX_TOKENS", "4096"))

SYSTEM_PROMPT = """You are a powerful coding assistant with access to the user's terminal and filesystem.
- Think step by step before using tools
- Prefer reading files before editing them
- Always show what you're about to do before doing it
- Be concise in your final answers"""