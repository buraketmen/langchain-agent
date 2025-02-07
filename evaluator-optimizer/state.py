from typing_extensions import TypedDict

class GraphState(TypedDict):
    joke: str # Joke
    topic: str # Report topic
    feedback: str # Feedback
    funny_or_not: str 