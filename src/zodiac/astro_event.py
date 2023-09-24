from dataclasses import dataclass
from datetime import datetime
from typing import List
from core.util import ends_with, find_smallest_elements, group_by
from zodiac.mapped_position import MappedPosition


@dataclass
class AstroEvent:
    time: datetime

    def tv_timestamp(self) -> str:
        """timestamp("2023-02-27 11:05:00")"""
        return f'timestamp(\"{self.time.strftime("%Y-%m-%d %H:%M:%S")}\")'


@dataclass
class DecanChange(AstroEvent):
    current: MappedPosition
    previous: MappedPosition

    def __repr__(self) -> str:
        return f'{self.current.planet} Decan change at {self.current.time}: {self.previous.decan} -> {self.previous.decan}'

    def __str__(self) -> str:
        return f'Decan change at {self.current.time.strftime("%Y-%m-%d %H:%M:%S")}: {self.previous.decan.name} -> {self.previous.decan.name}'

@dataclass
class TermChange(AstroEvent):
    current: MappedPosition
    previous: MappedPosition

    def __repr__(self) -> str:
        f'{self.current.planet} Term change at {self.current.time}: {self.previous.term} -> {self.previous.term}'


@dataclass
class Progression(AstroEvent):
    name: str


def get_decan_changes(positions: List[MappedPosition]) -> List[AstroEvent]:
    return [DecanChange(pos.time, pos, prev_pos) for prev_pos, pos in zip(positions, positions[1:]) if pos.decan.id != prev_pos.decan.id]


def get_term_changes(positions: List[MappedPosition]) -> List[AstroEvent]:
    return [TermChange(pos.time, pos, prev_pos) for prev_pos, pos in zip(positions, positions[1:]) if pos.term.id != prev_pos.term.id]


def get_progressions(positions: List[MappedPosition]) -> List[AstroEvent]:
    events = []
    for pos in positions:
        if (ends_with(5, pos.lon)):
            events.append(Progression(pos, "50%"))
        # elif (ends_with(7, pos.lon)):
            # events.append(Progression(pos, "70%"))

    groups = group_by(events, lambda x: int(x.position.lon))

    closest = find_smallest_elements(groups, lambda x: x.position.lon)

    return sorted(list(closest.values()), key=lambda x: x.position.time)
