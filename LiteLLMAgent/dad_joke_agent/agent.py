import os
import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(
    model="openrouter/openai/gpt-4.1-nano",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def get_dad_joke():
    """Randomly return a dad joke from a list of them."""
    jokes = [
        "Why do chicken cross the road? To get to the other side!",
        "What do you call a belt made of watches? A waste of time.",
        "What do you call fake spaghetti! An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
    ]
    return random.choice(jokes)

root_agent = Agent(
    name="dad_joke_agent",
    model=model,
    description="Dad Joke Agent",
    instruction="""
    You are a helpful assistant that can tell dad jokes.
    Only use the `get_dad_joke` tool.
    """,
    tools=[get_dad_joke]
)
