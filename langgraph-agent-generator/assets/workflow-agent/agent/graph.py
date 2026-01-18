from langgraph.graph import StateGraph, END

from .state import WorkflowState
from .nodes import initialize, process, validate, handle_error, complete


def route_workflow(state: WorkflowState) -> str:
    """Route to the next step based on current state."""
    step = state.get("current_step", "initialize")

    if step in ["done", "failed"]:
        return END
    return step


def create_workflow_agent():
    """Create a workflow agent with conditional branching and retry logic."""

    graph = StateGraph(WorkflowState)

    # Add nodes
    graph.add_node("initialize", initialize)
    graph.add_node("process", process)
    graph.add_node("validate", validate)
    graph.add_node("handle_error", handle_error)
    graph.add_node("complete", complete)

    # Set entry point
    graph.set_entry_point("initialize")

    # Add edges
    graph.add_edge("initialize", "process")
    graph.add_conditional_edges(
        "process",
        route_workflow,
        {
            "validate": "validate",
            "handle_error": "handle_error",
            END: END
        }
    )
    graph.add_conditional_edges(
        "validate",
        route_workflow,
        {
            "complete": "complete",
            "handle_error": "handle_error",
            END: END
        }
    )
    graph.add_conditional_edges(
        "handle_error",
        route_workflow,
        {
            "process": "process",
            "failed": END,
            END: END
        }
    )
    graph.add_edge("complete", END)

    return graph.compile()
