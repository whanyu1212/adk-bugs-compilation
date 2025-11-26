# ADK Bugs Compilation

A repository documenting bugs, issues, and unexpected behaviors found in Google's Agent Development Kit (ADK).

## Purpose

This repository serves as a collection of reproducible examples demonstrating various bugs and edge cases encountered while working with the Google ADK framework. Each example is self-contained and includes code to reproduce the issue.

## Captured Issues

### 1. ThinkingConfig + Output Schema Conflict

**Location**: [src/agent_tool_example/](src/agent_tool_example/)

**Issue**: When an Agent is configured with both `ThinkingConfig(include_thoughts=True)` and a structured `output_schema`, the model outputs markdown-formatted thoughts instead of valid JSON conforming to the Pydantic schema.

**Error**:
```
1 validation error for CalculatorOutput
  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='**Alright, let\'s break ... so 25 + 192 = 217."\n}', input_type=str]
```

**Root Cause**:
- `ThinkingConfig(include_thoughts=True, thinking_budget=-1)` instructs the model to output verbose reasoning in natural language
- `output_schema=CalculatorOutput` expects strict JSON conforming to the Pydantic model
- These configurations conflict, causing the model to prioritize thought output over structured schema compliance

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

**Status**: Unresolved - Framework should either:
- Prevent this configuration combination
- Automatically disable thoughts when output_schema is set
- Document this limitation clearly

