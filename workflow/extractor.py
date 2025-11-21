import os
from langchain.chat_models import init_chat_model
from prompts.extraction_prompt import prompt
from models.agentState import AgentState
import dotenv
import json
from models.extractor import ExtractorData
dotenv.load_dotenv()
extractorLlm = init_chat_model("google_genai:gemini-2.0-flash")


async def extractor(state: AgentState) -> AgentState:
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": state["file_content"]}
    ]
    
    response = await extractorLlm.with_structured_output(ExtractorData).ainvoke(messages)
    
    # The response is already a structured ExtractorData object, no need to parse JSON
    state["tasks"] = [task.dict() for task in response.tasks]
    state["github_issues"] = [issue.dict() for issue in response.github_issues]
    state["slack_messages"] = [message.dict() for message in response.slack_messages]
    state["file_content"] = response.file_content
    
    print(state)
    return state


if __name__ == "__main__":
    import asyncio
    
    async def test_extractor():
        test_text = """
        Meeting Notes - Project Alpha
        Date: 2024-01-15
        
        Action Items:
        - John needs to complete the database schema by Friday
        - Sarah will review the UI mockups and provide feedback by Wednesday
        - Team meeting scheduled for next Monday at 2 PM
        
        Attendees: John Smith, Sarah Johnson, Mike Davis
        Location: Conference Room A
        """
        
        result = await extractor(test_text)
        print("Extraction Result:")
        print(result)
    
    asyncio.run(test_extractor())
