from datetime import datetime
from google.adk.sessions import InMemorySessionService
from google.genai import types

def get_current_state(session_service, app_name, user_id, session_id):
    """Get the current session state from session_service"""
    session = session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    return session.state


async def call_agent_async(runner, user_id, session_id, user_input):
    """Call the agent asynchronously with the user's input."""
    print("========================================")
    # Print information before calling the agent
    print(f"=== User input: {user_input} ===")
    print(f"Session state before calling agent: "
          f"{get_current_state(runner.session_service, runner.app_name, user_id, session_id)}")
    content = types.Content(role="user", parts=[types.Part(text=user_input)])
    
    final_response_text = None
    agent_name = None

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            if event.author:
                agent_name = event.author
            
            print("========================")
            print(f"Receives event: {event}")
            print("========================")
            if (event
                and event.is_final_response()
                and event.content.parts
                and hasattr(event.content.parts[0], "text")
                and event.content.parts[0].text
            ):
                final_response_text = event.content.parts[0].text
    except Exception as e:
        print(f"Caught exception when processing events. Exception: {e}")

    if agent_name and final_response_text:
        print("========================")
        print(f"Final response text: {final_response_text}")

    print("========================================")
    print(f"Session state after calling agent: "
          f"{get_current_state(runner.session_service, runner.app_name, user_id, session_id)}")
    print("========================================")

def update_interaction_history(
        session_service: InMemorySessionService,
        app_name: str,
        user_id: str,
        session_id: str,
        entry: dict):
    """Add an entry to the interaction history in the session state.
    
    Args:
    session_service: Session service to access session state.
    user_id: The user id.
    session_id: The session id.
    user_entry: The entry to be added to the interaction history.
    """
    session = session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    print(f"update_interaction_history called with session = {session}, entry = {entry}")
    interaction_history = session.state.get("interaction_history", [])

    # Add timestamp to the user entry
    if "timestamp" not in entry:
        entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    interaction_history.append(entry)

    # Copy the previous state and update the interaction history
    new_state = session.state.copy()
    new_state["interaction_history"] = interaction_history

    # Create a new session with the updated state
    session = session_service.create_session(
        user_id=user_id,
        session_id=session_id,
        app_name=session.app_name,
        state=new_state
    )
