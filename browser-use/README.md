# Browser Automation Agent

A web browser automation agent built with Strands AI framework that can interact with web pages using natural language instructions. This demo showcases an AI agent that can navigate websites, click elements, type text, and perform complex web tasks autonomously.

## Features

- **Natural Language Web Automation**: Give the agent tasks in plain English
- **Visual Feedback**: Real-time screenshots with visual indicators showing where the agent clicks
- **Browser Control**: Full browser automation including navigation, clicking, typing, and form filling
- **AI-Powered Decision Making**: Uses Claude 3.7 Sonnet via AWS Bedrock for intelligent web interaction
- **MCP Integration**: Leverages Model Context Protocol (MCP) with Playwright for browser automation

## Prerequisites

- Python 3.10 or higher
- Node.js and npm (for Playwright MCP server)
- AWS credentials configured for Bedrock access
- Terminal that supports Sixel graphics (for image display)

## Installation

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Ensure Node.js is installed** (required for Playwright MCP server):
   ```bash
   node --version
   npm --version
   ```

## Usage

Run the browser automation agent:

```bash
cd browser-use
uv run main.py
```

The agent will:
1. Launch a browser instance
2. Execute the predefined task (currently searches for flights from Shenzhen to Beijing on trip.com)
3. Display real-time screenshots and actions in the terminal
4. Show visual indicators of where it clicks on the page

## How It Works

### Core Components

**main.py**: The main application that:
- Initializes the Bedrock AI model (Claude 3.7 Sonnet)
- Sets up MCP client connection to Playwright browser automation
- Configures the agent with browser control tools
- Defines the automation task and executes it

**callback_handler.py**: Provides visual feedback by:
- Displaying colored terminal output for different message types
- Showing screenshots using Sixel graphics
- Drawing visual indicators (red circles) on screenshots to show click locations
- Formatting tool usage and results for easy reading

### Available Browser Tools

The agent has access to these browser automation capabilities:
- `browser_navigate` - Navigate to URLs
- `browser_navigate_back/forward` - Browser history navigation
- `browser_screen_capture` - Take screenshots
- `browser_screen_click` - Click on page elements
- `browser_screen_drag` - Drag and drop actions
- `browser_screen_type` - Type text into fields
- `browser_press_key` - Send keyboard inputs
- `browser_wait_for` - Wait for page elements
- `browser_handle_dialog` - Handle browser dialogs

### Configuration

Key settings in `main.py`:
- **Model**: Claude 3.7 Sonnet via AWS Bedrock (us-west-2 region)
- **Screen Resolution**: 768x768 pixels
- **Temperature**: 0.3 (for consistent behavior)
- **Browser**: Isolated Playwright instance with vision capabilities

## Customization

### Changing the Task

Modify the `task` variable in `main.py`:
```python
task = "Your custom web automation task here"
```

### Adjusting Screen Size

Update the screen dimensions:
```python
SCREEN_HEIGHT = 1024
SCREEN_WIDTH = 1280
```

### Model Configuration

Change the AI model or settings:
```python
bedrock_model = BedrockModel(
    model_id="your-preferred-model-id",
    region_name='your-aws-region',
    temperature=0.5,  # Adjust creativity vs consistency
)
```

## Example Tasks

The agent can handle various web automation scenarios:

- **E-commerce**: "Find and add the cheapest laptop under $1000 to cart"
- **Travel**: "Search for flights from NYC to LA next week"
- **Research**: "Find the contact information for the top 3 AI companies"
- **Form Filling**: "Fill out the contact form with sample data"
- **Data Extraction**: "Extract all product prices from this page"

## Terminal Output

The callback handler provides color-coded output:
- 🌟 **Green**: Agent responses and reasoning
- 👤 **Blue**: User messages and tasks
- 🔧 **Yellow**: Tool usage (browser actions)
- 📊 **Magenta**: Tool results and status
- 📷 **Cyan**: Screenshot notifications
- **Red circles**: Visual click indicators on screenshots

## Troubleshooting

**Browser doesn't launch**: Ensure Node.js is installed and Playwright MCP server can be accessed via `npx @playwright/mcp@latest`

**No images displayed**: Your terminal needs Sixel graphics support. Try using iTerm2 on macOS or a compatible terminal emulator.

**AWS Bedrock errors**: Verify your AWS credentials are configured and you have access to Claude models in the us-west-2 region.

**MCP connection issues**: Check that the Playwright MCP server starts correctly by running the command manually.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Strands       │    │   MCP Client     │    │   Playwright    │
│   Agent         │◄──►│   (stdio)        │◄──►│   Browser       │
│   (Claude 3.7)  │    │                  │    │   Automation    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         ▲
         │
         ▼
┌─────────────────┐
│   Callback      │
│   Handler       │
│   (Visual UI)   │
└─────────────────┘
```

The agent uses the Strands framework to coordinate between the AI model, browser automation tools, and user interface, creating a seamless web automation experience.
