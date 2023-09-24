from datetime import datetime
from typing import List
from zodiac.mapped_position import map_divisions
from zodiac.event import DecanChange, MappedPosition, get_decan_changes
from timegen.interval import calculate_intervals

def get_positions_for_planet_in_time_range(planet: str, start_time: datetime, end_time: datetime) -> List[MappedPosition]:
    return [map_divisions(planet, date) for date in calculate_intervals(start_time, end_time, 240)]

def get_planet_decan_changes(planet: str, start_time: datetime, end_time: datetime) -> List[DecanChange]:
    return get_decan_changes(get_positions_for_planet_in_time_range(planet, start_time, end_time))


start_time = datetime(2023, 1, 1)
end_time = datetime(2023, 12, 31)
planet = 'Mars'
decan_changes = get_planet_decan_changes(planet, start_time, end_time)

counter = 0
for event in decan_changes:
    counter += 1
    print(f"Event {counter}: {event}")
