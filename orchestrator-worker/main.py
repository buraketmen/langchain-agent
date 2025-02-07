from langchain_ollama import ChatOllama
from langgraph.constants import Send
from langgraph.graph import StateGraph, START, END
from state import GraphState
from nodes import Nodes

LLM = ChatOllama(model="qwen2:7b", temperature=0) # Local model
print('Model loaded with Ollama.')


nodes = Nodes(llm=LLM)

def assign_workers(state: GraphState):
    """Assign worker to each section in the plan."""
    return [Send("llm_call", {"section": s}) for s in state["sections"]]


print('Initializing workflow...')
workflow = StateGraph(GraphState)

print('Adding nodes...')
workflow.add_node("orchestrator", nodes.orchestrator)
workflow.add_node("llm_call", nodes.llm_call)
workflow.add_node("synthesizer", nodes.synthesizer)

print('Adding edges...')
workflow.add_edge(START, "orchestrator")
workflow.add_conditional_edges("orchestrator", assign_workers, ["llm_call"]) # Assign workers to each section
workflow.add_edge("llm_call", "synthesizer")
workflow.add_edge("synthesizer", END)

chain = workflow.compile()
if __name__ == '__main__':
    print("Workflow initialized. Type 'exit' to quit.\n")
    print('Samples:')
    print('- Create a report about on the benefits of AI.')
    print('- Create a report about on the history of AI.')
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        state = chain.invoke({"topic": user_input})
        print('Agent:', state['final_report'])
