from __future__ import annotations

from datetime import datetime, timezone


def _now_iso_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_item_min(
    conn,
    day_id: int,
    title: str,
    category: str,
) -> int:
    now = _now_iso_utc()
    cursor = conn.execute(
        """
        INSERT INTO items (
            day_id,
            title,
            category,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?);
        """,
        (day_id, title, category, now, now),
    )
    conn.commit()
    return int(cursor.lastrowid)


def create_item_scheduled(
    conn,
    day_id: int,
    title: str,
    category: str,
    start_min: int,
    end_min: int,
) -> int:
    now = _now_iso_utc()
    cursor = conn.execute(
        """
        INSERT INTO items (
            day_id,
            title,
            category,
            start_min,
            end_min,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """,
        (day_id, title, category, start_min, end_min, now, now),
    )
    conn.commit()
    return int(cursor.lastrowid)


def get_item(conn, item_id: int) -> dict | None:
    cursor = conn.execute(
        """
        SELECT
            id,
            day_id,
            title,
            category,
            subcategory,
            status,
            start_min,
            end_min,
            is_all_day,
            timezone,
            duration_min,
            position,
            pinned,
            location_name,
            location_address,
            lat,
            lon,
            estimated_cost,
            actual_cost,
            currency,
            cost_notes,
            tags,
            notes,
            url,
            confirmation_code,
            provider,
            extra_json,
            created_at,
            updated_at
        FROM items
        WHERE id = ?;
        """,
        (item_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return None

    return {
        "id": row[0],
        "day_id": row[1],
        "title": row[2],
        "category": row[3],
        "subcategory": row[4],
        "status": row[5],
        "start_min": row[6],
        "end_min": row[7],
        "is_all_day": row[8],
        "timezone": row[9],
        "duration_min": row[10],
        "position": row[11],
        "pinned": row[12],
        "location_name": row[13],
        "location_address": row[14],
        "lat": row[15],
        "lon": row[16],
        "estimated_cost": row[17],
        "actual_cost": row[18],
        "currency": row[19],
        "cost_notes": row[20],
        "tags": row[21],
        "notes": row[22],
        "url": row[23],
        "confirmation_code": row[24],
        "provider": row[25],
        "extra_json": row[26],
        "created_at": row[27],
        "updated_at": row[28],
    }


def list_items_for_day(conn, day_id: int) -> list[dict]:
    cursor = conn.execute(
        """
        SELECT
            id,
            day_id,
            title,
            category,
            start_min,
            end_min,
            is_all_day,
            pinned,
            estimated_cost,
            actual_cost,
            currency,
            tags,
            notes,
            created_at,
            updated_at
        FROM items
        WHERE day_id = ?
        ORDER BY
            pinned DESC,
            CASE WHEN start_min IS NULL THEN 1 ELSE 0 END,
            start_min ASC,
            id ASC;
        """,
        (day_id,),
    )

    rows = cursor.fetchall()
    return [
        {
            "id": r[0],
            "day_id": r[1],
            "title": r[2],
            "category": r[3],
            "start_min": r[4],
            "end_min": r[5],
            "is_all_day": r[6],
            "pinned": r[7],
            "estimated_cost": r[8],
            "actual_cost": r[9],
            "currency": r[10],
            "tags": r[11],
            "notes": r[12],
            "created_at": r[13],
            "updated_at": r[14],
        }
        for r in rows
    ]


def delete_item(conn, item_id: int) -> None:
    conn.execute(
        "DELETE FROM items WHERE id = ?;",
        (item_id,),
    )
    conn.commit()