from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from tools import tools

LLM = ChatOllama(model="qwen2:7b") # Local model
print('Model loaded with Ollama.')


print('Initializing agent...')
agent = create_react_agent(model=LLM, tools=tools)

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