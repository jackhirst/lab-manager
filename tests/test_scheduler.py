import datetime as dt

from lab_manager.scheduler import Schedule


def test_test():
    assert True


def test_initialise_schedule():
    sched = Schedule("test")

    sched.initialise_schedule(
        [
            {"task_name": "transfection"},
            {"task_name": "media_change", "category": "hard", "wait_time": 24},
            {"task_name": "d3_harvest", "category": "hard", "wait_time": 48},
        ],
        dt.datetime.fromisoformat("2026-01-01"),
    )

    assert sched.schedule == [
        {"task_name": "transfection", "task_date": dt.datetime(2026, 1, 1, 0, 0), "category": "soft"},
        {"task_name": "media_change", "task_date": dt.datetime(2026, 1, 2, 0, 0), "category": "hard"},
        {"task_name": "d3_harvest", "task_date": dt.datetime(2026, 1, 4, 0, 0), "category": "hard"},
    ]


def test_alter_schedule():
    sched = Schedule("test")

    sched.schedule = [
        {"task_name": "transfection", "task_date": dt.datetime(2026, 1, 1, 0, 0), "category": "soft"},
        {"task_name": "media_change", "task_date": dt.datetime(2026, 1, 2, 0, 0), "category": "hard"},
        {"task_name": "d3_harvest", "task_date": dt.datetime(2026, 1, 4, 0, 0), "category": "soft"},
    ]

    sched.alter_schedule(1, "2026-01-03")

    assert sched.schedule == [
        {"task_name": "transfection", "task_date": dt.datetime(2026, 1, 1, 0, 0), "category": "soft"},
        {"task_name": "media_change", "task_date": dt.datetime(2026, 1, 3, 0, 0), "category": "hard"},
        {"task_name": "d3_harvest", "task_date": dt.datetime(2026, 1, 5, 0, 0), "category": "soft"},
    ]
