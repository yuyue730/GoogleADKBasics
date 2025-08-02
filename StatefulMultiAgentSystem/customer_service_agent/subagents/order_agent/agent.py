from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def get_current_time() -> dict:
    """Get the current time in a formatted string."""
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def refund_course(course_id: str, tool_context: ToolContext) -> dict:
    """
    Process a refund for the purchased course. Update state with refund information.

    Args:
    course_id: The ID of the course to refund.
    tool_context: The context containing the current state.

    Returns:
    A dictionary with the status of the refund operation.
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get current purchased courses
    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    # Check if user owns the course
    course_ids = [
        course["id"] for course in current_purchased_courses if isinstance(course, dict)
    ]
    if course_id not in course_ids:
        return {
            "status": "error",
            "message": "You do not own this course, so it cannot be refunded!"
        }

    # Remove the course from the purchased courses
    updated_courses = [
        course for course in current_purchased_courses if course.get("id") != course_id
    ]
    tool_context.state["purchased_courses"] = updated_courses

    # Add refund information to interaction history
    current_interaction_history = tool_context.state.get("interaction_history", [])
    new_interaction_history = current_interaction_history.copy()
    new_interaction_history.append({
        "action": "refund_course",
        "course_id": course_id,
        "timestamp": current_time,
    })
    tool_context.state["interaction_history"] = new_interaction_history

    return {
        "status": "success",
        "message": f"Successfully refunded AI course {course_id}",
        "course_id": course_id,
        "timestamp": current_time
    }

order_agent = Agent(
    name="order_agent",
    model="gemini-2.0-flash",
    description="Order agent for viewing history and process refunding",
    instruction="""
    You are an order agent for the AI Learner community, specifically helping users view their
    purchase history, course access, and process refunds.

    <user_info>
    Name: {user_name}
    </user_info>

    <purchase_info>
    Purchased Courses: {purchased_courses}
    </purchase_info>

    <interaction_history>
    Interaction History: {interaction_history}
    </interaction_history>

    When users ask about their purchases history
    1. Check their course list from the purchase_info.
      - Course information is stored as objects with "id" and "purchase_datetime".
    2. Format the response clearly showing:
      - Which courses the user has purchased
      - wHEN they purchased each course

    When users request a refund:
    1. Check if the user has purchased the course.
    2. If they own the course:
      - Use the refund_course tool to process the refund.
      - Confirm the refund was successful.
      - If it has been more than 30 days since purchase, inform the user that refunds are not
      available.
    3. If they do not own the course:
      - Inform the user that they cannot refund a course they do not own.

    Course Information:
    - Course 1: "Introduction to AI" ($49)
    - Course 2: "Advanced AI" ($69)
    - Course 3: "Hands-on AI Project" ($89)

    Remember:
    - Be clear and professional in your responses.
    - Mention 30-day refund policy if relevant.
    - Direct course questions to the course support agent.
    - Direct purchase questions to the sales agent.
    """,
    tools=[refund_course]
)
