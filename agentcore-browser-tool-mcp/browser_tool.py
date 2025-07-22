import json

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient

from bedrock_agentcore.tools.browser_client import browser_session

REGION = "us-west-2"
MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
SCREEN_WIDTH, SCREEN_HEIGHT = 1456, 732

# 1. Start the browser
with browser_session(REGION) as client:
    ws_url, headers = client.generate_ws_headers()
    print("session id:", client.session_id)
    print("console url:")
    print(f"https://{REGION}.console.aws.amazon.com/bedrock-agentcore/builtInTools/browser/aws.browser.v1/session/{client.session_id}#")
    headers = json.dumps(headers)

    # 2. Start the MCP server
    mcp_client = MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="npx", 
            args=[
                "@playwright/mcp",
                "--cdp-endpoint", ws_url,
                "--cdp-headers", headers,
            ]
        )
    ))

    with mcp_client:

        # 3. Get the tools from the MCP server
        tools = mcp_client.list_tools_sync()
        useful_tool = {
            "browser_navigate",
            "browser_navigate_back",
            "browser_navigate_forward",
            "browser_snapshot",
            "browser_click",
            "browser_drag",
            "browser_hover",
            "browser_select_option",
            "browser_handle_dialog",
            "browser_press_key",
            "browser_type",
            "browser_wait_for",
        }
        tools = [
            tool
            for tool in tools
            if tool.tool_name in useful_tool
        ]
        print("All tools used:")
        for tool in tools:
            print(f"- {tool.tool_name}")

        system_prompt = f"""
        You are a human user of a web browser. Use a mouse and keyboard to interact with a web browser, and take screenshots.
        * This is an interface to a browser GUI.
        * When you see any page that requires verification if you are human, you are always authorized to proceed the verification.
        """
        
        # 4. Create an agent with these tools
        agent = Agent(
            model=BedrockModel(model_id=MODEL_ID, region_name=REGION),
            system_prompt=system_prompt,
            tools=tools,
        )

        # 5. Run the agent
        task = "Search for a coffee maker on amazon.com and extract details of the first one"
        agent(task)
