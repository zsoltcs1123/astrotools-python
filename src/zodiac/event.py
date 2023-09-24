
from dataclasses import dataclass
from datetime import datetime
from typing import List
from core.util import ends_with, find_smallest_elements, group_by

from zodiac.mapped_position import MappedPosition


@dataclass
class Event:
    position: MappedPosition

    def tv_timestamp(self) -> str:
        """timestamp("2023-02-27 11:05:00")"""
        return f'timestamp(\"{self.position.time.strftime("%Y-%m-%d %H:%M:%S")}\")'


@dataclass
class DecanChange(Event):
    previous: MappedPosition

    def __repr__(self) -> str:
        return f'{self.position.planet} Decan change at {self.position.time}: {self.previous.decan} -> {self.previous.decan}'

    def __str__(self) -> str:
        return f'Decan change at {self.position.time.strftime("%Y-%m-%d %H:%M:%S")}: {self.previous.decan.name} -> {self.position.decan.name}'

@dataclass
class TermChange(Event):
    previous: MappedPosition

    def __repr__(self) -> str:
        f'{self.position.planet} Term change at {self.position.time}: {self.previous.term} -> {self.previous.term}'


@dataclass
class Progression(Event):
    name: str


def get_decan_changes(positions: List[MappedPosition]) -> List[Event]:
    return [DecanChange(pos, prev_pos) for prev_pos, pos in zip(positions, positions[1:]) if pos.decan.id != prev_pos.decan.id]


def get_term_changes(positions: List[MappedPosition]) -> List[Event]:
    return [TermChange(pos, prev_pos) for prev_pos, pos in zip(positions, positions[1:]) if pos.term.id != prev_pos.term.id]


def get_progressions(positions: List[MappedPosition]) -> List[Event]:
    events = []
    for pos in positions:
        if (ends_with(5, pos.lon)):
            events.append(Progression(pos, "50%"))
        # elif (ends_with(7, pos.lon)):
            # events.append(Progression(pos, "70%"))

    groups = group_by(events, lambda x: int(x.position.lon))

    closest = find_smallest_elements(groups, lambda x: x.position.lon)

    return sorted(list(closest.values()), key=lambda x: x.position.time)
