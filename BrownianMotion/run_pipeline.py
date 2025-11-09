#!/usr/bin/env python3
"""Run the full pipeline on Brownian Motion prompt."""

import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv()

from agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer
from agents.enrichment_chain import KimiEnrichmentPipeline
from logger import get_logger, reset_logger


async def run_pipeline(concept: str, prompt_text: str):
    """Run the full pipeline: prerequisite tree → enrichment → narrative."""
    # Reset logger for fresh start
    reset_logger()
    logger = get_logger(use_colors=True, verbose=True)
    
    logger.info("=" * 70)
    logger.info(f"RUNNING PIPELINE FOR: {concept}")
    logger.info("=" * 70)
    logger.debug(f"Full prompt: {prompt_text[:200]}...")
    
    # Set up output directory early
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Stage 1: Build prerequisite tree
    logger.stage("Building Prerequisite Tree", 1, 3)
    explorer = KimiPrerequisiteExplorer(max_depth=3, use_tools=True, logger=logger)
    tree = await explorer.explore_async(concept, verbose=True)
    
    logger.success(f"Tree built: {tree.depth} levels deep")
    
    # Save prerequisite tree immediately after Stage 1
    tree_file_intermediate = output_dir / f"{concept.replace(' ', '_')}_prerequisite_tree.json"
    with tree_file_intermediate.open("w", encoding="utf-8") as f:
        json.dump(tree.to_dict(), f, indent=2)
    logger.success(f"Saved prerequisite tree to {tree_file_intermediate}")
    
    if logger.verbose:
        try:
            tree.print_tree()
        except UnicodeEncodeError:
            logger.warning("Skipping tree visualization due to encoding issues (Windows console)")
            logger.debug("Tree structure saved in JSON output")
    
    # Stage 2: Run enrichment pipeline
    logger.stage("Running Enrichment Pipeline", 2, 3)
    pipeline = KimiEnrichmentPipeline(logger=logger)
    result = await pipeline.run_async(tree)
    
    # Stage 3: Save results
    logger.stage("Saving Results", 3, 3)
    
    # Save enriched tree
    tree_file = output_dir / f"{concept.replace(' ', '_')}_enriched.json"
    with tree_file.open("w", encoding="utf-8") as f:
        json.dump(result.enriched_tree.to_dict(), f, indent=2)
    logger.success(f"Saved enriched tree to {tree_file}")
    
    # Save narrative
    narrative_file = output_dir / f"{concept.replace(' ', '_')}_narrative.txt"
    narrative_file.write_text(result.narrative.verbose_prompt, encoding="utf-8")
    logger.success(f"Saved narrative to {narrative_file}")
    
    # Print summary
    logger.info("=" * 70)
    logger.success("PIPELINE COMPLETE!")
    logger.info("=" * 70)
    logger.info(f"Narrative length: {len(result.narrative.verbose_prompt)} characters")
    logger.info(f"Total duration: {result.narrative.total_duration}s")
    logger.info(f"Scene count: {result.narrative.scene_count}")
    
    if logger.verbose:
        logger.info("\nNarrative preview (first 500 chars):")
        logger.info("-" * 70)
        preview = result.narrative.verbose_prompt[:500]
        logger.info(preview + "..." if len(result.narrative.verbose_prompt) > 500 else preview)
    
    # Print logger summary
    logger.summary()


if __name__ == "__main__":
    # Read prompt from file
    script_dir = Path(__file__).parent
    prompt_file = script_dir / "prompt.txt"
    
    if not prompt_file.exists():
        print(f"ERROR: Prompt file not found: {prompt_file}")
        sys.exit(1)
    
    prompt_text = prompt_file.read_text(encoding="utf-8").strip()
    
    # Extract main concept - use "Brownian Motion" as the core concept
    # The prompt is about connecting Brown's observations to Einstein's heat equation
    concept = "Brownian Motion and Einstein's Heat Equation"
    
    try:
        asyncio.run(run_pipeline(concept, prompt_text))
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

