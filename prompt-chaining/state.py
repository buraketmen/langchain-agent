from typing_extensions import TypedDict

class JokeState(TypedDict):
    topic:str
    joke: str
    improved_joke: str
    final_joke: str