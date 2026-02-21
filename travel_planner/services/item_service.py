from __future__ import annotations

from sqlite3 import Connection

from travel_planner.domain.validators import ValidationError, validate_time_range
from travel_planner.persistence import item_repository


def _validate_basic_item_fields(title: str, category: str) -> tuple[str, str]:
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

    return t, c


def _ranges_overlap(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    # Standard half-open interval overlap check: [start, end)
    return a_start < b_end and b_start < a_end


def _list_scheduled_items_for_day(conn: Connection, day_id: int) -> list[dict]:
    items = item_repository.list_items_for_day(conn, day_id)
    return [
        it for it in items
        if it.get("start_min") is not None and it.get("end_min") is not None
    ]


def check_overlaps_for_day(conn: Connection, day_id: int) -> list[dict]:
    scheduled = _list_scheduled_items_for_day(conn, day_id)
    overlaps: list[dict] = []

    # O(n^2) is fine for MVP day sizes; can optimize later with ordering/scan.
    for i in range(len(scheduled)):
        a = scheduled[i]
        for j in range(i + 1, len(scheduled)):
            b = scheduled[j]
            if _ranges_overlap(a["start_min"], a["end_min"], b["start_min"], b["end_min"]):
                overlap_start = max(a["start_min"], b["start_min"])
                overlap_end = min(a["end_min"], b["end_min"])
                overlaps.append(
                    {
                        "item_a_id": a["id"],
                        "item_b_id": b["id"],
                        "overlap_min": max(0, overlap_end - overlap_start),
                    }
                )

    return overlaps


def create_item_min(conn: Connection, day_id: int, title: str, category: str) -> int:
    if not isinstance(day_id, int) or day_id <= 0:
        raise ValidationError("day_id must be a positive integer.")

    t, c = _validate_basic_item_fields(title, category)
    return int(item_repository.create_item_min(conn, day_id, t, c))


def create_item_scheduled(
    conn: Connection,
    day_id: int,
    title: str,
    category: str,
    start_min: int,
    end_min: int,
    *,
    reject_overlaps: bool = True,
) -> int:
    if not isinstance(day_id, int) or day_id <= 0:
        raise ValidationError("day_id must be a positive integer.")

    t, c = _validate_basic_item_fields(title, category)
    validate_time_range(start_min, end_min)

    if reject_overlaps:
        existing = _list_scheduled_items_for_day(conn, day_id)
        for it in existing:
            if _ranges_overlap(start_min, end_min, it["start_min"], it["end_min"]):
                raise ValidationError(
                    f"scheduled item overlaps existing item id={it['id']} "
                    f"({it['start_min']}–{it['end_min']})."
                )

    return int(item_repository.create_item_scheduled(conn, day_id, t, c, start_min, end_min))


def check_tight_connections_for_day(
    conn: Connection,
    day_id: int,
    buffer_min: int = 15,
) -> list[dict]:
    if not isinstance(buffer_min, int) or buffer_min < 0:
        raise ValidationError("buffer_min must be an integer >= 0.")

    scheduled = sorted(
        _list_scheduled_items_for_day(conn, day_id),
        key=lambda it: (it["start_min"], it["end_min"], it["id"]),
    )

    warnings: list[dict] = []
    for prev, nxt in zip(scheduled, scheduled[1:]):
        gap = nxt["start_min"] - prev["end_min"]
        if gap < buffer_min:
            warnings.append(
                {
                    "prev_item_id": prev["id"],
                    "next_item_id": nxt["id"],
                    "gap_min": gap,
                    "buffer_min": buffer_min,
                }
            )

    return warnings