from typing import Literal
from langchain_core.language_models import BaseChatModel
from langgraph.graph import MessagesState, END
from langchain_core.messages import SystemMessage, ToolMessage
from tools import tools_by_name, tools

class Nodes:
    def __init__(self, llm: BaseChatModel):
        self.llm: BaseChatModel = llm
        self.llm_with_tools = llm.bind_tools(tools=tools)

    def llm_call(self, state: MessagesState) -> dict:
        """Decide whether to call a tool or not."""
        print('calling llm')
        return {
            "messages": [
                self.llm_with_tools.invoke(
                    [
                        SystemMessage(
                            content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
                        )
                    ]
                    + state['messages']
                )
            ]
        }
    
    def tool_node(self, state: dict):
        """Call a tool."""
        result = []
        for tool_call in state["messages"][-1].tool_calls:
            tool = tools_by_name[tool_call["name"]]
            print(f"Agent: Calling tool ({tool.name}) with args {tool_call['args']}")
            observation = tool.invoke(tool_call["args"])
            result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
        return {"messages": result}

    @staticmethod
    def should_continue(state: MessagesState) -> Literal["Action", "Reply"]:
        messages = state["messages"]
        last_message = messages[-1]
        # If the LLM makes a tool call, then perform an action
        if last_message.tool_calls:
            return "Action"
        # Otherwise, we stop (reply to the user)
        return "Reply"