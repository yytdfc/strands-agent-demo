# SageMaker Endpoint with Strands Agent SDK

Use your SageMaker endpoints as LLMs in Strands agents with tool support.

## Files

- `sagemaker_model.py` - Custom SageMaker model implementation
- `calculator.py` - Demo with calculator tool

## Usage

```python
from strands import Agent
from strands_tools import calculator
from sagemaker_model import SageMakerModel

model = SageMakerModel(
    endpoint_name="your-endpoint-name",
    model_id="your-model-id"
)

agent = Agent(
    model=model,
    system_prompt="You are a helpful assistant.",
    tools=[calculator]
)

response = agent("What is 23 * 23412?")
```

## Requirements

- AWS credentials configured
- SageMaker endpoint with OpenAI-compatible API
- Endpoint must support streaming responses
- For vLLM need to set `--enable-auto-tool-choice` and `--tool_call_parser`
