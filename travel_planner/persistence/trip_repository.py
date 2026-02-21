def create_trip(conn, name: str) -> int:
    cursor = conn.execute(
        "INSERT INTO trips (name) VALUES (?);",
        (name,),
    )
    conn.commit()
    return cursor.lastrowid

def get_trip(conn, trip_id: int) -> dict | None:
    cursor = conn.execute(
        "SELECT id, name FROM trips WHERE id = ?;",
        (trip_id,),
    )
    row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
    }


def list_trips(conn) -> list[dict]:
    cursor = conn.execute(
        "SELECT id, name FROM trips ORDER BY id ASC;"
    )
    rows = cursor.fetchall()

    return [
        {"id": row[0], "name": row[1]}
        for row in rows
    ]


def delete_trip(conn, trip_id: int) -> None:
    conn.execute(
        "DELETE FROM trips WHERE id = ?;",
        (trip_id,),
    )
    conn.commit()