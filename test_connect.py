from travel_planner.persistence.db import connect

conn = connect("travel.db")
print("Connected successfully!")
conn.close()
