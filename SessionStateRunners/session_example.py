from google.adk.sessions import InMemorySessionService, Session

print("This is a program to exam Session object Properties")

session_service = InMemorySessionService()
example_session: Session = session_service.create_session(
    app_name="my_app",
    user_id="example_user",
    state={"initial_key": "initial_value"}  # Session State can be initialized 
)

print("----- Session Properties -----")
print(f"ID (`id`): {example_session.id}")
print(f"Application Name (`app_name`): {example_session.app_name}")
print(f"User ID (`user_id`): {example_session.user_id}")
print(f"State (`state`): {example_session.state}")
print(f"Events (`events`): {example_session.events}")
print(f"Last Update (`last_update_time`): {example_session.last_update_time}")
print("------------------------------")
