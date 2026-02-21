from __future__ import annotations

from typing import Any


def build_parser() -> Any:
    """
    Build and return the argument parser for the CLI.

    Expected command groups (MVP):
      - trip: create, list, delete
      - day: add, list, delete
      - item: add, list, get (optional), delete, check (optional)

    Returns:
      Parser instance (argparse.ArgumentParser or equivalent).
    """
    raise NotImplementedError


def dispatch(args: Any) -> int:
    """
    Dispatch parsed args to the correct command handler.

    Args:
      args: Parsed CLI args object.

    Returns:
      Process exit code (0 success, non-zero error).
    """
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """
    CLI entrypoint.

    Responsibilities:
      - Parse argv
      - Open DB connection
      - Initialize schema (idempotent)
      - Call dispatch()
      - Handle ValidationError and sqlite errors with friendly messages

    Args:
      argv: Optional list of CLI arguments. If None, uses sys.argv.

    Returns:
      Exit code.
    """
    raise NotImplementedError