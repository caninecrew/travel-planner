from __future__ import annotations

from sqlite3 import Connection


def cmd_trip_create(conn: Connection, name: str) -> int:
    """
    Create a trip.

    Args:
      conn: SQLite connection
      name: Trip name (raw user input)

    Returns:
      Exit code.
    """
    raise NotImplementedError


def cmd_trip_list(conn: Connection) -> int:
    """
    List trips.

    Args:
      conn: SQLite connection

    Returns:
      Exit code.
    """
    raise NotImplementedError


def cmd_trip_delete(conn: Connection, trip_id: int) -> int:
    """
    Delete a trip by id.

    Args:
      conn: SQLite connection
      trip_id: Trip identifier

    Returns:
      Exit code.
    """
    raise NotImplementedError