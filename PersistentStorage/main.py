import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from memory_agent.agent import memory_agent
from utils import call_agent_async

load_dotenv()

# Initialize Persistent Storage Session Service
DB_URL = "sqlite:///./my_agent_data.db"
db_session_service = DatabaseSessionService(db_url=DB_URL)

# Define the initial state
initial_state = {
    "user_name": "yyu196",
    "reminders": [],
}

async def main_async():
    """Implementation of the main method that is run asynchronously."""
    print("Persistent Storage Session Agent demo project starts.")
    APP_NAME = "Memory Agent"
    USER_ID = "yyu196"

    # Check for existing session of this user
    existing_sessions = db_session_service.list_sessions(app_name=APP_NAME, user_id=USER_ID)

    print(f"existing_sessions = {existing_sessions.sessions}")
    if existing_sessions and len(existing_sessions.sessions) > 0:
        # Use the most recent existing session
        session_id = existing_sessions.sessions[0].id
        print(f"App name: {APP_NAME}, User id: {USER_ID}, find existing session id: {session_id}")
    else:
        # Create a new session
        new_session = db_session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state
        )
        session_id = new_session.id
        print(
            f"App name: {APP_NAME}, User id: {USER_ID}, "
            f"a new session created with id: {session_id}"
        )

    # Create a Runner with the memory agent
    runner = Runner(agent=memory_agent, app_name=APP_NAME, session_service=db_session_service)

    # Interactive Conversation Loop
    print(
        "Reminder agent conversation loop starts. Type 'exit' or 'quit' to end the conversation"
    )

    while True:
        user_input = input("User: ")

        # Check if user want to end the conversation
        if user_input.lower() in ["exit", "quit"]:
            print("End conversation")
            break

        await call_agent_async(
            runner=runner,
            user_id=USER_ID,
            session_id=session_id,
            user_input=user_input
        )

if __name__ == "__main__":
    asyncio.run(main_async())
