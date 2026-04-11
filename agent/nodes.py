from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import END
from .state import AgentState
from .tools.registry import ALL_TOOLS
import config

def make_llm():
    kwargs = dict(model=config.MODEL, api_key=config.API_KEY, max_tokens=config.MAX_TOKENS)
    if config.BASE_URL:
        kwargs["base_url"] = config.BASE_URL
    return ChatOpenAI(**kwargs).bind_tools(ALL_TOOLS)

llm = make_llm()

def call_llm(state: AgentState) -> dict:
    """The main LLM node — prepends system prompt, calls the model."""
    messages = [SystemMessage(content=config.SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    """Router: if the last message has tool calls → go to tools, else → END."""
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END