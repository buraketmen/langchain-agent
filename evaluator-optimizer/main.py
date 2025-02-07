from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from state import GraphState
from nodes import Nodes

LLM = ChatOllama(model="qwen2:7b") # Local model
print('Model loaded with Ollama.')

nodes = Nodes(llm=LLM)

print('Initializing workflow...')
workflow = StateGraph(GraphState)

print('Adding nodes...')
workflow.add_node("llm_call_generator", nodes.llm_call_generator)
workflow.add_node("llm_call_evaluator", nodes.llm_call_evaluator)


print('Adding edges...')
workflow.add_edge(START, "llm_call_generator")
workflow.add_edge("llm_call_generator", "llm_call_evaluator")
workflow.add_conditional_edges(
    'llm_call_evaluator',
    nodes.route_joke,
    {
        "Accepted": END,
        "Rejected + Feedback": "llm_call_generator"
    }
)

chain = workflow.compile()
if __name__ == '__main__':
    print("Workflow initialized. Type 'exit' to quit.\n")
    print('Agent: Give me a topic to make a joke about.')
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        state = chain.invoke({"topic": user_input})
        print('Agent:', state['joke'])
