'''
Purpose: Responsible for opening a connection to the SQLite databse
'''

import sqlite3

def connect(db_path: str) -> sqlite3.Connection:
    """
    Open to a connection to the SQLite database and enable foreign key enforcement.
    """

    conn = sqlite3.connect(db_path)

    # Enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn