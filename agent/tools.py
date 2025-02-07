from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply a by b.
    Args:
        a: The first number.
        b: The second number.
    """
    return a * b

@tool
def add(a: int, b: int) -> int:
    """
    Add a to b.
    Args:
        a: The first number.
        b: The second number.
    """
    return a + b

@tool
def divide(a: int, b: int) -> int:
    """
    Divide a by b.
    Args:
        a: The first number.
        b: The second number.
    """
    return a / b

tools = [multiply, add, divide]
tools_by_name = {tool.name: tool for tool in tools}