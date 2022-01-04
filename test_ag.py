import datetime
from zoneinfo import ZoneInfo

import pytest
import time_machine

from at import gen_row, get_tz_offset

berlin_tz = ZoneInfo("Europe/Berlin")


@time_machine.travel(datetime.datetime(2021, 9, 18, 13, 37, tzinfo=berlin_tz))
@pytest.mark.parametrize(
    "date,time,expected",
    (
        (
            None,
            None,
            {
                "date": "2021-09-18",
                "date_rolling": "2021-09-18",
                "dayname": "Sat",
                "time": "13:37",
                "tz": "+0200",
            },
        ),
        (
            datetime.date(2021, 9, 17),
            None,
            {
                "date": "2021-09-17",
                "date_rolling": "2021-09-17",
                "dayname": "Fri",
                "time": "13:37",
                "tz": "+0200",
            },
        ),
        (
            datetime.date(2021, 9, 18),
            datetime.datetime.now().replace(hour=1, minute=2),
            {
                "date": "2021-09-18",
                "date_rolling": "2021-09-17",
                "dayname": "Sat",
                "time": "01:02",
                "tz": "+0200",
            },
        ),
        # winter example
        (
            datetime.date(2020, 12, 25),
            datetime.datetime.now().replace(hour=17, minute=11),
            {
                "date": "2020-12-25",
                "date_rolling": "2020-12-25",
                "dayname": "Fri",
                "time": "17:11",
                "tz": "+0100",
            },
        ),
    ),
)
def test_gen_row(date, time, expected):
    assert gen_row(date, time) == expected


@time_machine.travel(datetime.datetime(2021, 1, 1, 13, 37, tzinfo=berlin_tz))
def test_get_tz_offset_winter():
    dt = datetime.datetime.now()
    assert get_tz_offset(dt) == "+0100"


@time_machine.travel(datetime.datetime(2021, 9, 18, 13, 37, tzinfo=berlin_tz))
def test_get_tz_offset_summer():
    dt = datetime.datetime.now()
    assert get_tz_offset(dt) == "+0200"
