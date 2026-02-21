from __future__ import annotations

from typing import Any


def fmt_minutes(mins: int | None) -> str:
    """
    Format minutes since midnight to HH:MM (24-hour).

    Rules:
      - None -> "—"
      - 0 -> "00:00"
      - 75 -> "01:15"
      - 1440 -> "24:00" (if you choose to allow end-of-day as 1440)
    """
    if mins is None:
        return "—"
    if not isinstance(mins, int):
        return str(mins)

    if mins < 0:
        return str(mins)

    hours = mins // 60
    minutes = mins % 60
    return f"{hours:02d}:{minutes:02d}"


def fmt_money(amount: float | None, currency: str | None) -> str:
    """
    Format a money amount.

    Rules:
      - None -> "—"
      - If currency provided, append it (e.g., "12.34 USD")
      - Always show 2 decimals for numeric values
    """
    if amount is None:
        return "—"

    if not isinstance(amount, (int, float)):
        return str(amount)

    cur = (currency or "").strip()
    if cur:
        return f"{amount:,.2f} {cur}"
    return f"{amount:,.2f}"


def print_table(headers: list[str], rows: list[list[str]]) -> None:
    """
    Print a simple aligned table to stdout.

    Args:
      headers: Column names
      rows: Row values (will be stringified)
    """
    if not headers:
        print("")
        return

    # Normalize row widths
    normalized_rows: list[list[str]] = []
    for r in rows:
        r = ["" if v is None else str(v) for v in r]
        if len(r) < len(headers):
            r = r + [""] * (len(headers) - len(r))
        elif len(r) > len(headers):
            r = r[: len(headers)]
        normalized_rows.append(r)

    # Column widths = max(header, any cell)
    widths = [len(str(h)) for h in headers]
    for r in normalized_rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(cell))

    def _fmt_row(values: list[str]) -> str:
        return "  ".join(values[i].ljust(widths[i]) for i in range(len(headers)))

    header_line = _fmt_row([str(h) for h in headers])
    sep_line = "  ".join("-" * w for w in widths)

    print(header_line)
    print(sep_line)
    for r in normalized_rows:
        print(_fmt_row(r))


def print_item_summary(item: dict[str, Any]) -> None:
    """
    Print a single item summary line/block.

    Expected keys (best-effort):
      - id, title, category, start_min, end_min, is_all_day, pinned
    """
    item_id = item.get("id", "")
    title = item.get("title", "") or ""
    category = item.get("category", "") or ""

    is_all_day = bool(item.get("is_all_day"))
    pinned = bool(item.get("pinned"))

    if is_all_day:
        time_str = "ALL DAY"
    else:
        time_str = f"{fmt_minutes(item.get('start_min'))}–{fmt_minutes(item.get('end_min'))}"

    pin_str = "[PIN]" if pinned else ""
    print(f"{item_id}: {time_str} {pin_str} {title} ({category})".strip())

def fmt_time_range(start_min: int | None, end_min: int | None, *, is_all_day: bool = False) -> str:
    """
    Format a time range for display.

    Rules:
      - all-day -> "ALL DAY"
      - both None -> "UNSCHEDULED"
      - one None -> "INVALID" (should not happen if validators are used)
      - else -> "HH:MM–HH:MM"
    """
    if is_all_day:
        return "ALL DAY"
    if start_min is None and end_min is None:
        return "UNSCHEDULED"
    if start_min is None or end_min is None:
        return "INVALID"
    return f"{fmt_minutes(start_min)}–{fmt_minutes(end_min)}"