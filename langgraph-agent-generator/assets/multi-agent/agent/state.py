from typing import Annotated, TypedDict, Literal
from langgraph.graph.message import add_messages


class MultiAgentState(TypedDict):
    """State for the multi-agent system."""
    messages: Annotated[list, add_messages]
    next_agent: str
    task_complete: bool
