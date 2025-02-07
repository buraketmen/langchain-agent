from state import GraphState
from schemas import RouterSchema
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models import BaseChatModel

class Nodes:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        # Augment the LLM with schema for structured output
        self.router = llm.with_structured_output(schema=RouterSchema)

    def llm_call_1(self, state: GraphState) -> dict:
        """Write a joke."""
        print("Writing a joke...")
        msg = self.llm.invoke(state["input"])
        return {"output": msg.content}

    def llm_call_2(self, state: GraphState) -> dict:
        """Write a story."""
        print("Writing a story...")
        msg = self.llm.invoke(state["input"])
        return {"output": msg.content}
    
    def llm_call_3(self, state: GraphState) -> dict:
        """Write a poem."""
        print("Writing a poem...")
        msg = self.llm.invoke(state["input"])
        return {"output": msg.content}

    def llm_call_router(self, state: GraphState) -> dict:
        """Route the input to the appropriate node."""

        # Run the augmented LLM with structured output to serve as routing logic
        decision: RouterSchema = self.router.invoke(
            [
                SystemMessage(content="Route the input to story, joke or poem based on the user's request."),
                HumanMessage(content=state["input"]),
            ]
        )
        return {"decision": decision.step}

    def route_decision(self, state: GraphState) -> str:
        """Route the input to the appropriate node."""
        if state["decision"] == "joke":
            return "llm_call_1"
        elif state["decision"] == "story":
            return "llm_call_2"
        elif state["decision"] == "poem":
            return "llm_call_3"
        else:
            raise ValueError(f"Invalid decision: {state['decision']}")