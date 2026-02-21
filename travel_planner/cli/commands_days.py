from __future__ import annotations

from sqlite3 import Connection

from travel_planner.domain.validators import ValidationError
from travel_planner.cli.formatters import print_table
from travel_planner.services import day_service


# Prefer service layer when present
try:
    from travel_planner.services.day_service import create_day as svc_create_day
except Exception:  # pragma: no cover
    svc_create_day = None

from travel_planner.persistence.day_repository import (
    list_days_for_trip,
    delete_day,
)


def cmd_day_add(conn: Connection, trip_id: int, date_str: str) -> int:
    """
    Add a day to a trip.
    """
    if not isinstance(trip_id, int) or trip_id <= 0:
        raise ValidationError("trip_id must be a positive integer.")

    if svc_create_day is not None:
        day_id = int(svc_create_day(conn, trip_id, date_str))
    else:
        # Fallback validation (minimal)
        from travel_planner.domain.validators import validate_date_string
        from travel_planner.persistence.day_repository import create_day as repo_create_day

        validate_date_string(date_str)
        day_id = int(repo_create_day(conn, trip_id, date_str))

    print(f"Created day id={day_id} for trip id={trip_id}")
    return 0


def cmd_day_list(conn: Connection, trip_id: int) -> int:
    """
    List days for a trip.
    """
    if not isinstance(trip_id, int) or trip_id <= 0:
        raise ValidationError("trip_id must be a positive integer.")

    days = list_days_for_trip(conn, trip_id)

    if not days:
        print("No days found for this trip.")
        return 0

    headers = ["Day ID", "Trip ID", "Date"]
    rows = [
        [str(d["id"]), str(d["trip_id"]), str(d["date"])]
        for d in days
    ]

    print_table(headers, rows)
    return 0


def cmd_day_delete(conn: Connection, day_id: int) -> int:
    """
    Delete a day by id.
    """
    if not isinstance(day_id, int) or day_id <= 0:
        raise ValidationError("day_id must be a positive integer.")

    delete_day(conn, day_id)
    print(f"Deleted day id={day_id}")
    return 0

def cmd_day_set_date(conn, day_id: int, date_str: str) -> int:
    day_service.set_day_date(conn, day_id, date_str)
    print(f"Updated day id={day_id}")
    return 0