from typing_extensions import TypedDict

class RouterState(TypedDict):
    input: str # The input from the user
    decision: str # The decision made by the router
    output: str # The output from the LLM
    