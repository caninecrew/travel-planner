from __future__ import annotations

import argparse
import sqlite3
import sys
from typing import Any

from travel_planner.domain.validators import ValidationError
from travel_planner.persistence.db import connect
from travel_planner.persistence.schema import init_schema

from travel_planner.cli.commands_trips import (
    cmd_trip_create,
    cmd_trip_delete,
    cmd_trip_list,
)
from travel_planner.cli.commands_days import (
    cmd_day_add,
    cmd_day_delete,
    cmd_day_list,
)
from travel_planner.cli.commands_items import (
    cmd_item_add_min,
    cmd_item_add_scheduled,
    cmd_item_delete,
    cmd_item_list,
)


DEFAULT_DB_PATH = "travel_planner.db"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="travel-planner")
    parser.add_argument(
        "--db",
        dest="db_path",
        default=DEFAULT_DB_PATH,
        help=f"Path to SQLite database file (default: {DEFAULT_DB_PATH})",
    )

    subparsers = parser.add_subparsers(dest="command_group", required=True)

    # ---- trip ----
    trip_p = subparsers.add_parser("trip", help="Trip commands")
    trip_sp = trip_p.add_subparsers(dest="command_action", required=True)

    trip_create = trip_sp.add_parser("create", help="Create a trip")
    trip_create.add_argument("--name", required=True)
    trip_create.set_defaults(command_group="trip", command_action="create")

    trip_list = trip_sp.add_parser("list", help="List trips")
    trip_list.set_defaults(command_group="trip", command_action="list")

    trip_delete = trip_sp.add_parser("delete", help="Delete a trip")
    trip_delete.add_argument("--trip-id", type=int, required=True)
    trip_delete.set_defaults(command_group="trip", command_action="delete")

    # ---- day ----
    day_p = subparsers.add_parser("day", help="Day commands")
    day_sp = day_p.add_subparsers(dest="command_action", required=True)

    day_add = day_sp.add_parser("add", help="Add a day to a trip")
    day_add.add_argument("--trip-id", type=int, required=True)
    day_add.add_argument("--date", required=True, help="YYYY-MM-DD")
    day_add.set_defaults(command_group="day", command_action="add")

    day_list = day_sp.add_parser("list", help="List days for a trip")
    day_list.add_argument("--trip-id", type=int, required=True)
    day_list.set_defaults(command_group="day", command_action="list")

    day_delete = day_sp.add_parser("delete", help="Delete a day")
    day_delete.add_argument("--day-id", type=int, required=True)
    day_delete.set_defaults(command_group="day", command_action="delete")

    # ---- item ----
    item_p = subparsers.add_parser("item", help="Item commands")
    item_sp = item_p.add_subparsers(dest="command_action", required=True)

    item_add = item_sp.add_parser("add", help="Add an item to a day")
    item_add.add_argument("--day-id", type=int, required=True)
    item_add.add_argument("--title", required=True)
    item_add.add_argument("--category", required=True)
    item_add.add_argument("--start", type=int, default=None, help="Minutes since midnight")
    item_add.add_argument("--end", type=int, default=None, help="Minutes since midnight")
    item_add.set_defaults(command_group="item", command_action="add")

    item_list = item_sp.add_parser("list", help="List items for a day")
    item_list.add_argument("--day-id", type=int, required=True)
    item_list.set_defaults(command_group="item", command_action="list")

    item_delete = item_sp.add_parser("delete", help="Delete an item")
    item_delete.add_argument("--item-id", type=int, required=True)
    item_delete.set_defaults(command_group="item", command_action="delete")

    return parser


def dispatch(conn: sqlite3.Connection, args: Any) -> int:
    group = getattr(args, "command_group", None)
    action = getattr(args, "command_action", None)

    if group == "trip":
        if action == "create":
            return cmd_trip_create(conn, args.name)
        if action == "list":
            return cmd_trip_list(conn)
        if action == "delete":
            return cmd_trip_delete(conn, args.trip_id)

    if group == "day":
        if action == "add":
            return cmd_day_add(conn, args.trip_id, args.date)
        if action == "list":
            return cmd_day_list(conn, args.trip_id)
        if action == "delete":
            return cmd_day_delete(conn, args.day_id)

    if group == "item":
        if action == "add":
            start = args.start
            end = args.end
            if start is None and end is None:
                return cmd_item_add_min(conn, args.day_id, args.title, args.category)
            return cmd_item_add_scheduled(
                conn,
                args.day_id,
                args.title,
                args.category,
                start,
                end,
                reject_overlaps=True,
            )
        if action == "list":
            return cmd_item_list(conn, args.day_id)
        if action == "delete":
            return cmd_item_delete(conn, args.item_id)

    print("Unknown command. Use -h for help.", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    conn: sqlite3.Connection | None = None
    try:
        conn = connect(args.db_path)
        init_schema(conn)
        return dispatch(conn, args)

    except ValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return 2

    except sqlite3.IntegrityError as e:
        print(f"Database constraint error: {e}", file=sys.stderr)
        return 3

    except sqlite3.OperationalError as e:
        print(f"Database operational error: {e}", file=sys.stderr)
        return 4

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    raise SystemExit(main())