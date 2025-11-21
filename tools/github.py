from typing import Optional, List, Dict, Any
from langchain_core.tools import tool
from pydantic import BaseModel, Field
import requests
import os
from datetime import datetime
from models.github import GitHubRepoParticipantsInput

@tool
def github_repo_participants(owner: str, repo: str) -> str:
    """Get participants (contributors and collaborators) of a GitHub repository.
    
    Args:
        owner: Repository owner/organization name
        repo: Repository name
    
    Returns:
        String containing information about repository participants
    """
    # Hard-coded repository values
    # owner = "aymanshalaby55"
    # repo = "Chess-Mate"
    
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}
    
    try:
        # Get contributors
        contributors_url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
        contributors_response = requests.get(contributors_url, headers=headers)
        contributors_response.raise_for_status()
        contributors = contributors_response.json()
        
        # Get collaborators (requires push access)
        collaborators_url = f"https://api.github.com/repos/{owner}/{repo}/collaborators"
        collaborators_response = requests.get(collaborators_url, headers=headers)
        
        result = {
            "repository": f"{owner}/{repo}",
            "contributors": [
                {
                    "login": contributor["login"],
                    "contributions": contributor["contributions"],
                    "avatar_url": contributor["avatar_url"],
                    "html_url": contributor["html_url"]
                }
                for contributor in contributors[:20]  # Limit to top 20
            ],
            "total_contributors": len(contributors)
        }
        
        if collaborators_response.status_code == 200:
            collaborators = collaborators_response.json()
            result["collaborators"] = [
                {
                    "login": collab["login"],
                    "permissions": collab.get("permissions", {}),
                    "avatar_url": collab["avatar_url"],
                    "html_url": collab["html_url"]
                }
                for collab in collaborators
            ]
        
        return result
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching repository participants: {str(e)}"


# Export all tool
github_tools = github_repo_participants

