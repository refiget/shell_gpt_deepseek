"""shell_gpt package.

Keep this module free of import-time side effects.
The CLI entry lives in :mod:`sgpt.cli`.
"""

from .__version__ import __version__


def main(*args, **kwargs):  # type: ignore
    """Back-compat wrapper for older imports: `from sgpt import main`.

    Importing sgpt should stay lightweight; defer CLI imports until runtime.
    """

    from .cli import main as _main

    return _main(*args, **kwargs)


def cli() -> None:
    """Back-compat wrapper for `sgpt:cli` entrypoints."""

    from .cli import entry_point

    entry_point()


__all__ = ["__version__", "main", "cli"]
