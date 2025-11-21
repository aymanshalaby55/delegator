from markitdown import MarkItDown
import asyncio
from models.agentState import AgentState  

async def userInput(AgentState: AgentState) -> AgentState:
    md = MarkItDown(enable_plugins=False)  
    result = md.convert(AgentState.file_content)
    AgentState["file_content"] = result.text_content

    return AgentState

