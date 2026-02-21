from __future__ import annotations

from sqlite3 import Connection


def cmd_day_add(conn: Connection, trip_id: int, date_str: str) -> int:
    """
    Add a day to a trip.

    Args:
      conn: SQLite connection
      trip_id: Parent trip id
      date_str: ISO date string YYYY-MM-DD

    Returns:
      Exit code.
    """
    raise NotImplementedError


def cmd_day_list(conn: Connection, trip_id: int) -> int:
    """
    List days for a trip.

    Args:
      conn: SQLite connection
      trip_id: Parent trip id

    Returns:
      Exit code.
    """
    raise NotImplementedError


def cmd_day_delete(conn: Connection, day_id: int) -> int:
    """
    Delete a day by id.

    Args:
      conn: SQLite connection
      day_id: Day identifier

    Returns:
      Exit code.
    """
    raise NotImplementedError