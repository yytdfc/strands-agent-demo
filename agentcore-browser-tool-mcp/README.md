

# Browser Tool MCP Demo

This demonstration showcases intelligent browser automation using the Model Context Protocol (MCP) with two distinct operational modes: vision-enabled and standard DOM-based interactions.

## Prerequisites

### playwright-mcp Setup

``` bash
# Clone the repository:
git clone https://github.com/yytdfc/playwright-mcp.git -b dev
cd playwright-mcp

# Install dependencies:
npm install

# Build the project:
npm run build

# Create a local link:
npm link
```

## Execution Options

### Standard Mode (Recommended for Structured Web Applications)

Execute the DOM-based browser tool:

```bash
uv run ./browser_tool_wo_vision.py
```

**Capabilities:**
- Leverages DOM element selectors for precise interactions
- Optimized for structured web applications with identifiable elements
- Recommended tools include:
  - `browser_navigate` - URL navigation
  - `browser_snapshot` - DOM state capture
  - `browser_click` - Element-based clicking
  - `browser_type` - Text input functionality
  - `browser_select_option` - Dropdown interactions
  - `browser_wait_for` - Conditional waiting

**Recommended for:** Applications with well-defined DOM structures, form interactions, and predictable element hierarchies.

### Vision-Enhanced Mode (Recommended for Dynamic Interfaces)

Execute the vision-capable browser tool:

```bash
uv run ./browser_tool_with_vision.py
```

**Enhanced Capabilities:**
- Utilizes coordinate-based interactions with visual processing
- Incorporates `--caps vision` for advanced visual analysis
- Recommended tools include:
  - `browser_take_screenshot` - Visual state capture
  - `browser_mouse_click_xy` - Coordinate-precise clicking
  - `browser_mouse_move_xy` - Cursor positioning
  - `browser_mouse_drag_xy` - Drag operations
  - Screen resolution optimization (1456x732)

**Recommended for:** Dynamic content, canvas-based applications, complex visual interfaces, and scenarios requiring visual feedback.

## Implementation Comparison

| Aspect | Standard Mode | Vision-Enhanced Mode |
|--------|---------------|---------------------|
| Interaction Strategy | DOM element targeting | Visual coordinate mapping |
| Feedback Mechanism | DOM snapshots | Screenshot analysis |
| Processing Capabilities | Standard MCP | Vision-enhanced MCP |
| Optimal Use Cases | Structured web forms | Dynamic visual content |
| Performance Profile | Lower resource usage | Higher visual processing |

Choose the mode that best aligns with your specific automation requirements and target application characteristics.
