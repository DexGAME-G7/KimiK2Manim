"""Launch Kimi K2 to generate Manim visualization for Dakota grammar.

This script:
1. Reads the large grammar JSON file (550k tokens)
2. Sends it to Kimi K2 along with the prompt
3. Saves the generated Manim code to a file
"""

import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from kimi_client import get_kimi_client
from logger import get_logger


def main():
    """Main execution function."""
    logger = get_logger()
    
    # File paths
    prompt_path = Path(__file__).parent / "prompt.txt"
    grammar_path = Path(r"C:\Users\chris\KimiK2Manim\Dakota\grammar_full.json")
    output_path = Path(__file__).parent / "dakota_visualization.py"
    
    # Verify files exist
    if not prompt_path.exists():
        logger.error(f"Prompt file not found: {prompt_path}")
        return 1
    
    if not grammar_path.exists():
        logger.error(f"Grammar file not found: {grammar_path}")
        return 1
    
    # Read prompt
    logger.info("Reading prompt file...", prefix="LOAD")
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt = f.read().strip()
    
    logger.info(f"Prompt: {prompt[:100]}...", prefix="PROMPT")
    
    # Read grammar JSON file
    logger.info("Reading grammar JSON file (this may take a moment)...", prefix="LOAD")
    with open(grammar_path, 'r', encoding='utf-8') as f:
        grammar_content = f.read()
    
    # Get file size info
    file_size_mb = len(grammar_content) / (1024 * 1024)
    logger.info(f"Grammar file size: {file_size_mb:.2f} MB", prefix="INFO")
    
    # Parse JSON to get structure info
    try:
        grammar_data = json.loads(grammar_content)
        if isinstance(grammar_data, dict):
            logger.info(f"Grammar contains {len(grammar_data)} top-level entries", prefix="INFO")
        elif isinstance(grammar_data, list):
            logger.info(f"Grammar contains {len(grammar_data)} items", prefix="INFO")
    except json.JSONDecodeError as e:
        logger.warning(f"Could not parse JSON for info: {e}", prefix="WARN")
        grammar_data = None
    
    # Initialize Kimi client
    logger.info("Initializing Kimi K2 client...", prefix="INIT")
    client = get_kimi_client()
    
    # Construct the full message
    logger.info("Preparing message for Kimi K2...", prefix="PREP")
    
    system_prompt = """You are an expert in Manim (Mathematical Animation Engine) and data visualization.
Your task is to create beautiful, poetic visualizations of linguistic data structures.

You will receive:
1. A creative prompt describing the visualization goal
2. A large JSON dataset representing a linguistic grammar ruleset

Create a complete, executable Manim scene that:
- Imports all necessary Manim components
- Defines a scene class
- Visualizes the structure and patterns in the grammar data
- Uses creative camera work, colors, and animations
- Is poetic and visually stunning
- Can run successfully without errors

IMPORTANT: 
- Output ONLY the complete Python Manim code
- Do NOT include explanations, markdown formatting, or comments outside the code
- The code should be ready to execute directly
- Make sure all imports are included
- Use proper Manim syntax for the latest version"""

    user_message = f"""{prompt}

Here is the Dakota grammar dataset (JSON format):

```json
{grammar_content}
```

Generate a complete Manim scene that creatively visualizes this linguistic structure."""

    # Make API call
    logger.info("Sending request to Kimi K2 (this will take some time)...", prefix="API")
    logger.info("Processing 550k+ tokens - please be patient...", prefix="API")
    
    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": user_message}],
            system=system_prompt,
            max_tokens=16000,  # Large output for complete Manim scene
            temperature=0.8,   # Creative but not too random
        )
        
        # Extract response text
        response_text = client.get_text_content(response)
        
        if not response_text:
            logger.error("No response received from Kimi K2", prefix="ERROR")
            return 1
        
        logger.success("Received response from Kimi K2!", prefix="SUCCESS")
        logger.info(f"Response length: {len(response_text)} characters", prefix="INFO")
        
        # Extract Python code from response if wrapped in markdown
        code = response_text
        if "```python" in response_text:
            # Extract from code blocks
            parts = response_text.split("```python")
            if len(parts) > 1:
                code = parts[1].split("```")[0].strip()
        elif "```" in response_text:
            # Try generic code block
            parts = response_text.split("```")
            if len(parts) > 1:
                code = parts[1].strip()
        
        # Save to output file
        logger.info(f"Saving Manim scene to: {output_path}", prefix="SAVE")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        logger.success(f"Saved visualization code to: {output_path}", prefix="COMPLETE")
        
        # Print usage statistics
        usage = response.get("usage")
        if usage:
            logger.info("=" * 60, prefix="STATS")
            logger.info(f"Prompt tokens: {usage.get('prompt_tokens', 'N/A')}", prefix="STATS")
            logger.info(f"Completion tokens: {usage.get('completion_tokens', 'N/A')}", prefix="STATS")
            logger.info(f"Total tokens: {usage.get('total_tokens', 'N/A')}", prefix="STATS")
            logger.info("=" * 60, prefix="STATS")
        
        # Print next steps
        print("\n" + "=" * 60)
        print("NEXT STEPS:")
        print("=" * 60)
        print(f"1. Review the generated code: {output_path}")
        print(f"2. Run the visualization:")
        print(f"   manim -pql {output_path} <SceneName>")
        print(f"\n   (Replace <SceneName> with the actual scene class name)")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.error(f"Error during API call: {e}", prefix="ERROR")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    # Verify API key
    if not os.getenv("MOONSHOT_API_KEY"):
        print("[ERROR] MOONSHOT_API_KEY environment variable not set.")
        print("\nPlease set your Moonshot API key in .env file")
        sys.exit(1)
    
    exit_code = main()
    sys.exit(exit_code)
