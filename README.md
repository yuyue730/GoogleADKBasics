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

Create the most basic [`greenting_agent`](./BasicAgent/greeting_agent/) agent which asks for 
username and greets the user. Execute `adk web` to debug the agent.

## Tool Agent

### Built-in tools

In [this example](./ToolAgent/google_search_tool_agent/agent.py), an agent which has access to the `google_search` internal tool is implemented. See this screenshot:

![Google Search Build-in tool example](./Screenshots/GoogleSearchBuiltInTool.png)

### Function tools

In [this example](./ToolAgent/two_function_tools_agent/agent.py), an agent which queries 
Database for order and inventory status is implemented. See this screenshot:

![Query order inventory tool example](./Screenshots/TwoFunctionTools.png)

### Third Party tools

Agent could also be designed to integrate tools from other AI Agent frameworks like LangChain.

## LiteLLM

Register a https://openrouter.ai/ account and add some credit, then create an API Key and put 
it in the `.env` file in the agent's directory.

In [this example](./LiteLLMAgent/dad_joke_agent/agent.py), an agent which asks Open AI gpt-4.1-nano model to execute `get_dad_joke()` tool is implemented. See this screenshot:

![LiteLLM tool example](./Screenshots/LiteLLMTool.png)

## Structring Data

* `input_schema` (Optional): Expected input structure. This might not be very useful.
* `output_schema` (Optional but highly recommended): Define a schema representing the desired output structure. If set, the agent's final response must be a JSON string conforming to this schema.
* `output_key` (Optional): If set, the text content of the agent's final response is automatically saved to the session's state dictionary under the `output_key`. See the screenshots below:

![Example Structured Output Conversation](./Screenshots/StructuredOutput_Conversation.png)
![Example Structured Output Request](./Screenshots/StructuredOutput_Request.png)
![Example Structured Output Response](./Screenshots/StructuredOutput_Response.png)