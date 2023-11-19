from typing import List, Optional
from util.common import find_smallest_elements, group_by, integral_ends_with
from zodiac.mapped_position import MappedPosition as mp
from events.astro_event import (
    AstroEvent,
    DecanChange,
    SignChange,
    TermChange,
    NakshatraChange,
    DirectionChange,
    Progression,
)


class ZodiacalEventFactory:
    def __init__(self, event_types: List[type]):
        self.check_functions = []

        for event_type in event_types:
            if not issubclass(event_type, AstroEvent):
                raise ValueError(
                    f"{event_type.__name__} is not a subclass of AstroEvent"
                )
            else:
                if event_type == DecanChange:
                    self.check_functions.append(
                        ZodiacalEventFactory._check_decan_change
                    )
                elif event_type == SignChange:
                    self.check_functions.append(ZodiacalEventFactory._check_sign_change)
                elif event_type == TermChange:
                    self.check_functions.append(ZodiacalEventFactory._check_term_change)
                elif event_type == NakshatraChange:
                    self.check_functions.append(ZodiacalEventFactory._check_nakshatra_change)
                elif event_type == DirectionChange:
                    self.check_functions.append(
                        ZodiacalEventFactory._check_direction_change
                    )
                elif event_type == Progression:
                    self.check_functions.append(ZodiacalEventFactory._get_progressions)
        self.event_types = event_types

    @staticmethod
    def _check_decan_change(previous: mp, current: mp) -> Optional[DecanChange]:
        if previous.decan.id != current.decan.id:
            return DecanChange(current.base_position.dt, previous, current)

    @staticmethod
    def _check_sign_change(previous: mp, current: mp) -> Optional[SignChange]:
        if previous.sign.id != current.sign.id:
            return SignChange(current.base_position.dt, previous, current)

    @staticmethod
    def _check_term_change(previous: mp, current: mp) -> Optional[TermChange]:
        if previous.term.id != current.term.id:
            return TermChange(current.base_position.dt, previous, current)

    @staticmethod
    def _check_direction_change(previous: mp, current: mp) -> Optional[DirectionChange]:
        if previous.direction != current.direction:
            return DirectionChange(current.base_position.dt, previous, current)
        
    @staticmethod
    def _check_nakshatra_change(previous: mp, current: mp) -> Optional[NakshatraChange]:
        if previous.nakshatra.id != current.nakshatra.id:
            return NakshatraChange(current.base_position.dt, previous, current)

    def _check_changes(self, previous: mp, current: mp):
        ret = []
        for check_function in self.check_functions:
            event = check_function(previous, current)
            if event is not None:
                ret.append(event)
        return ret

    def _get_progressions(self, mps: List[mp]) -> List[AstroEvent]:
        events = []
        for mp in mps:
            if integral_ends_with(5, mp.base_position.lon.dec):
                events.append(Progression(mp.base_position.dt, mp, "50%"))
            elif integral_ends_with(7, mp.base_position.lon.dec):
                events.append(Progression(mp.base_position.dt, mp, "70%"))
            elif integral_ends_with(3, mp.base_position.lon.dec):
                events.append(Progression(mp.base_position.dt, mp, "30%"))

        groups = group_by(events, lambda x: int(x.mp.base_position.lon.dec))

        closest = find_smallest_elements(groups, lambda x: x.mp.base_position.lon.dec)

        filtered_closest = {
            k: v for k, v in closest.items() if str(v.mp.tropical_pos).endswith("0")
        }
        return sorted(list(filtered_closest.values()), key=lambda x: x.mp.base_position.dt)

    def create_events(self, mps: List[mp]) -> List[AstroEvent]:
        if len(mps) < 2:
            return []

        ret = []
        for i in range(1, len(mps)):
            ret += self._check_changes(mps[i - 1], mps[i])

        progs = self._get_progressions(mps)
        ret += progs
        return ret
