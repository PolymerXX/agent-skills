import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage

from .state import WorkflowState

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="anthropic/claude-3.5-sonnet"
)

MAX_RETRIES = 3


def initialize(state: WorkflowState) -> dict:
    """Initialize the workflow."""
    return {
        "current_step": "process",
        "retries": 0,
        "data": {},
        "error": None
    }


def process(state: WorkflowState) -> dict:
    """Main processing step."""
    try:
        messages = state["messages"]
        response = llm.invoke(messages)

        return {
            "messages": [AIMessage(content=response.content)],
            "current_step": "validate",
            "data": {"result": response.content}
        }
    except Exception as e:
        return {
            "current_step": "handle_error",
            "error": str(e)
        }


def validate(state: WorkflowState) -> dict:
    """Validate the processing result."""
    data = state.get("data", {})

    # Add your validation logic here
    is_valid = data.get("result") is not None

    if is_valid:
        return {"current_step": "complete"}
    else:
        return {"current_step": "handle_error", "error": "Validation failed"}


def handle_error(state: WorkflowState) -> dict:
    """Handle errors with retry logic."""
    retries = state.get("retries", 0)

    if retries < MAX_RETRIES:
        return {
            "current_step": "process",
            "retries": retries + 1,
            "error": None
        }
    else:
        return {
            "current_step": "failed",
            "messages": [AIMessage(content=f"Workflow failed after {MAX_RETRIES} retries: {state.get('error')}")]
        }


def complete(state: WorkflowState) -> dict:
    """Complete the workflow successfully."""
    return {
        "messages": [AIMessage(content="Workflow completed successfully!")],
        "current_step": "done"
    }
