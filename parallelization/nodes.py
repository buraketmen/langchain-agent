from state import GraphState
from langchain_core.language_models import BaseChatModel

class Nodes:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    def call_llm1(self, state: GraphState) -> dict:
        """First LLM call to generate initial joke."""
        msg = self.llm.invoke(f'Write a short joke about {state["topic"]}')
        return {"joke": msg.content}

    def call_llm2(self, state: GraphState) -> dict:
        """Second LLM call to generate story."""
        msg = self.llm.invoke(f'Write a short storyy about: {state["topic"]}')
        return {"story": msg.content}
    
    def call_llm3(self, state: GraphState) -> dict:
        """Third LLM call to generate poem."""
        msg = self.llm.invoke(f'Write a short poem about: {state["topic"]}')
        return {"poem": msg.content}

    def aggregator(self, state: GraphState) -> dict:
        """Aggregator function to combine outputs."""
        combined = f"Here is a story, joke and poem about {state["topic"]}\n\n"
        combined += f"Story:\n {state["story"]}\n\n"
        combined += f"Joke:\n {state["joke"]}\n\n"
        combined += f"Poem:\n {state["poem"]}\n\n"
        return {"combined_output": combined}