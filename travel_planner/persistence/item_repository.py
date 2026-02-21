from datetime import datetime, timezone

def create_item_min(
    conn,
    day_id: int,
    title: str,
    category: str,
) -> int:
    now = datetime.now(timezone.utc)

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
    return cursor.lastrowid

def create_item_scheduled(
    conn,
    day_id: int,
    title: str,
    category: str,
    start_min: int,
    end_min: int,
) -> int:
    now = datetime.now(timezone.utc)

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
    return cursor.lastrowid


def get_item(conn, item_id: int) -> dict | None:
    cursor = conn.execute(
        """
        SELECT id, day_id, title, category,
               start_min, end_min,
               estimated_cost, actual_cost,
               created_at, updated_at
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
        "start_min": row[4],
        "end_min": row[5],
        "estimated_cost": row[6],
        "actual_cost": row[7],
        "created_at": row[8],
        "updated_at": row[9],
    }


def list_items_for_day(conn, day_id: int) -> list[dict]:
    cursor = conn.execute(
        """
        SELECT id, day_id, title, category,
               start_min, end_min,
               estimated_cost, actual_cost,
               created_at, updated_at
        FROM items
        WHERE day_id = ?
        ORDER BY
            CASE WHEN start_min IS NULL THEN 1 ELSE 0 END,
            start_min ASC;
        """,
        (day_id,),
    )

    rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "day_id": row[1],
            "title": row[2],
            "category": row[3],
            "start_min": row[4],
            "end_min": row[5],
            "estimated_cost": row[6],
            "actual_cost": row[7],
            "created_at": row[8],
            "updated_at": row[9],
        }
        for row in rows
    ]


def delete_item(conn, item_id: int) -> None:
    conn.execute(
        "DELETE FROM items WHERE id = ?;",
        (item_id,),
    )
    conn.commit()