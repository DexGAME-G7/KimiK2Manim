"""
Kosong-based Mathematical Enricher - Example Refactoring

This module demonstrates how to refactor KimiMathematicalEnricher to use Kosong.
Note: Requires Python 3.13+ and kosong package.

To use:
1. Upgrade to Python 3.13+
2. Install: uv add kosong (or pip install kosong)
3. Replace imports from enrichment_chain to enrichment_chain_kosong
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

# Kosong imports (requires Python 3.13+)
try:
    import kosong
    from kosong import StepResult
    from kosong.chat_provider.kimi import Kimi
    from kosong.message import Message
    from kosong.tooling import CallableTool2, ToolOk, ToolReturnType
    from kosong.tooling.simple import SimpleToolset
    KOSONG_AVAILABLE = True
except ImportError:
    KOSONG_AVAILABLE = False
    # Fallback message
    print("WARNING: Kosong not available. Requires Python 3.13+ and 'kosong' package.")

# Import shared types
try:
    from ..agents.prerequisite_explorer_kimi import KnowledgeNode
    from ..config import MOONSHOT_API_KEY, MOONSHOT_BASE_URL, KIMI_K2_MODEL
    from ..logger import get_logger
except ImportError:
    from agents.prerequisite_explorer_kimi import KnowledgeNode
    from config import MOONSHOT_API_KEY, MOONSHOT_BASE_URL, KIMI_K2_MODEL
    from logger import get_logger


# ---------------------------------------------------------------------------
# Pydantic Models for Tool Parameters
# ---------------------------------------------------------------------------


class MathematicalContentParams(BaseModel):
    """Parameters for mathematical content tool."""
    equations: List[str]
    definitions: Dict[str, str]
    interpretation: str
    examples: Optional[List[str]] = []
    typical_values: Optional[Dict[str, str]] = {}


# ---------------------------------------------------------------------------
# Kosong Tool Definition
# ---------------------------------------------------------------------------


class WriteMathematicalContentTool(CallableTool2[MathematicalContentParams]):
    """Kosong tool for writing mathematical content."""
    
    name: str = "write_mathematical_content"
    description: str = (
        "Return the key mathematical information needed to present this "
        "concept in a Manim animation."
    )
    params: type[MathematicalContentParams] = MathematicalContentParams

    async def __call__(self, params: MathematicalContentParams) -> ToolReturnType:
        """
        Execute the tool. In this case, we just return the structured data.
        The actual enrichment happens in the LLM response.
        """
        # Return the structured data as JSON string
        return ToolOk(output=json.dumps(params.dict(), ensure_ascii=False))


# ---------------------------------------------------------------------------
# Data Classes (same as original)
# ---------------------------------------------------------------------------


@dataclass
class MathematicalContent:
    """Mathematical content for a concept."""
    equations: List[str] = field(default_factory=list)
    definitions: Dict[str, str] = field(default_factory=dict)
    interpretation: str = ""
    examples: List[str] = field(default_factory=list)
    typical_values: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_params(cls, params: MathematicalContentParams) -> "MathematicalContent":
        """Create from Pydantic params."""
        return cls(
            equations=params.equations,
            definitions=params.definitions,
            interpretation=params.interpretation,
            examples=params.examples or [],
            typical_values=params.typical_values or {},
        )


# ---------------------------------------------------------------------------
# Kosong-based Mathematical Enricher
# ---------------------------------------------------------------------------


class KosongMathematicalEnricher:
    """Mathematical enricher using Kosong abstraction layer."""

    def __init__(
        self,
        client: Optional[Kimi] = None,
        logger=None,
    ):
        if not KOSONG_AVAILABLE:
            raise ImportError(
                "Kosong not available. Requires Python 3.13+ and 'kosong' package.\n"
                "Install with: uv add kosong (or pip install kosong)"
            )
        
        self.client = client or self._create_client()
        self.logger = logger or get_logger()
        self.cache: Dict[str, MathematicalContent] = {}
        
        # Create toolset
        self.toolset = SimpleToolset()
        self.toolset += WriteMathematicalContentTool()

    @staticmethod
    def _create_client() -> Kimi:
        """Create Kosong Kimi client."""
        return Kimi(
            base_url=MOONSHOT_BASE_URL,
            api_key=MOONSHOT_API_KEY,
            model=KIMI_K2_MODEL,
        )

    async def enrich_tree(self, root: KnowledgeNode) -> KnowledgeNode:
        """Enrich entire tree with mathematical content."""
        await self._enrich_node(root)
        return root

    async def _enrich_node(self, node: KnowledgeNode) -> None:
        """Enrich a single node."""
        # Check cache
        if node.concept in self.cache:
            cached = self.cache[node.concept]
            node.equations = cached.equations
            node.definitions = cached.definitions
            if node.visual_spec is None:
                node.visual_spec = {}
            node.visual_spec.setdefault("interpretation", cached.interpretation)
            node.visual_spec.setdefault("examples", cached.examples)
            node.visual_spec.setdefault("typical_values", cached.typical_values)
            for prereq in node.prerequisites:
                await self._enrich_node(prereq)
            return

        # Prepare prompt
        complexity = "high school level" if node.is_foundation else "upper-undergraduate level"
        
        system_prompt = (
            "You are an expert mathematical physicist preparing content for a "
            "Manim animation. Provide rigorous, properly formatted LaTeX and "
            "clear symbol definitions. Respond by calling the tool "
            "'write_mathematical_content'. Do not include plain text responses."
        )

        user_prompt = (
            f"Concept: {node.concept}\n"
            f"Depth: {node.depth}\n"
            f"Complexity target: {complexity}\n"
            "Return 2-5 LaTeX equations (raw strings with escaped backslashes), "
            "definitions for every symbol, at least one interpretation paragraph, "
            "and any illustrative examples/typical values that help teach the idea."
        )

        self.logger.info(f"Enriching: '{node.concept}' (depth {node.depth})", prefix="MATH")
        
        # Use Kosong step for tool calling
        try:
            result: StepResult = await kosong.step(
                chat_provider=self.client,
                system_prompt=system_prompt,
                toolset=self.toolset,
                history=[Message(role="user", content=user_prompt)],
            )
            
            # Get tool results
            tool_results = await result.tool_results()
            
            if tool_results and len(tool_results) > 0:
                # Parse tool output
                tool_output = tool_results[0].output
                if isinstance(tool_output, str):
                    payload = json.loads(tool_output)
                else:
                    payload = tool_output
                
                # Create MathematicalContent from payload
                try:
                    params = MathematicalContentParams(**payload)
                    math_content = MathematicalContent.from_params(params)
                except Exception as e:
                    self.logger.warning(f"Failed to parse tool params: {e}, using raw payload")
                    math_content = MathematicalContent(
                        equations=payload.get("equations", []),
                        definitions=payload.get("definitions", {}),
                        interpretation=payload.get("interpretation", ""),
                        examples=payload.get("examples", []),
                        typical_values=payload.get("typical_values", {}),
                    )
            else:
                # Fallback: try to parse from message content
                self.logger.warning("No tool results, attempting to parse from message content")
                message_content = result.message.content
                try:
                    payload = json.loads(message_content)
                    params = MathematicalContentParams(**payload)
                    math_content = MathematicalContent.from_params(params)
                except:
                    self.logger.error(f"Failed to extract mathematical content for {node.concept}")
                    math_content = MathematicalContent()
            
            eq_count = len(math_content.equations)
            def_count = len(math_content.definitions)
            self.logger.success(
                f"Extracted payload for '{node.concept}': {eq_count} equations, {def_count} definitions"
            )
            if self.logger.verbose and math_content.equations:
                self.logger.debug(f"Equation preview: {math_content.equations[0][:100]}...")
            
            # Cache and update node
            self.cache[node.concept] = math_content
            node.equations = math_content.equations
            node.definitions = math_content.definitions

            if node.visual_spec is None:
                node.visual_spec = {}
            node.visual_spec.setdefault("interpretation", math_content.interpretation)
            node.visual_spec.setdefault("examples", math_content.examples)
            node.visual_spec.setdefault("typical_values", math_content.typical_values)

        except Exception as e:
            self.logger.error(f"Failed to enrich {node.concept}: {e}")
            import traceback
            traceback.print_exc()
            # Create empty content on error
            math_content = MathematicalContent()
            self.cache[node.concept] = math_content

        # Recursively enrich prerequisites
        for prereq in node.prerequisites:
            await self._enrich_node(prereq)


# ---------------------------------------------------------------------------
# Compatibility Wrapper
# ---------------------------------------------------------------------------


def get_mathematical_enricher(use_kosong: bool = True, **kwargs):
    """
    Factory function to get mathematical enricher.
    
    Args:
        use_kosong: If True and Kosong is available, use Kosong version
        **kwargs: Passed to enricher constructor
    
    Returns:
        Mathematical enricher instance
    """
    if use_kosong and KOSONG_AVAILABLE:
        return KosongMathematicalEnricher(**kwargs)
    else:
        # Fallback to original implementation
        from agents.enrichment_chain import KimiMathematicalEnricher
        return KimiMathematicalEnricher(**kwargs)

