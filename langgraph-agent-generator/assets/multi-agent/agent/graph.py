from langgraph.graph import StateGraph, END

from .state import MultiAgentState
from .nodes import supervisor, researcher, writer


def route_to_agent(state: MultiAgentState) -> str:
    """Route to the next agent based on supervisor decision."""
    next_agent = state.get("next_agent", "supervisor")
    if next_agent == "FINISH":
        return END
    return next_agent


def create_multi_agent():
    """Create a multi-agent system with supervisor pattern."""

    graph = StateGraph(MultiAgentState)

    # Add nodes
    graph.add_node("supervisor", supervisor)
    graph.add_node("researcher", researcher)
    graph.add_node("writer", writer)

    # Set entry point
    graph.set_entry_point("supervisor")

    # Add edges
    graph.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "researcher": "researcher",
            "writer": "writer",
            END: END
        }
    )
    graph.add_edge("researcher", "supervisor")
    graph.add_edge("writer", "supervisor")

    return graph.compile()
