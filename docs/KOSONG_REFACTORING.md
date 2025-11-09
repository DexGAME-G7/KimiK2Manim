# Kosong Refactoring Guide

This document outlines how to refactor the KimiK2Manim agents to use [Kosong](https://github.com/MoonshotAI/kosong), the official LLM abstraction layer from Moonshot AI.

## Overview

Kosong provides:
- Unified message structures (`Message` class)
- Async tool orchestration with `kosong.step()`
- Pluggable chat providers (including Kimi)
- Built-in tool calling abstraction with Pydantic models
- Simplified API that reduces boilerplate

## Prerequisites

**Important**: Kosong requires Python 3.13+. If you're on an older version, you'll need to upgrade first.

```bash
# Check Python version
python --version

# If < 3.13, upgrade Python or use uv (recommended by Kosong)
uv init --python 3.13
uv add kosong
```

## Current Architecture vs Kosong Architecture

### Current (Custom Implementation)
```python
# Custom KimiClient wrapper
client = KimiClient()
response = client.chat_completion(
    messages=[{"role": "user", "content": "..."}],
    system="...",
    tools=[...],
    tool_choice="auto"
)
# Manual parsing of tool calls
tool_calls = client.get_tool_calls(response)
```

### With Kosong
```python
# Unified interface
from kosong.chat_provider.kimi import Kimi
from kosong.message import Message
from kosong import step

kimi = Kimi(
    base_url="https://api.moonshot.ai/v1",
    api_key=os.getenv("MOONSHOT_API_KEY"),
    model="kimi-k2-turbo-preview",
)

# Simple generation
message, usage = await kosong.generate(
    chat_provider=kimi,
    system_prompt="...",
    history=[Message(role="user", content="...")],
    tools=[],
)

# Tool calling with automatic orchestration
result = await kosong.step(
    chat_provider=kimi,
    system_prompt="...",
    toolset=toolset,
    history=[Message(role="user", content="...")],
)
```

## Refactoring Steps

### Step 1: Define Tools with Pydantic Models

Kosong uses `CallableTool2` with Pydantic models instead of raw dicts:

```python
from pydantic import BaseModel
from kosong.tooling import CallableTool2, ToolOk, ToolReturnType
from kosong.tooling.simple import SimpleToolset

class MathematicalContentParams(BaseModel):
    equations: List[str]
    definitions: Dict[str, str]
    interpretation: str
    examples: Optional[List[str]] = []
    typical_values: Optional[Dict[str, str]] = {}

class WriteMathematicalContentTool(CallableTool2[MathematicalContentParams]):
    name: str = "write_mathematical_content"
    description: str = "Return the key mathematical information needed to present this concept in a Manim animation."
    params: type[MathematicalContentParams] = MathematicalContentParams

    async def __call__(self, params: MathematicalContentParams) -> ToolReturnType:
        # Tool execution logic (if needed)
        return ToolOk(output=json.dumps(params.dict()))
```

### Step 2: Refactor Mathematical Enricher

**Before:**
```python
response = self.client.chat_completion(
    messages=[{"role": "user", "content": user_prompt}],
    system=system_prompt,
    tools=[MATHEMATICAL_CONTENT_TOOL],
    tool_choice="auto",
)
payload = _extract_tool_payload(response)
```

**After:**
```python
from kosong import step
from kosong.message import Message

toolset = SimpleToolset()
toolset += WriteMathematicalContentTool()

result = await step(
    chat_provider=kimi,
    system_prompt=system_prompt,
    toolset=toolset,
    history=[Message(role="user", content=user_prompt)],
)

# Get tool results
tool_results = await result.tool_results()
if tool_results:
    payload = tool_results[0].output  # Already parsed JSON
```

### Step 3: Refactor Prerequisite Explorer

**Before:**
```python
response = self.client.chat_completion(
    messages=[{"role": "user", "content": user_prompt}],
    system=system_prompt,
    max_tokens=50,
)
response_text = self.client.get_text_content(response)
```

**After:**
```python
from kosong import generate

message, usage = await generate(
    chat_provider=kimi,
    system_prompt=system_prompt,
    history=[Message(role="user", content=user_prompt)],
    tools=[],
    max_tokens=50,
)
response_text = message.content
```

### Step 4: Update Configuration

Create a Kosong-based client factory:

```python
# agents/kosong_client.py
import os
from kosong.chat_provider.kimi import Kimi
from config import MOONSHOT_API_KEY, MOONSHOT_BASE_URL, KIMI_K2_MODEL

def get_kosong_kimi_client() -> Kimi:
    """Get Kosong Kimi client instance."""
    return Kimi(
        base_url=MOONSHOT_BASE_URL,
        api_key=MOONSHOT_API_KEY,
        model=KIMI_K2_MODEL,
    )
```

## Benefits of Refactoring

1. **Less Boilerplate**: No manual tool call parsing, response formatting
2. **Type Safety**: Pydantic models provide validation and IDE support
3. **Automatic Tool Orchestration**: `kosong.step()` handles tool calling loops
4. **Unified Interface**: Easy to switch between LLM providers
5. **Official Support**: Maintained by Moonshot AI, stays up-to-date with API changes
6. **Better Error Handling**: Built-in retry and error handling

## Migration Strategy

1. **Phase 1**: Create Kosong-based versions alongside existing code
   - `agents/enrichment_chain_kosong.py`
   - `agents/prerequisite_explorer_kosong.py`
   
2. **Phase 2**: Test both implementations in parallel
   - Run both versions and compare outputs
   - Ensure feature parity

3. **Phase 3**: Gradually migrate
   - Update one agent at a time
   - Keep old code as fallback initially

4. **Phase 4**: Remove old implementation
   - Once stable, remove custom `KimiClient` wrapper
   - Update all imports

## Example: Complete Refactored Mathematical Enricher

See `agents/enrichment_chain_kosong.py` for a complete example.

## References

- [Kosong GitHub](https://github.com/MoonshotAI/kosong)
- [Kosong Documentation](https://moonshotai.github.io/kosong/)
- [Moonshot AI Platform](https://platform.moonshot.ai/)

