from datetime import datetime
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types

def before_model_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Runs before the model processes a request by filtering inappropriate content and logs
    request information.

    Args:
        callback_context: Contains state and context information.
        llm_request: The request to the model.

    Returns:
        Optional LlmResponse to override model response.
    """
    # Get session state and agent name
    state = callback_context.state
    agent_name = callback_context.agent_name

    # Extract the last user message from the request
    last_user_message = ""
    if llm_request.contents and len(llm_request.contents) > 0:
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts and len(content.parts) > 0:
                if hasattr(content.parts[0], "text") and content.parts[0].text:
                    last_user_message = content.parts[0].text
                    break

    # Log the request details
    print("=== Before Request Sent to LLM ===")
    print(f"Agent Name: {agent_name}")
    if last_user_message:
        print(f"Last User Message: {last_user_message}")
    else:
        print("User message: <empty>")

    # Check for inappropriate content
    if last_user_message and "sucks" in last_user_message.lower():
        print("=== INAPPROPRIATE CONTENT DETECTED ===")
        print("Blocking request due to content containing sucks.")
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="I cannot respond to messages containing sucks. "
                                 "Please rephrase your input without using words like 'sucks'."
                    )
                ],
            )
        )

    # Return None to continue processing
    return None

def after_model_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """Runs after the model processes a request to replace negative words with more positive
    alternatives.

    Args:
        callback_context: Contains state and context information.
        llm_response: The response from the model.

    Returns:
        Optional LlmResponse to override model response.
    """
    print("=== After Response Received from LLM ===")
    print(f"llm_response: {llm_response}")

    # Skip processing if no response parts are present
    if not llm_response or not llm_response.content or not llm_response.content.parts:
        print("No response parts to process.")
        return None

    # Get session state and timestamp
    response_text = ""
    for part in llm_response.content.parts:
        if hasattr(part, "text") and part.text:
            response_text += part.text

    print(f"Response Text: {response_text}")
    if not response_text:
        print("Response text is empty.")
        return None
    
    # Replacement definitions
    replacements = {
        "problem": "challenge",
        "difficult": "complex",
    }

    # Perform replacements
    modified_text = response_text
    modified = False

    for original, replacement in replacements.items():
        if original in modified_text.lower():
            print(f"Current text: {modified_text}")
            modified_text = modified_text.replace(original, replacement)
            modified_text = modified_text.replace(original.capitalize(), replacement.capitalize())
            modified = True

    if modified:
        print("=== Content Filtered and Modified ===")
        print(f"Original Response: {response_text}")
        print(f"Modified Response: {modified_text}")
        return LlmResponse(content=types.Content(text=modified_text))

    # Return None to keep the original response
    print("No modifications made to the response.")
    return None

root_agent = LlmAgent(
    name="content_filter_agent",
    model="gemini-2.0-flash",
    description="An agent that demonstrates model callbacks for content filtering and logging",
    instruction="""
    You are a helful assistant.

    You job is to:
    - Answer user questions concisely
    - Provide factual information based on the user's input
    - Be friendly and helpful
    """,
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
