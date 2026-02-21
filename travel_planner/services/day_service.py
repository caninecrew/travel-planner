from __future__ import annotations

import sqlite3
from sqlite3 import Connection

from travel_planner.domain.validators import ValidationError, validate_date_string
from travel_planner.persistence import day_repository


def create_day(conn: Connection, trip_id: int, date_str: str) -> int:
    if not isinstance(trip_id, int) or trip_id <= 0:
        raise ValidationError("trip_id must be a positive integer.")

    validate_date_string(date_str)

    try:
        return int(day_repository.create_day(conn, trip_id, date_str))
    except sqlite3.IntegrityError as e:
        # If you add UNIQUE(trip_id, date) later, this becomes your friendly message.
        raise ValidationError("could not create day (possible duplicate date for this trip).") from e