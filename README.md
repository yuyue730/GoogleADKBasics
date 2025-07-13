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
* `output_schema` (Optional but highly recommended): Define a schema representing the desired 
output structure. If set, the agent's final response must be a JSON string conforming to this 
schema.
* `output_key` (Optional): If set, the text content of the agent's final response is 
automatically saved to the session's state dictionary under the `output_key`. See the 
screenshots below:

![Example Structured Output Conversation](./Screenshots/StructuredOutput_Conversation.png)
<img src="./Screenshots/StructuredOutput_Request.png" width="500">
<img src="./Screenshots/StructuredOutput_Response.png" width="500">

## Session, State and Runners

### Session
A "Session" can be interpreted as a "Stateful chat history" or a "Conversation 
Thread". `Session` is an ADK object designed to store the "Conversation Thread". It includes:
  * `id` -- An identifier for the specific "Conversation Thread".
  * `events` -- A chronological sequence of all interactions, including "user messages", 
  "agent responses" and "tool actions".
  * `state` -- A dictionary storing temporary data relevant only to this specific 
  "Conversation Thread".

[This script](./SessionStateRunners/session_example.py) creates a session and print its 
important properties to the console. See its execution output below:
```
% python SessionStateRunners/session_example.py 
This is a program to exam Session object Properties
----- Session Properties -----
ID (`id`): e9faf650-a30b-44c8-b8be-2b19955a3301
Application Name (`app_name`): my_app
User ID (`user_id`): example_user
State (`state`): {'initial_key': 'initial_value'}
Events (`events`): []
Last Update (`last_update_time`): 1752375458.8551521
------------------------------
```

* `SessionService` -- The central manager responsible for the entire lifecycle of the 
conversation sessions.

[//]: # (TODO: Add an image showing the structure of a `SeSessionService` object)

### Runner

[//]: # (TODO: Add an image showing the `Runner` workflow)

* Step 1: `User` sends the query (`user_message`) to the Runner
* Step 2. Runner loads or creates the session and add appends `user_message` to the session 
history via `SessionService`.
* Step 3: Runner passes the context to the `Agent_Llm` which requests the `LLM` and executes the 
Tools per `LLM`'s response. Runner also updates the Session, including State and Events. Assume 
`Agent_Llm` decides to call `MyTool`, below are the detailed sub-steps:
  * Step 3.1: `Agent_Llm` receives `FunctionCall` response from `LLM` and `yields` an FunctionCall `Event`.
  * Step 3.2: `Runner` receives the `Event(FunctionCall)` from `Agent_Llm`. `SessionService` records it in the history. `Runner` yields `Event(FunctionCall)` to the `User`.
  * Step 3.3: `Agent_Llm` resumes to execute the requested `MyTool` by calling 
  `tool.run_async(...)`.
  * Step 3.4: `Agent_Llm` gets the tool execution result and yield `Event(FunctionResponse)` to 
  the `Runner`.
  * Step 3.5: `Runner` receives the `Event(FunctionResponse)` from `Agent_Llm`. `SessionService` 
  records the `Event(FunctionResponse)` and updates the underlying `Session`. `Runner` yields 
  `Event(FunctionResponse)` to the `User`.
  * Step 3.6: `Agent_Llm` resumes to send the tool result to the `LLM` to generate a natural 
  langauge response.
  * Step 3.7: `Agent_Llm` receives the final text from `LLM`, wraps it in the response to the 
  `Runner`.
* Step 4: `Runner` responds the final result / completion to the user.
