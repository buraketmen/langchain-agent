from typing_extensions import TypedDict

class JokeState(TypedDict):
    topic: str
    joke: str
    story: str
    poem: str
    combined_output: str