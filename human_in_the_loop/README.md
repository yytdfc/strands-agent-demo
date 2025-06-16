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

## Security

The system is designed with security in mind:
- Only specific directories are allowed for access
- Human confirmation is required before executing tools
- The agent runs in a controlled environment

## Requirements

- Python
- uv (Python package manager/runner)
