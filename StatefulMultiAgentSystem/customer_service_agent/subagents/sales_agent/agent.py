from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def purchase_course(course_id: str, tool_context: ToolContext) -> dict:
    """
    Purchase the Introduction to AI Course. Update state with purchase information.
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get current purchased courses
    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    # Check if user already owns the course
    course_ids = [
        course["id"] for course in current_purchased_courses if isinstance(course, dict)
    ]
    if course_id in course_ids:
        return {"status": "error", "message": "You already own this course!"}

    # Create the new list with course added
    current_purchased_courses.append({"id": course_id, "purchase_datetime": current_time})
    tool_context.state["purchased_courses"] = current_purchased_courses

    return {
        "status": "success",
        "message": f"Successfully purchased AI course {course_id}",
        "course_id": course_id,
        "timestamp": current_time
    }


sales_agent = Agent(
    name="sales_agent",
    model="gemini-2.0-flash",
    description="Sales agent for the Introduction to AI Course",
    instruction="""
    You are a sales agent for the AI Learner community, specifically handling sales for the
    Introduction to AI, Advanced AI and Hands-on AI Project courses.

    <user_info>
    Name: {user_name}
    </user_info>

    <purchase_info>
    Purchased Courses: {purchased_courses}
    </purchase_info>

    Course 1 Details:
    - Name: Introduction to AI
    - Price: $49
    - Value Proposition: Learn to build AI basic knowledge
    - Includes: 6 weeks of lectures and exercises 

    Course 2 Details:
    - Name: Advanced AI
    - Price: $69
    - Value Proposition: Learn to advanced AI knowledge
    - Includes: 6 weeks of lectures and exercises 

    Course 3 Details
    - Name: Hands-on AI Project
    - Price: $89
    - Value Proposition: Build an advanced AI system
    - Includes: 6 weeks of AI project guidance 
    """,
    tools=[purchase_course]
)
