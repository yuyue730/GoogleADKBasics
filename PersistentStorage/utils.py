from google.adk.runners import Runner
from google.genai import types

def get_current_state(session_service, app_name, user_id, session_id):
    """Get the current session state from session_service"""
    session = session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    return session.state

async def call_agent_async(runner: Runner, user_id, session_id, user_input):
    """Call the agent asynchronously with the user's input"""
    print(
        f"call_agent_sync called with user_input: {user_input}, "
        f"state: {get_current_state(runner.session_service, runner.app_name, user_id, session_id)}"
    )
    new_message = types.Content(role="user", parts=[types.Part(text=user_input)])

    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message
        ):
            print("===========")
            print(f"Event = {event}")
            print("===========")
            if event.is_final_response():
                print("===========")
                print(f"final response: {event.content.parts[0].text}")
                print("===========")
    except Exception as e:
        print(f"Error during agent call: {e}")

    print(
        f"call_agent_sync finishes updated state: "
        f"{get_current_state(runner.session_service, runner.app_name, user_id, session_id)}\n\n"
    )
