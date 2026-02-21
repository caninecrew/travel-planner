import random
from datetime import datetime, timedelta, timezone

from travel_planner.persistence.db import connect
from travel_planner.persistence.schema import init_schema
from travel_planner.persistence.trip_repository import create_trip
from travel_planner.persistence.day_repository import create_day
from travel_planner.persistence.item_repository import create_item_scheduled


TRIP_NAMES = [
    "Italy Adventure",
    "Japan Explorer",
    "Iceland Roadtrip",
    "Pacific Northwest",
    "European Capitals",
    "Southwest USA Tour",
    "Canadian Rockies",
    "Mediterranean Escape",
]

ITEM_TITLES = [
    "Flight",
    "Train Ride",
    "Museum Visit",
    "City Walking Tour",
    "Dinner Reservation",
    "Hotel Check-in",
    "Coffee Break",
    "Boat Cruise",
    "Hiking Trail",
    "Market Visit",
]

CATEGORIES = ["activity", "transport", "food", "logistics"]


def bootstrap_random_db(db_path: str) -> None:
    conn = connect(db_path)
    init_schema(conn)

    trip_name = random.choice(TRIP_NAMES)
    trip_id = create_trip(conn, trip_name)

    num_days = random.randint(3, 7)

    start_date = datetime.now(timezone.utc).date() + timedelta(days=random.randint(1, 90))

    for i in range(num_days):
        current_date = (start_date + timedelta(days=i)).isoformat()
        day_id = create_day(conn, trip_id, current_date)

        # Random items per day (2–5)
        current_time = 9 * 60  # start at 9:00 AM

        for _ in range(random.randint(2, 5)):
            title = random.choice(ITEM_TITLES)
            category = random.choice(CATEGORIES)

            duration = random.randint(60, 180)  # 1–3 hours
            start_min = current_time
            end_min = start_min + duration

            create_item_scheduled(
                conn,
                day_id,
                title,
                category,
                start_min,
                end_min,
            )

            # move time forward with a buffer
            current_time = end_min + random.randint(30, 90)

    conn.close()


if __name__ == "__main__":
    bootstrap_random_db("sample.db")