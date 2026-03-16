import datetime as dt

import lab_manager.scheduler as sc

test_schedule2 = [
    {"task_name": "transfection"},
    {"task_name": "media_change", "category": "hard", "wait_time": 24},
    {"task_name": "d3_harvest", "category": "soft", "wait_time": 48},
    {"task_name": "EP1", "category": "soft", "wait_time": 0},
    {"task_name": "EP1_harvest", "category": "hard", "wait_time": 72},
    {"task_name": "EP2", "category": "soft", "wait_time": 0},
    {"task_name": "EP2_harvest", "category": "hard", "wait_time": 72},
]


def test_initialise_schedule():
    assert sc.initialise_schedule(
        [
            {"task_name": "transfection"},
            {"task_name": "media_change", "category": "hard", "wait_time": 24},
            {"task_name": "d3_harvest", "category": "hard", "wait_time": 48},
        ],
        dt.datetime.fromisoformat("2026-01-01"),
    ) == [
        {"task_name": "transfection", "task_date": dt.datetime(2026, 1, 1, 0, 0), "category": "soft"},
        {"task_name": "media_change", "task_date": dt.datetime(2026, 1, 2, 0, 0), "category": "hard"},
        {"task_name": "d3_harvest", "task_date": dt.datetime(2026, 1, 4, 0, 0), "category": "hard"},
    ]


def test_alter_existing_schedule():
    assert sc.alter_existing_schedule(
        [
            {"task_name": "transfection", "task_date": dt.datetime(2026, 1, 1, 0, 0), "category": "soft"},
            {"task_name": "media_change", "task_date": dt.datetime(2026, 1, 2, 0, 0), "category": "hard"},
            {"task_name": "d3_harvest", "task_date": dt.datetime(2026, 1, 4, 0, 0), "category": "soft"},
        ],
        1,
        "2026-01-03",
    ) == [
        {"task_name": "transfection", "task_date": dt.datetime(2026, 1, 1, 0, 0), "category": "soft"},
        {"task_name": "media_change", "task_date": dt.datetime(2026, 1, 3, 0, 0), "category": "hard"},
        {"task_name": "d3_harvest", "task_date": dt.datetime(2026, 1, 5, 0, 0), "category": "soft"},
    ]


def test_insert_into_schedule():
    assert sc.insert_into_schedule(
        [
            {"task_name": "transfection", "task_date": dt.datetime(2026, 1, 1, 0, 0), "category": "soft"},
            {"task_name": "media_change", "task_date": dt.datetime(2026, 1, 2, 0, 0), "category": "hard"},
            {"task_name": "d3_harvest", "task_date": dt.datetime(2026, 1, 4, 0, 0), "category": "soft"},
        ],
        3,
        {"task_name": "writeup", "task_date": dt.datetime(2026, 1, 5, 0, 0), "category": "soft"},
    ) == [
        {"task_name": "transfection", "task_date": dt.datetime(2026, 1, 1, 0, 0), "category": "soft"},
        {"task_name": "media_change", "task_date": dt.datetime(2026, 1, 2, 0, 0), "category": "hard"},
        {"task_name": "d3_harvest", "task_date": dt.datetime(2026, 1, 4, 0, 0), "category": "soft"},
        {"task_name": "writeup", "task_date": dt.datetime(2026, 1, 5, 0, 0), "category": "soft"},
    ]


def test_remove_from_schedule():
    assert sc.remove_from_schedule(
        [
            {"task_name": "transfection", "task_date": dt.datetime(2026, 1, 1, 0, 0), "category": "soft"},
            {"task_name": "media_change", "task_date": dt.datetime(2026, 1, 2, 0, 0), "category": "hard"},
            {"task_name": "d3_harvest", "task_date": dt.datetime(2026, 1, 4, 0, 0), "category": "soft"},
            {"task_name": "accidental_addition", "task_date": dt.datetime(2026, 1, 7, 0, 0), "category": "soft"},
        ],
        3,
    ) == [
        {"task_name": "transfection", "task_date": dt.datetime(2026, 1, 1, 0, 0), "category": "soft"},
        {"task_name": "media_change", "task_date": dt.datetime(2026, 1, 2, 0, 0), "category": "hard"},
        {"task_name": "d3_harvest", "task_date": dt.datetime(2026, 1, 4, 0, 0), "category": "soft"},
    ]
