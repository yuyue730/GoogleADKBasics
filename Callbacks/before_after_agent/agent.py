from datetime import datetime
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """Callback that logs when the agent starts processing a request.
    
    Args:
        callback_context: Contains state and context information.

    Returns:
        None to continue with normal agent processing.
    """
    # Get session state and timestamp
    state = callback_context.state
    timestamp = datetime.now()

    # Set agent name if not present
    if "agent_name" not in state:
        state["agent_name"] = "SimpleChatBot"

    # Initialize request counter if necessary and increment it
    if "request_count" not in state:
        state["request_count"] = 0
    state["request_count"] += 1

    # Store the start time
    state["request_start_time"] = timestamp

    # Log the request
    print("=== Before Agent Execution Starts ===")
    print(f"Request Count: {state['request_count']}")
    print(f"Request Start Time: {state['request_start_time']}")

    return None

def after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """Callback that logs when the agent finishes processing a request.

    Args:
        callback_context: Contains state and context information.

    Returns:
        None to continue with normal agent processing.
    """
    # Get session state and timestamp
    state = callback_context.state
    timestamp = datetime.now()

    # Log the request duration
    duration = None
    if "request_start_time" in state:
        duration = timestamp - state["request_start_time"]

    print("=== After Agent Execution Ends ===")
    print(f"Request #: {state.get('request_count', 'Unknown')}")
    if duration is not None:
        print(f"Request Duration: {duration:.2f} seconds")

    return None

root_agent = LlmAgent(
    name="before_after_agent",
    model="gemini-2.0-flash",
    description="An agent that demonstrates before and after agent callbacks",
    instruction="""
    You are a friendly greeting agent. Your name is {agent_name}.

    You job is to:
    - Greet the user with a friendly message
    - Respond to basic questions
    - Keep your response friendly and concise
    """,
    before_agent_callback=before_agent_callback,)