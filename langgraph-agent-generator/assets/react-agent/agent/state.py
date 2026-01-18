from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State for the ReAct agent."""
    messages: Annotated[list, add_messages]
