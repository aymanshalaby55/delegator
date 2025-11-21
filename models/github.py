from typing import Optional, List
from pydantic import BaseModel, Field


class GitHubRepoParticipantsInput(BaseModel):
    """Input for GitHub repo participants tool."""
    owner: str = Field(description="Repository owner/organization name")
    repo: str = Field(description="Repository name")


class GitHubCreateIssueInput(BaseModel):
    """Input for GitHub create issue tool."""
    owner: str = Field(description="Repository owner/organization name")
    repo: str = Field(description="Repository name")
    title: str = Field(description="Issue title")
    body: Optional[str] = Field(default="", description="Issue body/description")
    labels: Optional[List[str]] = Field(default=None, description="List of labels to add to the issue")
    assignees: Optional[List[str]] = Field(default=None, description="List of usernames to assign to the issue")


class GitHubGetIssuesInput(BaseModel):
    """Input for GitHub get issues tool."""
    owner: str = Field(description="Repository owner/organization name")
    repo: str = Field(description="Repository name")
    state: Optional[str] = Field(default="open", description="Issue state: 'open', 'closed', or 'all'")
    labels: Optional[str] = Field(default=None, description="Comma-separated list of labels to filter by")


class GitHubRepoInfoInput(BaseModel):
    """Input for GitHub repo info tool."""
    owner: str = Field(description="Repository owner/organization name")
    repo: str = Field(description="Repository name")
