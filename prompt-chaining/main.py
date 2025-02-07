from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from state import JokeState
from nodes import Nodes

LLM = ChatOllama(model="qwen2:7b") # Local model
print('Model loaded with Ollama.')
nodes = Nodes(llm=LLM)

print('Initializing workflow...')
workflow = StateGraph(state_schema=JokeState)

print('Adding nodes...')
workflow.add_node('generate_joke', nodes.generate_joke)
workflow.add_node('improve_joke', nodes.improve_joke)
workflow.add_node('finalize_joke', nodes.finalize_joke)

print('Adding edges...')
workflow.add_edge(START, 'generate_joke')
workflow.add_conditional_edges(
    'generate_joke', nodes.check_punchline, {"Pass": "improve_joke", "Fail": END}
)
workflow.add_edge('improve_joke', 'finalize_joke')
workflow.add_edge('finalize_joke', END)

print('Compiling workflow...')
chain = workflow.compile()

if __name__ == '__main__':
    print("Workflow initialized. Type 'exit' to quit.")
    print('Agent: Give me a topic to make a joke about.')
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        state = chain.invoke({"topic": user_input})
        print('Agent:', state['initial_joke'] if 'improved_joke' not in state else state['final_joke'])