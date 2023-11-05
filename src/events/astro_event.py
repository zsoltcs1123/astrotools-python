from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from util.common import decimal_ends_with, integral_ends_with, find_smallest_elements, group_by
from zodiac.mapped_position import MappedPosition as mp


@dataclass
class AstroEvent:
    time: datetime

    def tv_timestamp(self) -> str:
        """timestamp("2023-02-27 11:05:00")"""
        return f'timestamp(\"{self.time.strftime("%Y-%m-%d %H:%M:%S")}\")'


@dataclass
class PositionalEvent(AstroEvent):
    previous: mp
    current: mp


@dataclass
class SignChange(PositionalEvent):

    def __repr__(self) -> str:
        return f'{self.current.position.dt}\t{self.current.position.name}\tSign change\t{self.previous.sign.name} -> {self.current.sign.name}'


@dataclass
class DecanChange(PositionalEvent):

    def __repr__(self) -> str:
        return f'{self.current.position.dt}\t{self.current.position.name}\tDecan change\t{self.previous.decan.name} -> {self.current.decan.name}'


@dataclass
class TermChange(PositionalEvent):

    def __repr__(self) -> str:
        return f'{self.current.position.dt}\t{self.current.position.name}\tTerm change\t{self.previous.term.name} -> {self.current.term.name}'


@dataclass
class DirectionChange(PositionalEvent):

    def __repr__(self) -> str:
        return f'{self.current.position.dt}\t{self.current.position.name}\Direct change\t{self.previous.direction} -> {self.current.direction}'


@dataclass
class Progression(AstroEvent):
    mp: mp
    name: str

    def __repr__(self) -> str:
        return f'{self.time}\t{self.mp.position.name}\t{self.name} progression at\t{self.mp.zodiac_pos}'


def check_decan_change(previous: mp, current: mp) -> Optional[DecanChange]:
    if previous.decan.id != current.decan.id:
        return DecanChange(current.position.dt, previous, current)


def check_sign_change(previous: mp, current: mp) -> Optional[SignChange]:
    if previous.sign.id != current.sign.id:
        return SignChange(current.position.dt, previous, current)


def check_term_change(previous: mp, current: mp) -> Optional[TermChange]:
    if previous.term.id != current.term.id:
        return TermChange(current.position.dt, previous, current)


def check_direction_change(previous: mp, current: mp) -> Optional[DirectionChange]:
    if previous.direction != current.direction:
        return DirectionChange(current.position.dt, previous, current)


check_functions = [check_decan_change, check_sign_change,
                   check_term_change, check_direction_change]


def get_astro_events(mps: List[mp]) -> List[AstroEvent]:
    if len(mps) < 2:
        return []

    ret = []
    for i in range(1, len(mps)):
        ret += _check_changes(mps[i-1], mps[i])

    progs = get_progressions(mps)
    ret += progs
    return ret


def _check_changes(previous: mp, current: mp):
    ret = []
    for check_function in check_functions:
        event = check_function(previous, current)
        if event is not None:
            ret.append(event)
    return ret


def get_progressions(mps: List[mp]) -> List[AstroEvent]:
    events = []
    for mp in mps:
        if integral_ends_with(5, mp.position.lon):
            events.append(Progression(mp.position.dt, mp, "50%"))
        elif (integral_ends_with(7, mp.position.lon)):
            events.append(Progression(mp.position.dt, mp, "70%"))
        elif (integral_ends_with(3, mp.position.lon)):
            events.append(Progression(mp.position.dt, mp, "30%"))

    groups = group_by(events, lambda x: int(x.mp.position.lon))

    closest = find_smallest_elements(groups, lambda x: x.mp.position.lon)
    
    filtered_closest = {k: v for k, v in closest.items() if str(v.mp.zodiac_pos).endswith('0')}
    return sorted(list(filtered_closest.values()), key=lambda x: x.mp.position.dt)
