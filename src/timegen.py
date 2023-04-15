from datetime import datetime, timedelta
from skyfield.api import load


def generate_datetimes(start_datetime, end_datetime, interval_minutes=60, num_intervals=24):
    interval_seconds = interval_minutes * 60
    return [start_datetime +
            datetime.timedelta(seconds=interval_seconds*i) for i in range(num_intervals)]


def calculate_intervals(start_time, end_time, interval_minutes):
    intervals = []
    current_time = start_time

    while current_time < end_time:
        intervals.append(current_time)
        current_time += timedelta(minutes=interval_minutes)

    return intervals


def generate_skyfield_times(datetimes):
    ts = load.timescale()
    return [ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second) for dt in datetimes]
