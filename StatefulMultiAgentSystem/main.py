import asyncio
from dotenv import load_dotenv

from customer_service_agent.agent import customer_service_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import call_agent_async, update_interaction_history

# Initialize in memory session service and initial state
session_service = InMemorySessionService()
initial_state = {
    "user_name": "yyu196",
    "purchased_courses": [],
    "interaction_history": []
}

load_dotenv()

async def main_async():
    """Entry point of the application"""
    print("Stateful Multi Agent Course Sale Customer Support System starts.")

    # Setup constant
    app_name = "Course Sale Customer Support"
    user_id = "yyu196"

    # Create a new session with initial state
    new_session = session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        state=initial_state
    )
    session_id = new_session.id
    print(f"Create a new session. Session id: {session_id}")

    # Create a runner with the main customer service agent
    runner = Runner(
        agent=customer_service_agent,
        app_name=app_name,
        session_service=session_service
    )

    # Interactive conversation loop
    print("Customer Service Chat starts. Type 'exit' or 'quit' to end the conversation.")
    while True:
        # Get user input
        user_input = input("You: ")

        # Check if user wants to end the program
        if user_input.lower() in ["exit", "quit"]:
            print("End conversation. Program ends.")
            break

        update_interaction_history(
            session_service=session_service,
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            entry={
                "action": "user_input",
                "text": user_input
            }
        )

        await call_agent_async(
            runner=runner,
            user_id=user_id,
            session_id=session_id,
            user_input=user_input
        )

if __name__ == "__main__":
    asyncio.run(main_async())
