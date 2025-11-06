"""KimiK2Manim package.

A standalone Python package for generating Manim animations using the Kimi K2 thinking model.
"""

__version__ = "0.1.0"

# Make key components available at package level
from .kimi_client import KimiClient, get_kimi_client
from .tool_adapter import ToolAdapter
from .config import (
    MOONSHOT_API_KEY,
    MOONSHOT_BASE_URL,
    KIMI_K2_MODEL,
    TOOLS_ENABLED,
    FALLBACK_TO_VERBOSE,
)

__all__ = [
    "KimiClient",
    "get_kimi_client",
    "ToolAdapter",
    "MOONSHOT_API_KEY",
    "MOONSHOT_BASE_URL",
    "KIMI_K2_MODEL",
    "TOOLS_ENABLED",
    "FALLBACK_TO_VERBOSE",
]
