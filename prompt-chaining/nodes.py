from state import GraphState
from langchain_core.language_models import BaseChatModel

class Nodes:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    def generate_joke(self, state: GraphState) -> dict:
        """LLM call to generate a joke."""
        msg = self.llm.invoke(f'Write a short joke about {state["topic"]}')
        return {"joke": msg.content}
    
    def improve_joke(self, state: GraphState) -> dict:
        """LLM call to improve the joke."""
        msg = self.llm.invoke(f'Make this joke funnier by adding wordplay and keep short: {state["joke"]}')
        return {"improved_joke": msg.content}

    def finalize_joke(self, state: GraphState) -> dict:
        """LLM call to finalize the joke."""
        msg = self.llm.invoke(f'Make this joke more funny by adding punchline: {state["improved_joke"]}')
        return {"final_joke": msg.content}

    def check_punchline(self, state: GraphState) -> str:
        """Gate function to check if the joke has a punchline."""
        if "?" in state["joke"] or "!" in state["joke"]:
            return "Pass"
        return "Fail"

