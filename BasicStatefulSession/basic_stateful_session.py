import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

load_dotenv()

# Create an InMemorySessionService object to store state
stateful_session_service = InMemorySessionService()

initial_state = {
    "user_name": "Yue Yu",
    "user_preference": """
    I like to play tennis and soccer.
    My favourite food is Chinese.
    My favourite TV show is The Big Bang Theory.
    Loves it when other engineers approve and merge his Pull Requests.
    """
}

# Create a session from the InMemorySessionService
APP_NAME = "Yue Bot"
USER_ID = "yyu196"
SESSION_ID = str(uuid.uuid4())
stateful_session = stateful_session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state
)
print(f"A new session has been created. Session ID: {stateful_session.id}")

# Create the runner
runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=stateful_session_service
)

#  Start the runner by passing the user_message to the agent
user_message = types.Content(
    role="user",
    parts=[types.Part(text="What is Yue's favorite TV show?")]
)
for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=user_message):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final response: {event.content.parts[0].text}")

print("===== Session Event Exploration: Final Session State =====")
session = stateful_session_service.get_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)

for key, value in session.state.items():
    print(f"{key}: {value}")
