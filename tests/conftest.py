from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from pydantic.dataclasses import dataclass  # Type Enforcement
import pytest


class SuccessStatus(Enum):
    SUCCESS = 1
    INCOMPLETE = 2
    MISSES = 3  # or wrong order
    NOT_STARTED = 4


@dataclass(frozen=True)
class MockCourse:
    course_name: str
    is_score_o: bool
    stations: list[int]


@dataclass(frozen=True)
class MockInputData:
    card_id: int
    start_time: dt.datetime
    finish_time: dt.datetime
    punches: list[tuple[int, dt.datetime]]
    reading_id: str


@dataclass(frozen=True)
class MockOutputData:
    course_name: str
    success_status: SuccessStatus
    missed_checkpoints: list[int]


@pytest.fixture
def example_course() -> MockCourse:
    return MockCourse(
        course_name="tutorial-O",
        is_score_o=False,
        stations=[42, 43, 49],
    )


@pytest.fixture
def example_input_success(example_course: MockCourse) -> MockInputData:
    start = dt.datetime(2025, 3, 14, 9, 30, 17)
    finish = dt.datetime(2025, 3, 14, 10, 22, 47)
    punches = [
        (42, dt.datetime(2025, 3, 14, 9, 37, 2)),
        (43, dt.datetime(2025, 3, 14, 9, 57, 8)),
        (49, dt.datetime(2025, 3, 14, 10, 9, 44)),
    ]
    return MockInputData(
        card_id=123,
        start_time=start,
        finish_time=finish,
        punches=punches,
        reading_id="202503140930170000000123",
    )


@pytest.fixture
def example_output_success(example_course: MockCourse) -> MockOutputData:
    return MockOutputData(
        course_name=example_course.course_name,
        success_status=SuccessStatus.SUCCESS,
        missed_checkpoints=[],
    )


@pytest.fixture
def example_input_incomplete(example_course: MockCourse) -> MockInputData:
    start = dt.datetime(2025, 3, 14, 9, 30, 17)
    finish = dt.datetime.min  # finish time precedes start time
    punches = [
        (42, dt.datetime(2025, 3, 14, 9, 37, 2)),
        (43, dt.datetime(2025, 3, 14, 9, 57, 8)),
        (49, dt.datetime(2025, 3, 14, 10, 9, 44)),
    ]
    return MockInputData(
        card_id=123,
        start_time=start,
        finish_time=finish,
        punches=punches,
        reading_id="202503140930170000000123",
    )


@pytest.fixture
def example_output_incomplete(example_course: MockCourse) -> MockOutputData:
    return MockOutputData(
        course_name=example_course.course_name,
        success_status=SuccessStatus.INCOMPLETE,
        missed_checkpoints=[],
    )


@pytest.fixture
def example_input_misses(example_course: MockCourse) -> MockInputData:
    start = dt.datetime(2025, 3, 14, 9, 30, 17)
    finish = dt.datetime(2025, 3, 14, 10, 22, 47)
    punches = [
        (43, dt.datetime(2025, 3, 14, 9, 57, 8)),
        (42, dt.datetime(2025, 3, 14, 9, 37, 2)),  # out of order
    ]
    return MockInputData(
        card_id=123,
        start_time=start,
        finish_time=finish,
        punches=punches,
        reading_id="202503140930170000000123",
    )


@pytest.fixture
def example_output_misses(example_course: MockCourse) -> MockOutputData:
    return MockOutputData(
        course_name=example_course.course_name,
        success_status=SuccessStatus.MISSES,
        missed_checkpoints=[42, 49],
    )


@pytest.fixture
def example_input_wrong_order(example_course: MockCourse) -> MockInputData:
    start = dt.datetime(2025, 3, 14, 9, 30, 17)
    finish = dt.datetime(2025, 3, 14, 10, 22, 47)
    punches = [
        (49, dt.datetime(2025, 3, 14, 10, 9, 44)),
        (42, dt.datetime(2025, 3, 14, 9, 37, 2)),
        (43, dt.datetime(2025, 3, 14, 9, 57, 8)),
    ]
    return MockInputData(
        card_id=123,
        start_time=start,
        finish_time=finish,
        punches=punches,
        reading_id="202503140930170000000123",
    )


@pytest.fixture
def example_output_wrong_order(example_course: MockCourse) -> MockOutputData:
    return MockOutputData(
        course_name=example_course.course_name,
        success_status=SuccessStatus.MISSES,
        missed_checkpoints=[49],
    )


@pytest.fixture
def example_input_not_started(example_course: MockCourse) -> MockInputData:
    start = dt.datetime.max  # after the finish time
    finish = dt.datetime(2025, 3, 14, 10, 22, 47)
    punches = [
        (42, dt.datetime(2025, 3, 14, 9, 37, 2)),
        (43, dt.datetime(2025, 3, 14, 9, 57, 8)),
        (49, dt.datetime(2025, 3, 14, 10, 9, 44)),
    ]
    return MockInputData(
        card_id=123,
        start_time=start,
        finish_time=finish,
        punches=punches,
        reading_id="202503140930170000000123",
    )


@pytest.fixture
def example_output_not_started(example_course: MockCourse) -> MockOutputData:
    return MockOutputData(
        course_name=example_course.course_name,
        success_status=SuccessStatus.NOT_STARTED,
        missed_checkpoints=[],
    )
