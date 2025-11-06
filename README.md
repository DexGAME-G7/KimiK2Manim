# KimiK2Manim

A standalone Python package for generating Manim animations using the **Kimi K2 thinking model** from Moonshot AI. This package provides agents that build knowledge trees, enrich them with mathematical content and visual specifications, and compose narrative prompts for Manim animation generation.

## Overview

KimiK2Manim uses the Kimi K2 model (via Moonshot AI's OpenAI-compatible API) to:

1. **Explore Prerequisites** - Build knowledge trees by identifying prerequisite concepts
2. **Enrich Mathematically** - Add LaTeX equations, definitions, and examples to each concept
3. **Design Visuals** - Plan Manim visual specifications (colors, animations, transitions)
4. **Compose Narratives** - Generate long-form animation prompts (2000+ words)

## Features

- **KimiClient**: OpenAI-compatible API wrapper for Moonshot AI
- **ToolAdapter**: Converts tool calls to verbose instructions when tools aren't available
- **KimiPrerequisiteExplorer**: Builds knowledge trees recursively
- **KimiEnrichmentPipeline**: Complete enrichment chain (math → visuals → narrative)
- **Standalone Package**: No dependencies on parent projects

## Installation

### From Source

```bash
git clone https://github.com/HarleyCoops/KimiK2Manim.git
cd KimiK2Manim
pip install -e .
```

### Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `openai>=1.0.0` - OpenAI-compatible API client
- `python-dotenv>=1.0.0` - Environment variable management

## Quick Start

### 1. Get API Key

Register at [Moonshot AI Platform](https://platform.moonshot.ai/) and get your API key.

### 2. Set Environment Variable

Create a `.env` file in the project root:

```bash
MOONSHOT_API_KEY=your_api_key_here
KIMI_MODEL=moonshot-v1-8k  # Optional: specify model name
KIMI_USE_TOOLS=true        # Optional: enable/disable tools
KIMI_ENABLE_THINKING=true   # Optional: enable thinking mode
```

### 3. Basic Usage

```python
from kimik2manim.agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer
import asyncio

async def main():
    explorer = KimiPrerequisiteExplorer(max_depth=3, use_tools=True)
    tree = await explorer.explore_async("quantum field theory", verbose=True)
    tree.print_tree()
    
    # Save to JSON
    import json
    with open("tree.json", "w") as f:
        json.dump(tree.to_dict(), f, indent=2)

asyncio.run(main())
```

### 4. Run Enrichment Pipeline

```python
from kimik2manim.agents.enrichment_chain import KimiEnrichmentPipeline
from kimik2manim.agents.prerequisite_explorer_kimi import KnowledgeNode
import json
import asyncio

async def main():
    # Load existing tree (or create one)
    with open("tree.json", "r") as f:
        tree_data = json.load(f)
    
    # Convert to KnowledgeNode (simplified - see examples for full implementation)
    tree = KnowledgeNode(**tree_data)  # Adjust based on your structure
    
    # Run enrichment
    pipeline = KimiEnrichmentPipeline()
    result = await pipeline.run_async(tree)
    
    # Access enriched data
    print(f"Narrative length: {len(result.narrative.verbose_prompt)} characters")
    print(f"Total duration: {result.narrative.total_duration}s")

asyncio.run(main())
```

### 5. Command-Line Usage

```bash
# Run enrichment pipeline on a tree JSON file
python examples/run_enrichment_pipeline.py path/to/tree.json
```

## Project Structure

```
KimiK2Manim/
├── README.md                    # This file
├── setup.py                     # Package setup
├── requirements.txt             # Dependencies
├── .gitignore                   # Git ignore rules
├── config.py                    # Configuration and constants
├── kimi_client.py               # Kimi K2 API client wrapper
├── tool_adapter.py              # Tool call to verbose instruction converter
├── agents/                       # Refactored agents
│   ├── __init__.py
│   ├── prerequisite_explorer_kimi.py
│   └── enrichment_chain.py     # Mathematical, visual, and narrative enrichment
└── examples/                    # Example usage scripts
    ├── test_kimi_integration.py
    ├── run_enrichment_pipeline.py
    └── test_qft_pipeline.py
```

## Configuration

All configuration is in `config.py` or via environment variables:

- `MOONSHOT_API_KEY`: Your Moonshot AI API key (required)
- `KIMI_MODEL`: Model name (default: "moonshot-v1-8k")
- `KIMI_USE_TOOLS`: Enable tool calling (default: "true")
- `KIMI_ENABLE_THINKING`: Enable thinking mode (default: "true")

## Key Components

### KimiClient

OpenAI-compatible wrapper for Moonshot AI's API:

```python
from kimik2manim.kimi_client import KimiClient

client = KimiClient()
response = client.chat_completion(
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100
)
print(client.get_text_content(response))
```

### ToolAdapter

Converts tool definitions to verbose instructions:

```python
from kimik2manim.tool_adapter import ToolAdapter

adapter = ToolAdapter()
tools = [...]  # Your tool definitions
instructions = adapter.tools_to_instructions(tools)
```

### KimiPrerequisiteExplorer

Builds knowledge trees by exploring prerequisites:

```python
from kimik2manim.agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer

explorer = KimiPrerequisiteExplorer(max_depth=3, use_tools=True)
tree = await explorer.explore_async("special relativity", verbose=True)
```

### KimiEnrichmentPipeline

Complete enrichment chain:

```python
from kimik2manim.agents.enrichment_chain import KimiEnrichmentPipeline

pipeline = KimiEnrichmentPipeline()
result = await pipeline.run_async(tree)
```

## Examples

See the `examples/` directory for:
- `test_kimi_integration.py` - Basic API and agent tests
- `run_enrichment_pipeline.py` - CLI for running enrichment
- `test_qft_pipeline.py` - Full pipeline test with QFT concepts

## Testing

```bash
# Run tests (requires MOONSHOT_API_KEY)
pytest tests/ -v

# Run without API calls (unit tests only)
pytest tests/ -v -k "not api"
```

## Architecture

The package follows a three-layer architecture:

1. **Client Layer**: `KimiClient` handles all API communication
2. **Adapter Layer**: `ToolAdapter` converts tools to instructions when needed
3. **Agent Layer**: Agents orchestrate knowledge tree building and enrichment

See `ARCHITECTURE.md` for detailed architecture documentation.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## References

- [Moonshot AI Platform](https://platform.moonshot.ai/)
- [Kimi K2 Documentation](https://platform.moonshot.ai/docs/guide/use-kimi-k2-thinking-model)
- [Manim Documentation](https://docs.manim.community/)

## Support

For issues and questions, please open an issue on [GitHub](https://github.com/HarleyCoops/KimiK2Manim/issues).
