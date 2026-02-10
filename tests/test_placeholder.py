import datetime as dt

import lab_manager.preliminary as pl


def test_placeholder2():
    assert pl.function_to_test(2) == 3


def test_initialise_schedule():
    assert pl.initialise_schedule(
        [["transfection"], ["media_change", "hard", 24], ["d3_harvest", "soft", 48]],
        dt.datetime.fromisoformat("2026-01-01"),
    ) == [
        ["transfection", dt.datetime(2026, 1, 1, 0, 0), "soft"],
        ["media_change", dt.datetime(2026, 1, 2, 0, 0), "hard"],
        ["d3_harvest", dt.datetime(2026, 1, 4, 0, 0), "soft"],
    ]


def test_alter_existing_schedule():
    assert pl.alter_existing_schedule(
        [
            ["transfection", dt.datetime(2026, 1, 1, 0, 0), "soft"],
            ["media_change", dt.datetime(2026, 1, 2, 0, 0), "hard"],
            ["d3_harvest", dt.datetime(2026, 1, 4, 0, 0), "soft"],
        ],
        1,
        dt.datetime(2026, 1, 3, 0, 0),
    ) == [
        ["transfection", dt.datetime(2026, 1, 1, 0, 0), "soft"],
        ["media_change", dt.datetime(2026, 1, 3, 0, 0), "hard"],
        ["d3_harvest", dt.datetime(2026, 1, 5, 0, 0), "soft"],
    ]


# This is a placeholder test file. Replace with actual tests.
