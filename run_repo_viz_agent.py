import os
import asyncio
from pathlib import Path
from kimi_client import get_kimi_client

# REPO CONTEXT (Simulated from your provided GitHub link content)
REPO_CONTEXT = """
REPOSITORY: HarleyCoops/Dakota1890
DESCRIPTION: Using GRPO and a modified compositional reward function to train an opensource model on the 1890 Dakota Dictionary.

KEY CONCEPTS:
1. VLM Extraction Layer:
   - Uses Claude Sonnet 4.5 to extract grammar from 1890 text without OCR.
   - Handles complex orthography with 92-95% accuracy.

2. RL Training System:
   - Base Model: Qwen/Qwen2.5-7B-Instruct
   - Method: GRPO (Group Relative Policy Optimization) via PrimeIntellect.
   - Compositional Reward Function: 
     reward = (0.4 * character + 0.4 * affix + 0.2 * semantic) * difficulty
   - Curriculum Learning: Easy -> Medium -> Hard stages.

3. Closed-Loop Synthesis:
   - Single textbook -> Complete training ecosystem.
   - Dictionary + Grammar = Self-validating system.

4. Generalized Applications:
   - Legal (Tax Code -> Compliance)
   - Biology (Papers -> Protein constraints)
   - Code Migration (COBOL manuals -> Translation agents)

KEY DIRECTORIES:
- data/grammar_extracted/ (Raw rules)
- dakota_rl_training/datasets/ (RL tasks)
- scripts/extraction/ (VLM logic)
- scripts/rl/ (Training logic)
"""

async def main():
    output_file = Path("Dakota/manim_repo_scene.py")
    
    print("Initializing Kimi client...")
    client = get_kimi_client()

    prompt = (
        f"You are an expert Manim developer. I need a visualization that explains the architecture and key concepts "
        f"of the following GitHub repository. \n\n"
        f"{REPO_CONTEXT}\n\n"
        f"Please create a Python script using Manim (Community Edition) that visualizes this pipeline:\n"
        f"1. Show the flow: 1890 Textbook -> VLM Extraction -> Grammar Rules -> RL Training (GRPO) -> Trained Model.\n"
        f"2. Visualize the 'Reward Function' equation creatively (maybe as a scale or formula appearing).\n"
        f"3. Show the 'Generalized Applications' expanding from the center (Language -> Legal, Bio, Code).\n"
        f"4. Use a clean, modern, dark-mode aesthetic with blue/gold color scheme.\n"
        f"5. The scene class name should be 'DakotaArchitecture'.\n"
        f"6. Output ONLY valid Python code."
    )

    print("Sending request to Kimi...")
    try:
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are an expert Manim developer. Output valid Python code for a Manim scene."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=8000,
            temperature=0.7
        )

        content = client.get_text_content(response)
        
        # Clean up markdown
        if "```python" in content:
            content = content.split("```python")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        print(f"Saving output to {output_file}...")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        print("Done! Run 'manim -pql Dakota/manim_repo_scene.py DakotaArchitecture' to render.")

    except Exception as e:
        print(f"Error calling Kimi API: {e}")

if __name__ == "__main__":
    asyncio.run(main())

