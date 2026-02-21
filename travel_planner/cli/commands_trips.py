from __future__ import annotations

from sqlite3 import Connection

from travel_planner.domain.validators import ValidationError
from travel_planner.cli.formatters import print_table

# Prefer service layer when present
try:
    from travel_planner.services.trip_service import create_trip as svc_create_trip
except Exception:  # pragma: no cover
    svc_create_trip = None

from travel_planner.persistence.trip_repository import delete_trip, list_trips


def cmd_trip_create(conn: Connection, name: str) -> int:
    """
    Create a trip and print the new trip id.
    """
    if svc_create_trip is not None:
        trip_id = int(svc_create_trip(conn, name))
    else:
        # Fallback (not ideal long-term): validate minimally here
        if not isinstance(name, str):
            raise ValidationError("trip name must be a string.")
        cleaned = name.strip()
        if not cleaned:
            raise ValidationError("trip name must not be blank.")

        from travel_planner.persistence.trip_repository import create_trip as repo_create_trip
        trip_id = int(repo_create_trip(conn, cleaned))

    print(f"Created trip id={trip_id}")
    return 0


def cmd_trip_list(conn: Connection) -> int:
    """
    List all trips.
    """
    trips = list_trips(conn)
    if not trips:
        print("No trips found.")
        return 0

    headers = ["ID", "Name"]
    rows = [[str(t["id"]), str(t["name"])] for t in trips]
    print_table(headers, rows)
    return 0


def cmd_trip_delete(conn: Connection, trip_id: int) -> int:
    """
    Delete a trip by id.
    """
    if not isinstance(trip_id, int) or trip_id <= 0:
        raise ValidationError("trip_id must be a positive integer.")

    delete_trip(conn, trip_id)
    print(f"Deleted trip id={trip_id}")
    return 0