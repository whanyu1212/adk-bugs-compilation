from pydantic import BaseModel, Field
from google.adk.agents import Agent
from google.adk.tools import agent_tool
from google.adk.planners import BasePlanner, BuiltInPlanner, PlanReActPlanner
from google.adk.models import LlmRequest

from google.genai.types import ThinkingConfig
from google.genai.types import GenerateContentConfig
from opik.integrations.adk import OpikTracer, track_adk_agent_recursive


class CalculatorOutput(BaseModel):
    result: str = Field(..., description="The result of the calculation")
    reasoning: str = Field(
        ..., description="The step by step reasoning for the calculation"
    )


# Create a specialized agent that acts as a tool
calculator_agent = Agent(
    name="calculator",
    model="gemini-3-pro-preview",
    instruction="""You are a calculator specialist.
    When given a math problem, solve it step by step and return the result.
    Always show your work.""",
    description="Solves mathematical calculations",
    planner=BuiltInPlanner(
        thinking_config=ThinkingConfig(include_thoughts=True, thinking_budget=-1),
    ),
    output_schema=CalculatorOutput,
)

# Wrap the calculator agent as a tool
calculator_tool = agent_tool.AgentTool(agent=calculator_agent)

# Create the root agent that uses the calculator agent as a tool
root_agent = Agent(
    name="assistant",
    model="gemini-3-pro-preview",
    instruction="""You are a helpful assistant.
    When users ask math questions, use the calculator tool to solve them.
    For other questions, answer directly.""",
    description="A helpful assistant with calculation abilities",
    tools=[calculator_tool],
)

opik_tracer = OpikTracer(
    name="agent-tool-example-tracer",
    tags=["multi-agent"],
    metadata={
        "environment": "development",
        "model": "gemini-3-pro-preview",
        "framework": "google-adk",
        "example": "basic",
    },
    project_name="agent-tool-example",
)

track_adk_agent_recursive(root_agent, opik_tracer)
