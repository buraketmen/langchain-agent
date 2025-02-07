from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage
from nodes import Nodes

LLM = ChatOllama(model="qwen2:7b") # Local model
print('Model loaded with Ollama.')

nodes = Nodes(llm=LLM)

print('Initializing agent...')
agent_builder = StateGraph(MessagesState)

print('Adding nodes...')
agent_builder.add_node("llm_call", nodes.llm_call)
agent_builder.add_node("environment", nodes.tool_node)

print('Adding edges...')
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    nodes.should_continue,
    {
        "Action": "environment",
        "Reply": END
    }
)
agent_builder.add_edge("environment", "llm_call")

agent = agent_builder.compile()

if __name__ == '__main__':
    print("Agent initialized. Type 'exit' to quit.\n")
    print('Samples:')
    print('- Add 3 and 4.')
    print('- Multiply 3 and 4.')
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        result = agent.invoke({"messages": [HumanMessage(content=user_input)]})
        print('Agent:', result["messages"][-1].content)