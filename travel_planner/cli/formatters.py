from __future__ import annotations

from typing import Any


def fmt_minutes(mins: int | None) -> str:
    """
    Format minutes since midnight to a human-readable time.

    Examples:
      0 -> "00:00"
      75 -> "01:15"
      None -> "—"
    """
    raise NotImplementedError


def fmt_money(amount: float | None, currency: str | None) -> str:
    """
    Format money values for display.

    Rules:
      - None -> "—"
      - If currency missing, omit or use a default (implementation choice)
    """
    raise NotImplementedError


def print_table(headers: list[str], rows: list[list[str]]) -> None:
    """
    Print a simple aligned table to stdout.

    Args:
      headers: Column names
      rows: Row values (already stringified)
    """
    raise NotImplementedError


def print_item_summary(item: dict[str, Any]) -> None:
    """
    Print a single item summary line/block.

    Args:
      item: Item dict (from repository/service)
    """
    raise NotImplementedError