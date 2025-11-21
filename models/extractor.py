from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Task(BaseModel):
    assignee: str
    task: str
    deadline: Optional[str] = None
    priority: Optional[str] = None
    status: str = "pending"
    context: str

class GitHubIssue(BaseModel):
    title: str
    description: str
    labels: List[str] = []
    assignee: Optional[str] = None
    priority: Optional[str] = None

class SlackMessage(BaseModel):
    channel: str
    message: str
    urgency: str = "medium"
    context: str

class ExtractorData(BaseModel):
    file_content: str
    tasks: List[Task] = []
    github_issues: List[GitHubIssue] = []
    slack_messages: List[SlackMessage] = []
