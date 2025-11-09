#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a Manim animation prompt for the Harmonic Theorem using KimiK2Manim pipeline.

This script:
1. Explores prerequisites for the harmonic theorem
2. Enriches with mathematical content (equations, definitions)
3. Designs visual specifications for Manim
4. Generates a 45-second narrative prompt
"""

import asyncio
import json
import sys
import io
from pathlib import Path

# Set UTF-8 encoding for console output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer
from agents.enrichment_chain import KimiEnrichmentPipeline


async def generate_harmonic_theorem_prompt():
    """Generate complete Manim animation prompt for harmonic theorem."""

    print("=" * 80)
    print("HARMONIC THEOREM ANIMATION GENERATOR")
    print("=" * 80)
    print()

    # Stage 1: Explore prerequisites (depth 2 for focused content)
    print("Stage 1: Exploring prerequisites for harmonic theorem...")
    print("-" * 80)
    explorer = KimiPrerequisiteExplorer(max_depth=2, use_tools=True)

    concept = "harmonic division and harmonic theorem in geometry"
    tree = await explorer.explore_async(concept, verbose=True)

    print("\n[OK] Knowledge tree built:")
    tree.print_tree()

    # Stage 2-4: Run enrichment pipeline
    print("\n" + "=" * 80)
    print("Stage 2-4: Running enrichment pipeline...")
    print("-" * 80)

    pipeline = KimiEnrichmentPipeline()
    result = await pipeline.run_async(tree)

    print("\n[OK] Enrichment complete!")
    print(f"  - Mathematical content added to {len(list(tree.traverse()))} nodes")
    print(f"  - Visual specifications designed")
    print(f"  - Narrative composed: {len(result.narrative.verbose_prompt)} characters")
    print(f"  - Estimated duration: {result.narrative.total_duration}s")

    # Add 45-second constraint to narrative
    print("\n" + "=" * 80)
    print("Refining narrative for 45-second animation...")
    print("-" * 80)

    refined_prompt = f"""# HARMONIC THEOREM MANIM ANIMATION (45 SECONDS)

## Animation Constraints
- **Total Duration**: 45 seconds maximum
- **Target Audience**: Upper high school / undergraduate mathematics
- **Visual Style**: Clean, modern, with smooth animations
- **Equations**: Display LaTeX on screen with step-by-step reveals

## Original Enriched Narrative
{result.narrative.verbose_prompt}

## Timing Breakdown (45 seconds total)
- Introduction (5s): Title and setup
- Visual construction (15s): Draw geometric figure with harmonic division
- Equation revelation (15s): Show LaTeX equations step-by-step
- Demonstration (8s): Animate the harmonic relationship
- Conclusion (2s): Final equation and fade out

## Key LaTeX Equations to Display
Extract the main equations from the enriched content and display them sequentially:
1. Definition equation
2. Harmonic division formula
3. Cross-ratio relationship

## Visual Specifications
Use the enriched visual specifications but adapt for 45-second timing:
- Smooth, continuous animations (no sudden jumps)
- Clear labels for points and segments
- Color-coded elements for clarity
- Professional gradient background
- Mathematical rigor with visual appeal

## Implementation Notes
- Use Manim's MathTex for all equations
- Implement smooth camera movements
- Use Write() animations for equations
- Use Create() for geometric constructions
- Ensure all text is readable at 1080p
"""

    # Save outputs
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Save tree
    tree_file = output_dir / "harmonic_theorem_tree.json"
    with open(tree_file, "w", encoding='utf-8') as f:
        json.dump(tree.to_dict(), f, indent=2)
    print(f"\n[OK] Knowledge tree saved to: {tree_file}")

    # Save narrative
    narrative_file = output_dir / "harmonic_theorem_narrative.txt"
    with open(narrative_file, "w", encoding='utf-8') as f:
        f.write(refined_prompt)
    print(f"[OK] Narrative prompt saved to: {narrative_file}")

    # Save full enrichment data
    enrichment_file = output_dir / "harmonic_theorem_enrichment.json"
    enrichment_data = {
        "tree": tree.to_dict(),
        "narrative": result.narrative.to_dict(),
        "refined_prompt": refined_prompt
    }
    with open(enrichment_file, "w", encoding='utf-8') as f:
        json.dump(enrichment_data, f, indent=2)
    print(f"[OK] Full enrichment data saved to: {enrichment_file}")

    print("\n" + "=" * 80)
    print("GENERATION COMPLETE!")
    print("=" * 80)
    print(f"\nNext steps:")
    print(f"1. Review the narrative in: {narrative_file}")
    print(f"2. Use it to create Manim scene in: manim_scenes/harmonic_theorem.py")
    print(f"3. Render with: manim -pql manim_scenes/harmonic_theorem.py HarmonicTheoremScene")

    return result, refined_prompt


if __name__ == "__main__":
    asyncio.run(generate_harmonic_theorem_prompt())
