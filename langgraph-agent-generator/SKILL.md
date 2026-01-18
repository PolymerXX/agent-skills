---
name: langgraph-agent-generator
description: Generate LangGraph Agent boilerplate code with various patterns. Use when users ask to create an AI agent, build a LangGraph project, generate agent code, create a multi-agent system, or scaffold an agent workflow. Supports ReAct agents, multi-agent collaboration, and complex workflow patterns with OpenRouter as the default LLM provider.
---

# LangGraph Agent Generator

Generate production-ready LangGraph agent code with best practices.

## Workflow

1. Determine the agent pattern based on user requirements
2. Copy appropriate template from `assets/`
3. Customize for specific use case
4. Add required tools and nodes

## Pattern Selection

Choose the pattern based on complexity:

| Requirement | Pattern | Template |
|-------------|---------|----------|
| Single task with tools | ReAct Agent | `assets/react-agent/` |
| Multiple specialized agents | Multi-Agent | `assets/multi-agent/` |
| Complex branching logic | Workflow Agent | `assets/workflow-agent/` |

## Quick Start

For any agent project, start with:

```bash
pip install langgraph langchain-openai python-dotenv
```

Create `.env`:
```
OPENROUTER_API_KEY=your_key_here
```

## Pattern 1: ReAct Agent

Basic agent with tool calling. Best for single-purpose agents.

```python
import os
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI

class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize LLM with OpenRouter
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="anthropic/claude-3.5-sonnet"
)

# Define tools
tools = [your_tool_1, your_tool_2]
llm_with_tools = llm.bind_tools(tools)

def agent(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

def should_continue(state: State):
    last_message = state["messages"][-1]
    return "tools" if last_message.tool_calls else END

# Build graph
graph = StateGraph(State)
graph.add_node("agent", agent)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

app = graph.compile()
```

## Pattern 2: Multi-Agent (Supervisor)

Multiple agents coordinated by a supervisor. Best for complex tasks.

```python
from langgraph.graph import StateGraph, END

class MultiAgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str

def supervisor(state: MultiAgentState):
    response = supervisor_llm.invoke(state["messages"])
    return {"next_agent": response.content}

def researcher(state: MultiAgentState):
    return {"messages": [research_result]}

def writer(state: MultiAgentState):
    return {"messages": [written_content]}

def route(state: MultiAgentState):
    return state["next_agent"]

graph = StateGraph(MultiAgentState)
graph.add_node("supervisor", supervisor)
graph.add_node("researcher", researcher)
graph.add_node("writer", writer)
graph.set_entry_point("supervisor")
graph.add_conditional_edges("supervisor", route, {
    "researcher": "researcher",
    "writer": "writer",
    "FINISH": END
})
graph.add_edge("researcher", "supervisor")
graph.add_edge("writer", "supervisor")

app = graph.compile()
```

## Pattern 3: Workflow Agent

Complex workflows with conditional branching and loops.

```python
class WorkflowState(TypedDict):
    messages: Annotated[list, add_messages]
    step: str
    retries: int

def step_1(state: WorkflowState):
    return {"step": "step_2", "messages": [...]}

def step_2(state: WorkflowState):
    success = process_data()
    if success:
        return {"step": "complete"}
    return {"step": "retry", "retries": state["retries"] + 1}

def should_retry(state: WorkflowState):
    if state["step"] == "retry" and state["retries"] < 3:
        return "step_1"
    elif state["step"] == "complete":
        return END
    return state["step"]

graph = StateGraph(WorkflowState)
graph.add_node("step_1", step_1)
graph.add_node("step_2", step_2)
graph.set_entry_point("step_1")
graph.add_edge("step_1", "step_2")
graph.add_conditional_edges("step_2", should_retry)

app = graph.compile()
```

## Project Structure

Generate this structure for production projects:

```
my-agent/
├── .env
├── requirements.txt
├── agent/
│   ├── __init__.py
│   ├── graph.py        # Main graph definition
│   ├── state.py        # State definitions
│   ├── nodes.py        # Node functions
│   └── tools.py        # Tool definitions
└── main.py
```

## Resources

- **Templates**: See `assets/` for complete project templates
- **API Reference**: See `references/langgraph-api.md` for LangGraph API details
