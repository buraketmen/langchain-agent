from state import GraphState
from schemas import Feedback
from langchain_core.language_models import BaseChatModel

class Nodes:
    def __init__(self, llm: BaseChatModel):
        self.llm: BaseChatModel = llm
        self.evaluator = llm.with_structured_output(Feedback)

    def llm_call_generator(self, state: GraphState) -> dict:
        """Generate a joke."""
        print('Agent: Generating joke...')
        if state.get('feedback'):
            msg = self.llm.invoke(
                f"Write a joke about {state['topic']} but take into account the feedback: {state['feedback']}"
            )
        else:
            msg = self.llm.invoke(
                f"Write a joke about {state['topic']}."
            )
        return {"joke": msg.content}

    def llm_call_evaluator(self, state: GraphState) -> dict:
        """Evaluate the joke."""
        print('Agent: Evaluating joke...')
        msg: Feedback = self.evaluator.invoke(
            f"Grade the joke: {state['joke']}."
        )
        return {"funny_or_not": msg.grade, "feedback": msg.feedback}

    def route_joke(self, state: GraphState) -> dict:
        """Route the joke to the appropriate function."""
        if state.get('funny_or_not') == 'funny':
            return "Accepted"
        return "Rejected + Feedback"