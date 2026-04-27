import os
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("AGENT_MODEL") or os.getenv("MODEL", "gpt-4o")
BASE_URL = os.getenv("AGENT_BASE_URL")
API_KEY = (
      os.getenv("OPENAI_API_KEY")
      or os.getenv("GROQ_API_KEY")
      or os.getenv("API_KEY", "ollama")
  )
AUTO_APPROVE = os.getenv("AGENT_AUTO_APPROVE", "false").lower() == "true"
MAX_TOKENS = int(os.getenv("AGENT_MAX_TOKENS") or os.getenv("MAX_TOKENS", "4096"))
PROVIDER = os.getenv("AGENT_PROVIDER", "groq")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

SYSTEM_PROMPT = """You are a powerful coding assistant with access to the user's terminal and filesystem.
  - Think step by step before using tools
  - Use tools only when they are necessary to complete the user's request
  - Use web_search for current events, recent news, or anything that requires internet lookup
  - Do not use run_shell for web/news lookup unless the user explicitly asks for a shell command
  - Do not use tools for casual chat, acknowledgements, compliments, or slash commands handled by the CLI
  - Prefer reading files before editing them
  - Always show what you're about to do before doing it
  - Be concise in your final answers"""
