"""
Trammel PE — Python SDK & CLI
Generate structured, tool-aware, self-improving prompts for any LLM agent.

Trace the arc from idea to execution.
"""

from .core import TrammelPE, PromptData, PromptChain, TEMPLATES
from .cli import main as cli_main
from .mcp_server import main as mcp_main

__version__ = "0.2.0"
__all__ = ["TrammelPE", "PromptData", "PromptChain", "TEMPLATES", "cli_main", "mcp_main"]