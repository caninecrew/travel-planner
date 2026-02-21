from __future__ import annotations

from sqlite3 import Connection

from travel_planner.domain.validators import ValidationError
from travel_planner.cli.formatters import fmt_minutes, fmt_money, print_table
from travel_planner.services import item_service


# Prefer service layer when present
try:
    from travel_planner.services.item_service import (
        create_item_min as svc_create_item_min,
        create_item_scheduled as svc_create_item_scheduled,
        check_overlaps_for_day as svc_check_overlaps_for_day,
        check_tight_connections_for_day as svc_check_tight_connections_for_day,
    )
except Exception:  # pragma: no cover
    svc_create_item_min = None
    svc_create_item_scheduled = None
    svc_check_overlaps_for_day = None
    svc_check_tight_connections_for_day = None

from travel_planner.persistence.item_repository import (
    create_item_min as repo_create_item_min,
    create_item_scheduled as repo_create_item_scheduled,
    delete_item,
    get_item,
    list_items_for_day,
)


def cmd_item_add_min(conn: Connection, day_id: int, title: str, category: str) -> int:
    """
    Add an unscheduled (minimal) item to a day.
    """
    if not isinstance(day_id, int) or day_id <= 0:
        raise ValidationError("day_id must be a positive integer.")

    if svc_create_item_min is not None:
        item_id = int(svc_create_item_min(conn, day_id, title, category))
    else:
        # Fallback validation
        if not isinstance(title, str):
            raise ValidationError("title must be a string.")
        if not isinstance(category, str):
            raise ValidationError("category must be a string.")
        t = title.strip()
        c = category.strip()
        if not t:
            raise ValidationError("title must not be blank.")
        if not c:
            raise ValidationError("category must not be blank.")

        item_id = int(repo_create_item_min(conn, day_id, t, c))

    print(f"Created item id={item_id} (unscheduled) for day id={day_id}")
    return 0


def cmd_item_add_scheduled(
    conn: Connection,
    day_id: int,
    title: str,
    category: str,
    start_min: int,
    end_min: int,
    *,
    reject_overlaps: bool = True,
) -> int:
    """
    Add a scheduled item to a day.
    """
    if not isinstance(day_id, int) or day_id <= 0:
        raise ValidationError("day_id must be a positive integer.")

    if start_min is None or end_min is None:
        raise ValidationError("scheduled items require both start_min and end_min.")

    if svc_create_item_scheduled is not None:
        item_id = int(
            svc_create_item_scheduled(
                conn,
                day_id,
                title,
                category,
                start_min,
                end_min,
                reject_overlaps=reject_overlaps,
            )
        )
    else:
        # Fallback validation
        from travel_planner.domain.validators import validate_time_range

        if not isinstance(title, str):
            raise ValidationError("title must be a string.")
        if not isinstance(category, str):
            raise ValidationError("category must be a string.")
        t = title.strip()
        c = category.strip()
        if not t:
            raise ValidationError("title must not be blank.")
        if not c:
            raise ValidationError("category must not be blank.")

        validate_time_range(start_min, end_min)

        if reject_overlaps:
            existing = [
                it
                for it in list_items_for_day(conn, day_id)
                if it.get("start_min") is not None and it.get("end_min") is not None
            ]
            for it in existing:
                a_start, a_end = start_min, end_min
                b_start, b_end = it["start_min"], it["end_min"]
                # overlap if [a_start,a_end) intersects [b_start,b_end)
                if a_start < b_end and b_start < a_end:
                    raise ValidationError(
                        f"scheduled item overlaps existing item id={it['id']} "
                        f"({it['start_min']}–{it['end_min']})."
                    )

        item_id = int(repo_create_item_scheduled(conn, day_id, t, c, start_min, end_min))

    print(
        f"Created item id={item_id} ({fmt_minutes(start_min)}–{fmt_minutes(end_min)}) for day id={day_id}"
    )
    return 0


def cmd_item_list(conn: Connection, day_id: int) -> int:
    """
    List items for a day (summary).
    """
    if not isinstance(day_id, int) or day_id <= 0:
        raise ValidationError("day_id must be a positive integer.")

    items = list_items_for_day(conn, day_id)
    if not items:
        print("No items found for this day.")
        return 0

    headers = ["ID", "Time", "Title", "Category", "Pinned", "Est", "Actual", "Tags"]
    rows: list[list[str]] = []

    for it in items:
        time_str = "ALL DAY" if it.get("is_all_day") else f"{fmt_minutes(it.get('start_min'))}–{fmt_minutes(it.get('end_min'))}"
        pinned_str = "Y" if it.get("pinned") else ""
        est = fmt_money(it.get("estimated_cost"), it.get("currency"))
        actual = fmt_money(it.get("actual_cost"), it.get("currency"))
        tags = it.get("tags") or ""

        rows.append(
            [
                str(it["id"]),
                time_str,
                str(it.get("title") or ""),
                str(it.get("category") or ""),
                pinned_str,
                est,
                actual,
                str(tags),
            ]
        )

    print_table(headers, rows)
    return 0


def cmd_item_get(conn: Connection, item_id: int) -> int:
    """
    Show full details for a single item.
    """
    if not isinstance(item_id, int) or item_id <= 0:
        raise ValidationError("item_id must be a positive integer.")

    item = get_item(conn, item_id)
    if item is None:
        print("Item not found.")
        return 0

    # Simple key/value print (formatter can be upgraded later)
    print(f"Item {item['id']}")
    for k in sorted(item.keys()):
        print(f"  {k}: {item[k]}")
    return 0


def cmd_item_delete(conn: Connection, item_id: int) -> int:
    """
    Delete an item by id.
    """
    if not isinstance(item_id, int) or item_id <= 0:
        raise ValidationError("item_id must be a positive integer.")

    delete_item(conn, item_id)
    print(f"Deleted item id={item_id}")
    return 0


def cmd_item_check(conn: Connection, day_id: int, buffer_min: int = 15) -> int:
    """
    Run scheduling diagnostics for a day.
    """
    if not isinstance(day_id, int) or day_id <= 0:
        raise ValidationError("day_id must be a positive integer.")
    if not isinstance(buffer_min, int) or buffer_min < 0:
        raise ValidationError("buffer_min must be an integer >= 0.")

    if svc_check_overlaps_for_day is None or svc_check_tight_connections_for_day is None:
        print("Item checks are not available (missing item_service).")
        return 1

    overlaps = svc_check_overlaps_for_day(conn, day_id)
    tight = svc_check_tight_connections_for_day(conn, day_id, buffer_min=buffer_min)

    if not overlaps and not tight:
        print("No scheduling issues found.")
        return 0

    if overlaps:
        print("Overlaps:")
        headers = ["Item A", "Item B", "Overlap (min)"]
        rows = [[str(o["item_a_id"]), str(o["item_b_id"]), str(o["overlap_min"])] for o in overlaps]
        print_table(headers, rows)

    if tight:
        print(f"Tight connections (gap < {buffer_min} min):")
        headers = ["Prev Item", "Next Item", "Gap (min)"]
        rows = [[str(t["prev_item_id"]), str(t["next_item_id"]), str(t["gap_min"])] for t in tight]
        print_table(headers, rows)

    return 0


def cmd_item_update(
    conn,
    item_id: int,
    *,
    title: str | None,
    category: str | None,
    notes: str | None,
    tags: str | None,
    pinned: int | None,
    start: int | None,
    end: int | None,
    clear_time: bool,
    allow_overlap: bool,
) -> int:

    if clear_time and (start is not None or end is not None):
        raise ValueError("Cannot use --clear-time with --start/--end.")

    if start is not None or end is not None:
        if start is None or end is None:
            raise ValueError("--start and --end must both be provided.")

        item_service.set_item_time(
            conn,
            item_id,
            start,
            end,
            reject_overlaps=not allow_overlap,
        )

    elif clear_time:
        item_service.clear_item_time(conn, item_id)

    if any(v is not None for v in [title, category, notes, tags, pinned]):
        item_service.update_item_fields(
            conn,
            item_id,
            title=title,
            category=category,
            notes=notes,
            tags=tags,
            pinned=(bool(pinned) if pinned is not None else None),
        )

    print(f"Updated item id={item_id}")
    return 0