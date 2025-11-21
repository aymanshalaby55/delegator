from typing import Annotated

from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from  tools.github import github_tools
import dotenv
dotenv.load_dotenv()
class State(TypedDict):
    messages: Annotated[list, add_messages]
    github_participants : list[str]
    pending_tool_call: dict | None

graph_builder = StateGraph(State)

from langchain.chat_models import init_chat_model

llm = init_chat_model("google_genai:gemini-2.0-flash")

tool = TavilySearch(
    max_results=1,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=False,
    include_images=True
)

tools = [tool]
llm_with_tools = llm

async def chatbot(state: State):
    response = await llm_with_tools.ainvoke(state["messages"])
    
    # Check if the response contains tool calls for GitHub participants
   
    
    return {
        "messages": [response],
    }
    

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")

memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)


import asyncio

async def main():
    res = await graph.ainvoke(
        {"messages": [{"role": "user", "content": "what is the new in react 19"}]},
        config={"configurable": {"thread_id": "1"}}
    )
    return res

res = asyncio.run(main())

for message in res["messages"]:
    print(f"Role: {message.type}")
    print(f"Content: {message.content}")
    print("-" * 50)