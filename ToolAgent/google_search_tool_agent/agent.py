from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="built_in_tool_agent",
    model="gemini-2.0-flash",
    description="Built In Tool (Calculator) Agent",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - Google search
    """,
    tools=[google_search]
)
