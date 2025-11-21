from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv  
from langchain_core.messages import BaseMessage # The foundational class for all message types in LangGraph
from langchain_core.messages import ToolMessage # Passes data back to LLM after it calls a tool such as the content and the tool_call_id
from langchain_core.messages import SystemMessage # Message for providing instructions to the LLM
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END,START
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
@tool
def add(a : int , b:int):
    """this is addition function that add 2 num"""
    return a + b

tools = [add]

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash").bind_tools(tools)

def model_call(state: AgentState) -> AgentState: 
    system_prompt = SystemMessage(content="You are a helpful assistant that can add two numbers")
    response = model.invoke([system_prompt + state["messages"]])
    return {"messages": [response]}


def should_continue(state: AgentState): 
    messages = state["messages"]
    last_message = messages[-1]
    print(last_message)
    if last_message.tool_calls:
        return "end"
    else:
        return "continue"

graph = StateGraph(AgentState)

graph.add_node("agent", model_call)

tool_node = ToolNode(tools=tools)

graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")


# conditional edge
graph.add_conditional_edges(
    "agent", should_continue, {
        "continue": "tools",
        "end": END
    })

#looping edge
graph.add_edge("agent", "tools")

app = graph.compile()



def print_stream(stream): 
    for s in stream: 
        message = s["messages"][-1]
        if(message.tool_calls):
            print(message.tool_calls)
        else:
            print(message.pretty_print())

print_stream(app.stream({"messages": [SystemMessage(content="What is the sum of 1 and 2?")]}))