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
            UNIQUE (trip_id, date),
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

            is_all_day INTEGER NOT NULL DEFAULT 0 CHECK (is_all_day IN (0,1)),
            timezone TEXT,
            duration_min INTEGER,
            position INTEGER,
            pinned INTEGER NOT NULL DEFAULT 0 CHECK (pinned IN (0,1)),

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

            FOREIGN KEY (day_id) REFERENCES days(id) ON DELETE CASCADE,

            CHECK (
                (start_min IS NULL AND end_min IS NULL)
                OR
                (
                    start_min IS NOT NULL
                    AND end_min IS NOT NULL
                    AND start_min >= 0
                    AND end_min <= 1440
                    AND start_min < end_min
                )
            )
        );
        """,
        # ---- INDEXES ----
        """
        CREATE INDEX IF NOT EXISTS idx_days_trip_date
        ON days (trip_id, date);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_items_day
        ON items (day_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_items_day_time
        ON items (day_id, start_min, end_min);
        """,
    ]


def init_schema(conn: Connection) -> None:
    for ddl in get_schema_ddl():
        conn.execute(ddl)
    conn.commit()