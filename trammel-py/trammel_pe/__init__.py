"""
Trammel PE — Python SDK & CLI
Generate structured, tool-aware, self-improving prompts for any LLM agent.

Trace the arc from idea to execution.
"""

from .core import TrammelPE, PromptData, TEMPLATES
from .cli import main as cli_main

__version__ = "0.1.0"
__all__ = ["TrammelPE", "PromptData", "TEMPLATES", "cli_main"]