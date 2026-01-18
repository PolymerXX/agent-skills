import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage

from .state import MultiAgentState

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="anthropic/claude-3.5-sonnet"
)


def supervisor(state: MultiAgentState) -> dict:
    """Supervisor agent that routes tasks to specialized agents."""
    system_prompt = """You are a supervisor managing a team of agents.
    Based on the conversation, decide which agent should handle the next step.
    Available agents: researcher, writer
    Respond with just the agent name, or 'FINISH' if the task is complete."""

    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    next_agent = response.content.strip().lower()

    if next_agent == "finish":
        return {"next_agent": "FINISH", "task_complete": True}
    return {"next_agent": next_agent}


def researcher(state: MultiAgentState) -> dict:
    """Research agent that gathers information."""
    system_prompt = """You are a research agent. Gather and analyze information
    based on the user's request. Provide detailed findings."""

    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [AIMessage(content=f"[Researcher] {response.content}")]}


def writer(state: MultiAgentState) -> dict:
    """Writer agent that creates content."""
    system_prompt = """You are a writing agent. Create well-structured content
    based on the research and user requirements."""

    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [AIMessage(content=f"[Writer] {response.content}")]}
