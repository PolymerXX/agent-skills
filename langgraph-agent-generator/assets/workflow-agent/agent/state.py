from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import add_messages


class WorkflowState(TypedDict):
    """State for the workflow agent."""
    messages: Annotated[list, add_messages]
    current_step: str
    retries: int
    data: Optional[dict]
    error: Optional[str]
