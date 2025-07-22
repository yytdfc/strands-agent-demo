import json

from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient
from strands import Agent


from bedrock_agentcore.tools.browser_client import browser_session

region = "us-west-2"

# 1. Start the browser
with browser_session(region) as client:
    ws_url, headers = client.generate_ws_headers()
    headers = json.dumps(headers)

    print("live view url:")
    print(client.generate_live_view_url())

    # 2. Start the MCP server
    mcp_client = MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="npx", 
            args=[
                "@playwright/mcp",
                "--isolated",
                "--cdp-endpoint", ws_url,
                "--cdp-headers", headers,
            ]
        )
    ))

    with mcp_client:

        # 3. Get the tools from the MCP server
        tools = mcp_client.list_tools_sync()

        
        # 4. Create an agent with these tools
        agent = Agent(tools=tools)

        # 5. Run the agent
        task = "Open trip.com, and search the cheapest flight from Shenzhen to Beijing."
        agent(task)

