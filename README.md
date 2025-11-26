# ADK Bugs Compilation

A repository documenting bugs, issues, and unexpected behaviors found in Google's Agent Development Kit (ADK).

## Purpose

This repository serves as a collection of reproducible examples demonstrating various bugs and edge cases encountered while working with the Google ADK framework. Each example is self-contained and includes code to reproduce the issue.

## Captured Issues

### 1. AgentTool Returns Thoughts Instead of Output

**Location**: [src/agent_tool_example/](src/agent_tool_example/)

**Issue**: When an Agent is wrapped as a tool via `AgentTool` and configured with `ThinkingConfig(include_thoughts=True)` and an `output_schema`, the tool's function response returns the model's thoughts instead of the structured output, causing JSON parsing failures.

**Error**:
```
1 validation error for CalculatorOutput
  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='**Alright, let\'s break ... so 25 + 192 = 217."\n}', input_type=str]
```

**Root Cause**:
- When `include_thoughts=True` is set on an agent used as a tool, the `AgentTool` wrapper returns the thoughts/reasoning text instead of the actual structured output
- The agent has `output_schema=CalculatorOutput` expecting JSON format
- But `AgentTool` is returning the markdown-formatted thoughts (e.g., `**Alright, let's break...`) as the function response
- This causes Pydantic validation to fail when trying to parse thoughts as JSON

**Expected Behavior**: The calculator agent should return JSON like:
```json
{
  "result": "4714",
  "reasoning": "125 * 37 = 4625, then 4625 + 89 = 4714"
}
```

**Actual Behavior**: Returns markdown-formatted text like:
```
**Alright, let's break this down step by step...
```

**Workarounds**:
1. Remove `ThinkingConfig` if structured output is required
2. Set `include_thoughts=False` in ThinkingConfig
3. Remove `output_schema` if free-form thoughts are needed

**Status**: Unresolved - `AgentTool` should:
- Return the actual structured output, not the thoughts, when an agent has both `include_thoughts=True` and `output_schema`
- Separate thoughts from the tool's return value
- Or prevent this configuration combination with a clear error message

**Reported**: Issue #3706

