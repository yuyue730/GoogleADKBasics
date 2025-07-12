# Introduction to Google Agent Development Kit (ADK) and Model Context Protocol (MCP)

## Environment Setup

The [`requirements.txt`](./requirements.txt) defines all dependencies needed for the agent 
development environment. Execute the following command to create the virtual environemnt and
install all the defined dependencies.

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Go to https://console.cloud.google.com to create a new Google Cloud project, then go to
https://aistudio.google.com/ to create the API Key.

## Basic Agent

Create the most basic [`greenting_agent`](./BasicAgent/greeting_agent/) agent which asks for user's 
name and greets the user.

Execute `adk web` to debug the agent. See the following screenshot on the behavior.

## Tool Agent

### Built-in tools

In [this example](./ToolAgent/google_search_tool_agent/agent.py), I added an agent which has access to the `google_search` internal tool. See this example:

![Google Search Build-in tool example](./Screenshots/GoogleSearchBuiltInTool.png)
