import asyncio
from workflow.extractor import extractor
import dotenv
dotenv.load_dotenv()

async def test_extractor_agent():
    """Test the extractor agent with various types of content."""
    
    # Test case 1: Meeting notes with tasks and deadlines
    test_text_1 = """
    Meeting Notes - Sprint Planning
    Date: 2024-01-20
    
    Action Items:
    - Alice needs to implement user authentication by January 25th (HIGH PRIORITY)
    - Bob will fix the login bug reported in GitHub issue #123 by end of week
    - Carol should send update to #dev-team channel about API changes
    - Team needs to review pull request #456 before Monday
    
    Issues to track:
    - Login form validation is broken - needs immediate attention
    - Performance optimization for dashboard loading
    - Add dark mode toggle to settings page
    
    Follow-up communications:
    - Notify stakeholders about deployment delay in #general channel
    - Send meeting summary to project-alpha@company.com
    """
    
    # Test case 2: Bug report with GitHub issues
    test_text_2 = """
    Bug Report Summary
    
    Critical Issues Found:
    1. Database connection timeout - assign to DevOps team, high priority
    2. Memory leak in image processing module - needs investigation
    3. API rate limiting not working correctly
    
    Tasks:
    - John to investigate memory leak issue by Wednesday
    - Sarah to update documentation for new API endpoints
    - Send status update to #engineering channel about critical bugs
    """
    
    # Test case 3: Project update with mixed content
    test_text_3 = """
    Weekly Project Update - Q1 2024
    
    Completed:
    - User registration flow implemented
    - Database migration completed successfully
    
    In Progress:
    - Payment integration (Mike working on it, due Friday)
    - Mobile app testing (QA team, ongoing)
    
    Upcoming:
    - Create GitHub issue for mobile push notifications feature
    - Schedule demo for stakeholders next week
    - Post update in #product-updates about Q1 progress
    """
    
    test_cases = [
        ("Meeting Notes Test", test_text_1),
        ("Bug Report Test", test_text_2),
        ("Project Update Test", test_text_3)
    ]
    
    for test_name, test_text in test_cases:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print(f"{'='*50}")
        print(f"Input text:\n{test_text[:200]}...")
        print(f"\n{'-'*30}")
        print("Extraction Result:")
        
        try:
            # Create AgentState with the test text
            state = {
                "messages": [],
                "file_content": test_text,
                "tasks": [],
                "user_choice": "",
                "github_issues": [],
                "slack_messages": []
            }
            result = await extractor(state)
            print(result)
        except Exception as e:
            print(f"Error during extraction: {e}")
        
        print(f"{'-'*30}\n")


if __name__ == "__main__":
    asyncio.run(test_extractor_agent())
