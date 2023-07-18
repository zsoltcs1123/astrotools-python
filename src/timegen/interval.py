from datetime import datetime, timedelta
from skyfield.api import load
from typing import List


def calculate_intervals(start_time: datetime, end_time: datetime, interval_minutes: int) -> List[datetime]:
    intervals = []
    current_time = start_time

    while current_time < end_time:
        intervals.append(current_time)
        current_time += timedelta(minutes=interval_minutes)

    return intervals


def generate_skyfield_times(datetimes):
    ts = load.timescale()
    return [ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second) for dt in datetimes]
