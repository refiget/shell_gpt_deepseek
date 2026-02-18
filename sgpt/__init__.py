"""shell_gpt package.

Keep this module free of import-time side effects.
The CLI entry lives in :mod:`sgpt.cli`.
"""

from .__version__ import __version__

# Back-compat exports.
# NOTE: `main` is a Typer command function; tests and downstream code import it.
from .cli import entry_point as cli
from .cli import main

__all__ = ["__version__", "main", "cli"]
