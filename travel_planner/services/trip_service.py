from __future__ import annotations

from sqlite3 import Connection

from travel_planner.domain.validators import ValidationError
from travel_planner.persistence import trip_repository


def create_trip(conn: Connection, name: str) -> int:
    if not isinstance(name, str):
        raise ValidationError("trip name must be a string.")
    cleaned = name.strip()
    if not cleaned:
        raise ValidationError("trip name must not be blank.")

    return int(trip_repository.create_trip(conn, cleaned))

def rename_trip(conn, trip_id: int, name: str) -> None:
    if trip_id <= 0:
        raise ValidationError("trip_id must be positive.")

    name = name.strip()
    if not name:
        raise ValidationError("trip name must not be blank.")

    trip = trip_repository.get_trip(conn, trip_id)
    if trip is None:
        raise ValidationError("trip not found.")

    trip_repository.rename_trip(conn, trip_id, name)