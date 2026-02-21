from sqlite3 import Connection

def get_schema_ddl() -> list[str]:
    return [
    """
    CREATE TABLE IF NOT EXISTS trips (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS days (
        id INTEGER PRIMARY KEY,
        trip_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        day_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT,
        status TEXT,
        start_min INTEGER,
        end_min INTEGER,
        is_all_day INTEGER NOT NULL DEFAULT 0,
        timezone TEXT,
        duration_min INTEGER,
        position INTEGER,
        pinned INTEGER NOT NULL DEFAULT 0,
        location_name TEXT,
        location_address TEXT,
        lat REAL,
        lon REAL,
        estimated_cost REAL,
        actual_cost REAL,
        currency TEXT,
        cost_notes TEXT,
        tags TEXT,
        notes TEXT,
        url TEXT,
        confirmation_code TEXT,
        provider TEXT,
        extra_json TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (day_id) REFERENCES days(id) ON DELETE CASCADE
    );
    """
    ]

def init_schema(conn):
    for ddl in get_schema_ddl():
        conn.execute(ddl)
    conn.commit()