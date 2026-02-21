import pytest

from travel_planner.domain.validators import (
    ValidationError,
    validate_cost,
    validate_date_string,
    validate_time_range,
)

def test_validate_time_range_allows_both_none():
    validate_time_range(None, None)


def test_validate_time_range_rejects_only_one_side_set():
    with pytest.raises(ValidationError):
        validate_time_range(60, None)
    with pytest.raises(ValidationError):
        validate_time_range(None, 120)


def test_validate_time_range_rejects_non_ints():
    with pytest.raises(ValidationError):
        validate_time_range(60.5, 120)  # type: ignore[arg-type]
    with pytest.raises(ValidationError):
        validate_time_range(60, "120")  # type: ignore[arg-type]


def test_validate_time_range_rejects_out_of_bounds():
    with pytest.raises(ValidationError):
        validate_time_range(-1, 10)
    with pytest.raises(ValidationError):
        validate_time_range(0, 1441)
    with pytest.raises(ValidationError):
        validate_time_range(1440, 1440)  # also fails start < end


def test_validate_time_range_rejects_start_not_less_than_end():
    with pytest.raises(ValidationError):
        validate_time_range(600, 600)
    with pytest.raises(ValidationError):
        validate_time_range(700, 650)


def test_validate_time_range_accepts_valid_range():
    validate_time_range(0, 1)
    validate_time_range(540, 600)
    validate_time_range(1439, 1440)


def test_validate_cost_allows_none():
    validate_cost(None)


def test_validate_cost_accepts_zero_and_positive():
    validate_cost(0)
    validate_cost(12.34)
    validate_cost(500)


def test_validate_cost_rejects_non_numeric():
    with pytest.raises(ValidationError):
        validate_cost("12.34")  # type: ignore[arg-type]


def test_validate_cost_rejects_negative():
    with pytest.raises(ValidationError):
        validate_cost(-0.01)


def test_validate_cost_rejects_unreasonably_large_default():
    with pytest.raises(ValidationError):
        validate_cost(1_000_000.01)


def test_validate_cost_allows_large_when_threshold_raised():
    validate_cost(5_000_000.0, max_reasonable=10_000_000.0)


def test_validate_date_string_accepts_valid_dates():
    validate_date_string("2026-05-23")
    validate_date_string("2000-02-29")


def test_validate_date_string_rejects_non_string():
    with pytest.raises(ValidationError):
        validate_date_string(20260523)  # type: ignore[arg-type]


def test_validate_date_string_rejects_wrong_format():
    for bad in ["2026/05/23", "05-23-2026", "2026-5-23", "2026-05-2", "abc"]:
        with pytest.raises(ValidationError):
            validate_date_string(bad)


def test_validate_date_string_rejects_invalid_calendar_dates():
    for bad in ["2026-02-29", "2026-13-01", "2026-00-10", "2026-04-31", "2026-01-00"]:
        with pytest.raises(ValidationError):
            validate_date_string(bad)