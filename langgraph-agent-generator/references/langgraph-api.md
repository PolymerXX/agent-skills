# LangGraph API Reference

## Core Concepts

### StateGraph
The main class for building agent graphs.

```python
from langgraph.graph import StateGraph, END

graph = StateGraph(StateType)
```

### State Definition
Use TypedDict with Annotated for message accumulation:

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    custom_field: str
```

## Graph Methods

| Method | Description |
|--------|-------------|
| `add_node(name, fn)` | Add a node with a function |
| `add_edge(from, to)` | Add a direct edge |
| `add_conditional_edges(from, fn, mapping)` | Add conditional routing |
| `set_entry_point(name)` | Set the starting node |
| `compile()` | Compile the graph to an executable |

## Prebuilt Components

### ToolNode
Automatically handles tool execution:

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode(tools)
graph.add_node("tools", tool_node)
```

### create_react_agent
Quick ReAct agent creation:

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(llm, tools)
```

## Conditional Edges

Route based on state:

```python
def router(state):
    if condition:
        return "node_a"
    return "node_b"

graph.add_conditional_edges(
    "source_node",
    router,
    {"node_a": "node_a", "node_b": "node_b", END: END}
)
```

## Checkpointing

Enable state persistence:

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app = graph.compile(checkpointer=memory)

# Invoke with thread_id
result = app.invoke(input, config={"configurable": {"thread_id": "1"}})
```

## Common Patterns

### Tool Calling Loop
```python
def should_continue(state):
    if state["messages"][-1].tool_calls:
        return "tools"
    return END
```

### Human-in-the-Loop
```python
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# Compile with interrupt
app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["human_review"]
)
```

## OpenRouter Integration

Configure ChatOpenAI for OpenRouter:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="anthropic/claude-3.5-sonnet"  # or other models
)
```

Available models via OpenRouter:
- `anthropic/claude-3.5-sonnet`
- `anthropic/claude-3-opus`
- `openai/gpt-4-turbo`
- `openai/gpt-4o`
- `google/gemini-pro`
- `meta-llama/llama-3-70b-instruct`
