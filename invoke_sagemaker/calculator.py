from strands import Agent
from strands_tools import calculator

from strands.telemetry import StrandsTelemetry

from sagemaker_model import SageMakerModel

model = SageMakerModel(endpoint_name="Qwen-Qwen3-30B-A3B-FP8-250724-1124", model_id="Qwen/Qwen3-30B-A3B-FP8")


agent = Agent(
    model=model,
    system_prompt="You are a helpful assistant that provides concise responses.",
    tools=[calculator],
)

agent("what is 23 * 23412")
