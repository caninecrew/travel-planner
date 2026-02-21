from __future__ import annotations

from typing import Any, Dict, List, Optional


def _row_to_dict(cursor, row) -> Dict[str, Any]:
    # sqlite3.Row supports mapping access; plain tuples do not.
    if hasattr(row, "keys"):
        return {k: row[k] for k in row.keys()}
    # Fallback: use cursor description
    cols = [d[0] for d in cursor.description]
    return dict(zip(cols, row))


def get_trip(conn, trip_id: int) -> Dict[str, Any]:
    cur = conn.execute(
        """
        SELECT id, name, created_at, updated_at
        FROM trips
        WHERE id = ?
        """,
        (trip_id,),
    )
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"Trip not found: trip_id={trip_id}")
    return _row_to_dict(cur, row)


def list_days_for_trip(conn, trip_id: int) -> List[Dict[str, Any]]:
    cur = conn.execute(
        """
        SELECT id, trip_id, date, notes
        FROM days
        WHERE trip_id = ?
        ORDER BY date ASC, id ASC
        """,
        (trip_id,),
    )
    return [_row_to_dict(cur, r) for r in cur.fetchall()]


def list_items_for_day(conn, day_id: int) -> List[Dict[str, Any]]:
    # Deterministic ordering:
    # 1) scheduled items (start_min not null) by time, then id
    # 2) unscheduled items (start_min null) by pinned desc, title asc, id asc
    cur = conn.execute(
        """
        SELECT
            id,
            day_id,
            title,
            category,
            start_min,
            end_min,
            estimated_cost,
            location,
            tags,
            notes,
            pinned
        FROM items
        WHERE day_id = ?
        ORDER BY
            CASE WHEN start_min IS NULL THEN 1 ELSE 0 END ASC,
            start_min ASC,
            end_min ASC,
            id ASC,
            pinned DESC,
            title ASC
        """,
        (day_id,),
    )
    return [_row_to_dict(cur, r) for r in cur.fetchall()]