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
workflow.add_node('call_llm_1', nodes.call_llm1)
workflow.add_node('call_llm_2', nodes.call_llm2)
workflow.add_node('call_llm_3', nodes.call_llm3)
workflow.add_node('aggregator', nodes.aggregator)

print('Adding edges...')
workflow.add_edge(START, 'call_llm_1')
workflow.add_edge(START, 'call_llm_2')
workflow.add_edge(START, 'call_llm_3')
workflow.add_edge('call_llm_1', 'aggregator')
workflow.add_edge('call_llm_2', 'aggregator')
workflow.add_edge('call_llm_3', 'aggregator')
workflow.add_edge('aggregator', END)

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
        print('Agent:', state['combined_output'])
