import os

from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

from callback_handler import message_callback_handler

MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
SCREEN_HEIGHT = 768
SCREEN_WIDTH = 768


# 1. Create a BedrockModel
bedrock_model = BedrockModel(
    model_id=MODEL_ID,
    region_name='us-west-2',
    temperature=0.3,
)

# 2. Connect to an MCP server using stdio transport

workspace_folder = os.path.dirname(os.path.abspath(__file__))

mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="npx", 
        args=[
          "-y",
          "@modelcontextprotocol/server-filesystem",
          f"{workspace_folder}",
        ]
    )
))


TERMINATE_WORDS = {"q", "quit", "exit"}


with mcp_client:

    # 3. Get the tools from the MCP server
    tools = mcp_client.list_tools_sync()


    # 4. Create an agent with these tools
    agent = Agent(
        tools=tools,
        callback_handler=message_callback_handler,
    )

    # 5. Run the agent

    while True:
        task = input("=====================================\nEnter a task: ")
        if task.strip() in TERMINATE_WORDS:
            break
        agent(task)
