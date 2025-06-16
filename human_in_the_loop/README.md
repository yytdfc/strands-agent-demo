# Human-in-the-Loop Agent Demo

This repository contains a demonstration of a human-in-the-loop agent system that allows for interactive control and confirmation of agent actions.

## Overview

The system implements a secure MCP (Model Context Protocol) Filesystem Server that runs on standard input/output. It provides a controlled environment where an agent can perform actions on the filesystem, but requires human confirmation before executing potentially sensitive operations.

## Files

- `main.py` - The main entry point for the application
- `callback_handler.py` - Handles callbacks and interactions between the agent and human user

## Usage

To run the application:

```bash
uv run main.py
```

Once running, you can enter tasks for the agent to perform. The agent will:

1. Analyze your request
2. Propose a tool to use
3. Ask for your confirmation before proceeding
4. Execute the confirmed action and show results

## Example Interactions

- `list all files` - Lists all files in the allowed directories
- Other commands can be used to interact with the filesystem within the allowed directories

### Example Session

```
uv run main.py
Secure MCP Filesystem Server running on stdio
Allowed directories: [ '/Users/cfu/git/300_autocode/strands-agent-demo/human_in_the_loop' ]
=====================================
Enter a task: list all files

🌟 Agent:

I'll help you list all the available files. First, let me check which directories are allowed for access, then I can show you the files in them.

🔧 Tool Used: list_allowed_directories
⚠️ Please confirm to use the tool ⚠️  (y/N): n
=====================================
Enter a task: continue

🌟 Agent:

Let me list the allowed directories first and then show you the files within them.

🔧 Tool Used: list_allowed_directories
⚠️ Please confirm to use the tool ⚠️  (y/N): y

📊 Tool Result (success):
Allowed directories:
/Users/cfu/git/300_autocode/strands-agent-demo/human_in_the_loop

🌟 Agent:

Now I'll list all the files in the allowed directory:

🔧 Tool Used: list_directory
{'path': '/Users/cfu/git/300_autocode/strands-agent-demo/human_in_the_loop'}
⚠️ Please confirm to use the tool ⚠️  (y/N): y

📊 Tool Result (success):
[DIR] __pycache__
[FILE] callback_handler.py
[FILE] main.py

🌟 Agent:

These are the files and directories in the allowed directory. There are two Python files (`callback_handler.py` and `main.py`) and one directory (`__pycache__`).
I see you're working with a project that has a human-in-the-loop agent system. Let me help you create a
README.md file for this project based on the files I can see in your directory.
```

## Security

The system is designed with security in mind:
- Only specific directories are allowed for access
- Human confirmation is required before executing tools
- The agent runs in a controlled environment

## Requirements

- Python
- uv (Python package manager/runner)
