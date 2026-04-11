from langgraph.checkpoint.sqlite import SqliteSaver  # update this line
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from .state import AgentState
from .nodes import call_llm, should_continue
from .tools.registry import ALL_TOOLS
import config

def build_graph(memory):
    graph = StateGraph(AgentState)

    graph.add_node("llm",   call_llm)
    graph.add_node("tools", ToolNode(ALL_TOOLS))

    graph.set_entry_point("llm")
    graph.add_conditional_edges("llm", should_continue)
    graph.add_edge("tools", "llm")

    interrupt = [] if config.AUTO_APPROVE else ["tools"]

    return graph.compile(checkpointer=memory, interrupt_before=interrupt)