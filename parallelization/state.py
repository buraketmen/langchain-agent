from typing_extensions import TypedDict

class GraphState(TypedDict):
    topic: str
    joke: str
    story: str
    poem: str
    combined_output: str