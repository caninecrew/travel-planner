from travel_planner.persistence.db import connect
from travel_planner.persistence.schema import init_schema

conn = connect("travel.db")
init_schema(conn)

conn.execute("INSERT INTO days (id, trip_id, date) VALUES (?, ?, ?);", ("day_1", "trip_1", "2026-05-23"))
conn.execute("INSERT INTO items (id, day_id, title, category, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?);", ("item_1", "day_1", "CN Tower", "activity", "2026-01-01T12:00:00", "2026-01-01T12:00:00"))
conn.commit()
conn.close()
