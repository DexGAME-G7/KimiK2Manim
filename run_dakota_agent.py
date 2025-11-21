import os
import json
import asyncio
from pathlib import Path

# Try to import KimiClient
try:
    from kimi_client import get_kimi_client
except ImportError:
    import sys
    sys.path.append(str(Path(__file__).parent))
    from kimi_client import get_kimi_client

async def main():
    # File paths
    prompt_file = Path("Dakota/prompt.txt")
    schema_file = Path("Dakota/grammar_schema.json")  # Use schema instead of full file
    data_file_path = "Dakota/grammar_full.json" # Path for the generated script to use
    output_file = Path("Dakota/manim_scene.py")

    if not prompt_file.exists():
        print(f"Error: {prompt_file} not found.")
        return
    if not schema_file.exists():
        print(f"Error: {schema_file} not found.")
        return

    print(f"Reading prompt from {prompt_file}...")
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_text = f.read().strip()

    print(f"Reading JSON Schema from {schema_file}...")
    with open(schema_file, "r", encoding="utf-8") as f:
        schema_content = f.read()

    # Construct the message
    # We provide the schema and instructions to read the actual data file
    
    user_content = (
        f"{prompt_text}\n\n"
        f"I cannot provide the full dataset because it is too large. "
        f"However, here is the JSON Schema that describes the structure of the data:\n\n"
        f"```json\n{schema_content}\n```\n\n"
        f"Please write a Manim script that:\n"
        f"1. Loads the actual data from the local file: '{data_file_path}'\n"
        f"2. Parses this data structure based on the schema provided.\n"
        f"3. Visualizes the ruleset creatively as a linguistic map.\n"
        f"4. Since the dataset is large, maybe only visualize a subset (e.g., first 10-20 rules) or aggregate statistics initially, "
        f"then zoom in on specific interesting patterns.\n"
        f"5. Use Manim's Graph or similar structures to show connections between rules, categories, and examples.\n"
        f"6. Make it visually stunning and poetic as requested."
    )

    print("Initializing Kimi client...")
    client = get_kimi_client()

    print("Sending request to Kimi (this may take a while due to large context)...")
    try:
        # We use a high max_tokens limit for the response since it's a Manim script
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are an expert Manim developer. You create visually stunning animations using the Manim library (Manim Community Edition). Output valid Python code for a Manim scene."},
                {"role": "user", "content": user_content}
            ],
            max_tokens=8000, # Adjust if needed, Manim scripts can be long
            temperature=0.7
        )

        content = client.get_text_content(response)
        
        # Clean up markdown code blocks if present
        if "```python" in content:
            content = content.split("```python")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        print(f"Saving output to {output_file}...")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        print("Done!")

    except Exception as e:
        print(f"Error calling Kimi API: {e}")

if __name__ == "__main__":
    asyncio.run(main())

