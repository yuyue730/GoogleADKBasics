from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    """Add a new reminder to the user's reminder list.

    Args:
        reminder: The reminder text to add
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(f"--- Tool: add_reminder called for {reminder} ---")

    # Get current reminders from state
    reminders = tool_context.state.get("reminders", [])

    # Add the new reminder
    reminders.append(reminder)

    # Update the state with the new list of reminders
    tool_context.state["reminders"] = reminders

    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": f"Added reminder: {reminder}"
    }

def view_reminders(tool_context: ToolContext) -> dict:
    """View all current reminders.

    Args:
        tool_context: Context for accessing session state

    Returns:
        The list of reminder
    """
    print("--- Tool: view_reminders called ---")

    # Get reminders from state
    reminders = tool_context.state.get("reminders", [])

    return {
        "action": "view_reminders",
        "reminders": reminders,
        "count": len(reminders)
    }

def update_reminder(index: int, updated_text: str, tool_context: ToolContext) -> dict:
    """Update an existing reminder.

    Args:
        index: The 1-based index of the reminder to update
        updated_text: The new text for the reminder
        tool_context: Context for accessing session state
    
    Returns:
        A confirmation message
    """
    print(f"--- Tool: update_reminder called with index: {index}, updated_text: {updated_text} ---")

    # Get current remindes from state
    reminders = tool_context.state.get("reminders", [])

    # Check if the index is valid
    if not reminders or index < 1 or index > len(reminders):
        error_message = f"""Could not find reminder at position {index}.
                            Currently there are {len(reminders)} reminders."""
        return {
            "action": "update_reminder",
            "status": "error",
            "message": error_message
        }
    
    # Update the reminder in the state
    old_reminder = reminders[index - 1]
    reminders[index - 1] = updated_text

    # Update the state with the modified text
    tool_context.state["reminders"] = reminders

    return {
        "action": "update_reminder",
        "index": index,
        "old_text": old_reminder,
        "updated_text": updated_text,
        "message": f"Updated reminder {index} from '{old_reminder}' to '{updated_text}'"
    }

def delete_reminder(index: int, tool_context: ToolContext) -> dict:
    """Delete a reminder.

    Args:
        index: The 1-based index of the reminder to delete
        tool_context: Context for accessing session state
    
    Returns:
        A confirmation message
    """
    print(f"--- Tool: delete_reminder called with index: {index} ---")

    # Get current reminders from state
    reminders = tool_context.state.get("reminders", [])

    # Check if the index is valid
    if not reminders or index < 1 or index > len(reminders):
        error_message = f"""Could not find reminder at position {index}.
                            Currently there are {len(reminders)} reminders."""
        return {
            "action": "delete_reminder",
            "status": "error",
            "message": error_message
        }
    
    # Remove the reminder (adjust to 0-based index)
    deleted_reminder = reminders.pop(index - 1)

    # Update state with the modified list
    tool_context.state["reminders"] = reminders

    return {
        "action": "delete_reminder",
        "index": index,
        "deleted_reminder": deleted_reminder,
        "message": f"Delete reminder {index}: '{deleted_reminder}'"
    }

def update_user_name(name: str, tool_context: ToolContext) -> dict:
    """Update the user's name.

    Args:
        name: The new name for the user
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message.
    """
    print(f"--- Tool: update_user_name called for {name} ---")

    # Get current name from state
    old_name = tool_context.state.get("user_name", "")

    # Update the name in state
    tool_context.state["user_name"] = name

    return {
        "action": "update_user_name",
        "old_name": old_name,
        "new_name": name,
        "message": f"Updated your name to: {name}"
    }

memory_agent = Agent(
    name="memory_agent",
    model="gemini-2.0-flash",
    description="A smart reminder agent with persistent memory",
    instruction="""
    You are a friendly reminder assistant that remembers users across conversations.

    The user's information is stored in state:
    - User's name: {user_name}
    - Reminders: {reminders}

    You can help users manage their reminders with the following capabilities:
    1. Add new reminders
    2. View existing reminders
    3. Update reminders
    4. Delete reminders
    5. Update the user's name

    Always be friendly and address the user by name. If you don't know their name yet, use the
    update_user_name tool to store it when they introduce themselves.

    * REMINDER MANAGEMENT GUIDELINES:**
    1. When the user asks to update a reminder but does not provide an index:
      - If they mention the content of the reminder (e.g. "delete my meeting reminder), look through
        the reminders to find a match.
      - If you find an exact or close match, use that index
      - Never clarify which reminder the user is referring to, just use the first match
      - If no match is found, list all reminders and ask the user to specify

    2. When the user mentions a number or position:
      - Use that as the index (e.g. "Update remind 2" means index = 2)
      - Remind that indexing starts at 1 for the user

    3. For relative positions
      - Handle "first", "last", "second" etc. appropriately
      - "First reminder" = index 1
      - "Last reminder" = the highest index
      - "Second reminder" = index 2, and so on

    4. For viewing:
      - Always use the view_reminders tool when the user asks to see their reminders
      - Format the response in a numbered list for clarity
      - If there are no reminders, suggest adding some

    5. For addition:
      - Extract the actual reminder text from user's request
      - Remove phrases like "add a reminder to" or "remind me to"
      - Focus on the task itself.
      - Example: "add a reminder to buy milk" -> add_reminder("buy_milk")

    6. For updates:
      - Identify both which reminder to update and what the new text should be
      - For example, "My second reminder is changed to picking up package" -> 
        update_reminder(2, "pick up package")

    7. For deletions:
      - Confirm deletion when complete and mention which reminder was removed
      - For example, "I have deleted your reminder to 'buy milk'.

    Remind to explain that you can remember their information across conversations.

    IMPORTANT:
    - Use your best judgement to determine which reminder the user is referring to.
    - You don't have to be 100% correct, but try to be as close as possible.
    - Never ask the user to clarify which reminder they are referring to.
    """,
    tools=[add_reminder, view_reminders, update_reminder, delete_reminder, update_user_name]
)
