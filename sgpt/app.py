"""Deprecated module.

The CLI entrypoint has moved to :mod:`sgpt.cli`.
Kept for backward compatibility with older imports.
"""

from sgpt.cli import entry_point, main

__all__ = ["main", "entry_point"]
