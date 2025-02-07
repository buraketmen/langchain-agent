from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply a by b.
    Args:
        a: The first number.
        b: The second number.
    """
    print(f"Agent: Calling tool (multiply) with args a:{a} and b:{b}")
    return a * b

@tool
def add(a: int, b: int) -> int:
    """
    Add a to b.
    Args:
        a: The first number.
        b: The second number.
    """
    print(f"Agent: Calling tool (add) with args a:{a} and b:{b}")
    return a + b

@tool
def divide(a: int, b: int) -> int:
    """
    Divide a by b.
    Args:
        a: The first number.
        b: The second number.
    """
    print(f"Agent: Calling tool (divide) with args a:{a} and b:{b}")
    return a / b

tools = [multiply, add, divide]
