from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    file_content: str
    tasks: list[dict]
    user_choice: str
    github_issues: list[dict]
    slack_messages: list[dict]
