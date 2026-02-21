# travel_planner/domain/validators.py

from __future__ import annotations

import re
from datetime import date


class ValidationError(ValueError):
    """Raised when domain validation fails."""


def validate_time_range(start_min: int | None, end_min: int | None) -> None:
    """
    Validates a time range expressed as minutes since midnight.

    Rules:
      - Either both start_min and end_min are None (unscheduled), OR both are provided.
      - If provided: 0 <= start_min <= 1440 and 0 <= end_min <= 1440
      - If provided: start_min < end_min
    """
    if (start_min is None) != (end_min is None):
        raise ValidationError("start_min and end_min must be both set or both None.")

    if start_min is None and end_min is None:
        return

    if not isinstance(start_min, int) or not isinstance(end_min, int):
        raise ValidationError("start_min and end_min must be integers (minutes since midnight).")

    if not (0 <= start_min <= 1440):
        raise ValidationError("start_min must be between 0 and 1440.")
    if not (0 <= end_min <= 1440):
        raise ValidationError("end_min must be between 0 and 1440.")

    if start_min >= end_min:
        raise ValidationError("start_min must be strictly less than end_min.")


def validate_cost(value: float | None, *, max_reasonable: float = 1_000_000.0) -> None:
    """
    Validates a monetary amount.

    Rules:
      - None is allowed (unknown / not provided)
      - If provided: value must be >= 0
      - Optionally blocks absurdly large values (default threshold can be changed)
    """
    if value is None:
        return

    if not isinstance(value, (int, float)):
        raise ValidationError("cost must be a number.")

    if value < 0:
        raise ValidationError("cost must not be negative.")

    if value > max_reasonable:
        raise ValidationError(f"cost is unusually large (>{max_reasonable}).")


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_date_string(date_str: str) -> None:
    """
    Validates an ISO date string 'YYYY-MM-DD'.

    Rules:
      - Must match YYYY-MM-DD
      - Must be a real calendar date
    """
    if not isinstance(date_str, str):
        raise ValidationError("date must be a string in YYYY-MM-DD format.")

    if not _DATE_RE.match(date_str):
        raise ValidationError("date must be in YYYY-MM-DD format.")

    y, m, d = date_str.split("-")
    try:
        date(int(y), int(m), int(d))
    except ValueError as e:
        raise ValidationError(f"invalid date: {date_str}") from e