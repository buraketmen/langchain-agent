from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from state import RouterState
from schemas import RouterSchema
from nodes import Nodes

LLM = ChatOllama(model="qwen2:7b") # Local model
print('Model loaded with Ollama.')

# Augment the LLM with schema for structured output
router = LLM.with_structured_output(schema=RouterSchema)

nodes = Nodes(llm=LLM, router=router)

print('Initializing workflow...')
workflow = StateGraph(RouterState)

print('Adding nodes...')
workflow.add_node('llm_call_1', nodes.llm_call_1)
workflow.add_node('llm_call_2', nodes.llm_call_2)
workflow.add_node('llm_call_3', nodes.llm_call_3)
workflow.add_node('llm_call_router', nodes.llm_call_router)

print('Adding edges...')
workflow.add_edge(START, 'llm_call_router')
workflow.add_conditional_edges('llm_call_router', nodes.route_decision, {
    'llm_call_1': 'llm_call_1',
    'llm_call_2': 'llm_call_2',
    'llm_call_3': 'llm_call_3'
})
workflow.add_edge('llm_call_1', END)
workflow.add_edge('llm_call_2', END)
workflow.add_edge('llm_call_3', END)

print('Compiling workflow...')
chain = workflow.compile()
if __name__ == '__main__':
    print("Workflow initialized. Type 'exit' to quit.\n")
    print('Samples:')
    print('- Write me a joke about cats.')
    print('- Write me a story about dogs.')
    print('- Write me a poem about birds.\n\n')
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        state = chain.invoke({"input": user_input})
        print('Agent:', state['output'])
