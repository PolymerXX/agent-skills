from langchain_core.tools import tool


@tool
def search(query: str) -> str:
    """Search for information on the web."""
    # TODO: Implement actual search logic
    return f"Search results for: {query}"


@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


# Add your custom tools here
TOOLS = [search, calculator]
