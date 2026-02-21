from __future__ import annotations

from sqlite3 import Connection


def cmd_item_add_min(conn: Connection, day_id: int, title: str, category: str) -> int:
    """
    Add an unscheduled (minimal) item to a day.

    Args:
      conn: SQLite connection
      day_id: Parent day id
      title: Item title
      category: Item category (e.g., activity, transport)

    Returns:
      Exit code.
    """
    raise NotImplementedError


def cmd_item_add_scheduled(
    conn: Connection,
    day_id: int,
    title: str,
    category: str,
    start_min: int,
    end_min: int,
    *,
    reject_overlaps: bool = True,
) -> int:
    """
    Add a scheduled item to a day.

    Args:
      conn: SQLite connection
      day_id: Parent day id
      title: Item title
      category: Item category (e.g., activity, transport)
      start_min: Minutes since midnight (start)
      end_min: Minutes since midnight (end)
      reject_overlaps: If True, reject inserts that overlap existing scheduled items

    Returns:
      Exit code.
    """
    raise NotImplementedError


def cmd_item_list(conn: Connection, day_id: int) -> int:
    """
    List items for a day.

    Args:
      conn: SQLite connection
      day_id: Parent day id

    Returns:
      Exit code.
    """
    raise NotImplementedError


def cmd_item_get(conn: Connection, item_id: int) -> int:
    """
    Show full details for a single item.

    Args:
      conn: SQLite connection
      item_id: Item identifier

    Returns:
      Exit code.
    """
    raise NotImplementedError


def cmd_item_delete(conn: Connection, item_id: int) -> int:
    """
    Delete an item by id.

    Args:
      conn: SQLite connection
      item_id: Item identifier

    Returns:
      Exit code.
    """
    raise NotImplementedError


def cmd_item_check(conn: Connection, day_id: int, buffer_min: int = 15) -> int:
    """
    Run scheduling diagnostics for a day:
      - overlaps among scheduled items
      - tight connections between consecutive scheduled items (gap < buffer_min)

    Args:
      conn: SQLite connection
      day_id: Parent day id
      buffer_min: Minimum acceptable gap between items

    Returns:
      Exit code.
    """
    raise NotImplementedError