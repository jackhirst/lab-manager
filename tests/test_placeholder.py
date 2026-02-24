import datetime as dt

import lab_manager.preliminary as pl
import lab_manager.scheduler as sc

# def test_initialise_schedule():
#     assert pl.initialise_schedule(
#         [["transfection"], ["media_change", "hard", 24], ["d3_harvest", "soft", 48]],
#         dt.datetime.fromisoformat("2026-01-01"),
#     ) == [
#         ["transfection", dt.datetime(2026, 1, 1, 0, 0), "soft"],
#         ["media_change", dt.datetime(2026, 1, 2, 0, 0), "hard"],
#         ["d3_harvest", dt.datetime(2026, 1, 4, 0, 0), "soft"],
#     ]


# def test_alter_existing_schedule():
#     assert pl.alter_existing_schedule(
#         [
#             ["transfection", dt.datetime(2026, 1, 1, 0, 0), "soft"],
#             ["media_change", dt.datetime(2026, 1, 2, 0, 0), "hard"],
#             ["d3_harvest", dt.datetime(2026, 1, 4, 0, 0), "soft"],
#         ],
#         1,
#         dt.datetime(2026, 1, 3, 0, 0),
#     ) == [
#         ["transfection", dt.datetime(2026, 1, 1, 0, 0), "soft"],
#         ["media_change", dt.datetime(2026, 1, 3, 0, 0), "hard"],
#         ["d3_harvest", dt.datetime(2026, 1, 5, 0, 0), "soft"],
#     ]

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