from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from core.util import ends_with, find_smallest_elements, group_by
from core.mapped_planetary_position import MappedPlanetaryPosition as mpp


@dataclass
class AstroEvent:
    time: datetime

    def tv_timestamp(self) -> str:
        """timestamp("2023-02-27 11:05:00")"""
        return f'timestamp(\"{self.time.strftime("%Y-%m-%d %H:%M:%S")}\")'


@dataclass
class PositionalEvent(AstroEvent):
    previous: mpp
    current: mpp


@dataclass
class SignChange(PositionalEvent):

    def __repr__(self) -> str:
        return f'{self.current.position.planet} Sign change at {self.current.position.dt}: {self.previous.sign.name} -> {self.current.sign.name}'


@dataclass
class DecanChange(PositionalEvent):

    def __repr__(self) -> str:
        return f'{self.current.position.planet} Decan change at {self.current.position.dt}: {self.previous.decan.name} -> {self.current.decan.name}'


@dataclass
class TermChange(PositionalEvent):

    def __repr__(self) -> str:
        return f'{self.current.position.planet} Term change at {self.current.position.dt}: {self.previous.term.name} -> {self.current.term.name}'


@dataclass
class DirectionChange(PositionalEvent):

    def __repr__(self) -> str:
        return f'{self.current.position.planet} Direction change at {self.current.position.dt}: {self.previous.direction} -> {self.current.direction}'


@dataclass
class Progression(AstroEvent):
    name: str


def check_decan_change(previous: mpp, current: mpp) -> Optional[DecanChange]:
    if previous.decan.id != current.decan.id:
        return DecanChange(current.position.dt, previous, current)


def check_sign_change(previous: mpp, current: mpp) -> Optional[SignChange]:
    if previous.sign.id != current.sign.id:
        return SignChange(current.position.dt, previous, current)


def check_term_change(previous: mpp, current: mpp) -> Optional[TermChange]:
    if previous.term.id != current.term.id:
        return TermChange(current.position.dt, previous, current)


def check_direction_change(previous: mpp, current: mpp) -> Optional[DirectionChange]:
    if previous.direction != current.direction:
        return DirectionChange(current.position.dt, previous, current)


check_functions = [check_decan_change, check_sign_change, check_term_change, check_direction_change]


def get_astro_events(mpps: List[mpp]) -> List[AstroEvent]:
    if len(mpps) < 2:
        return []

    ret = []
    for i in range(1, len(mpps)):
        ret += _check_changes(mpps[i-1], mpps[i])
    return ret


def _check_changes(previous: mpp, current: mpp):
    ret = []
    for check_function in check_functions:
        event = check_function(previous, current)
        if event is not None:
            ret.append(event)
    return ret

# TBD


def get_progressions(positions: List[mpp]) -> List[AstroEvent]:
    events = []
    for pos in positions:
        if (ends_with(5, pos.lon)):
            events.append(Progression(pos, "50%"))
        # elif (ends_with(7, pos.lon)):
            # events.append(Progression(pos, "70%"))

    groups = group_by(events, lambda x: int(x.position.lon))

    closest = find_smallest_elements(groups, lambda x: x.position.lon)

    return sorted(list(closest.values()), key=lambda x: x.position.time)
