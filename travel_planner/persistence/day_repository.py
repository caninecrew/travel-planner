def create_day(conn, trip_id: int, date: str) -> int:
    cursor = conn.execute(
        "INSERT INTO days (trip_id, date) VALUES (?, ?);",
        (trip_id, date),
    )
    conn.commit()
    return cursor.lastrowid

def get_day(conn, day_id: int) -> dict | None:
    cursor = conn.execute(
        "SELECT id, trip_id, date FROM days WHERE id = ?;",
        (day_id,),
    )
    row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "trip_id": row[1],
        "date": row[2],
    }


def list_days_for_trip(conn, trip_id: int) -> list[dict]:
    cursor = conn.execute(
        "SELECT id, trip_id, date FROM days WHERE trip_id = ? ORDER BY date ASC;",
        (trip_id,),
    )
    rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "trip_id": row[1],
            "date": row[2],
        }
        for row in rows
    ]


def delete_day(conn, day_id: int) -> None:
    conn.execute(
        "DELETE FROM days WHERE id = ?;",
        (day_id,),
    )
    conn.commit()


def update_day_date(conn, day_id: int, date_str: str) -> None:
    conn.execute(
        "UPDATE days SET date = ? WHERE id = ?;",
        (date_str, day_id),
    )
    conn.commit()