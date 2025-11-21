from pydantic import BaseModel, Field
from typing import Literal

class RouteToolInput(BaseModel):
    """Input model for routing tool selection."""
    query: str = Field(description="The user's query or request")

class RouteToolOutput(BaseModel):
    """Output model for routing tool selection."""
    tool: Literal["github"] = Field(description="The selected tool to handle the request") # here you can add what you want jira or slack.
    reasoning: str = Field(description="Explanation for why this tool was selected")
