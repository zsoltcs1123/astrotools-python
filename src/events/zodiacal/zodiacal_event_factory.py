from typing import List, Optional
from util.common import find_smallest_elements, group_by, integral_ends_with
from core.zodiac.positions.mapped_geo_position import MappedGeoPosition as mgp
from events.zodiacal.astro_event import (
    AstroEvent,
    DecanChange,
    TropicalSignChange,
    VedicSignChange,
    TermChange,
    NakshatraChange,
    DirectionChange,
    TropicalProgression,
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
                elif event_type == TropicalSignChange:
                    self.check_functions.append(
                        ZodiacalEventFactory._check_tropical_sign_change
                    )
                elif event_type == VedicSignChange:
                    self.check_functions.append(
                        ZodiacalEventFactory._check_vedic_sign_change
                    )
                elif event_type == TermChange:
                    self.check_functions.append(ZodiacalEventFactory._check_term_change)
                elif event_type == NakshatraChange:
                    self.check_functions.append(
                        ZodiacalEventFactory._check_nakshatra_change
                    )
                elif event_type == DirectionChange:
                    self.check_functions.append(
                        ZodiacalEventFactory._check_direction_change
                    )
        self.event_types = event_types

    @staticmethod
    def _check_decan_change(previous: mgp, current: mgp) -> Optional[DecanChange]:
        if previous.tropical.decan.id != current.tropical.decan.id:
            return DecanChange(current.dt, previous, current)

    @staticmethod
    def _check_tropical_sign_change(
        previous: mgp, current: mgp
    ) -> Optional[TropicalSignChange]:
        if previous.tropical.sign.id != current.tropical.sign.id:
            return TropicalSignChange(current.dt, previous, current)

    @staticmethod
    def _check_vedic_sign_change(
        previous: mgp, current: mgp
    ) -> Optional[VedicSignChange]:
        if previous.vedic.sign.id != current.vedic.sign.id:
            return VedicSignChange(current.dt, previous, current)

    @staticmethod
    def _check_term_change(previous: mgp, current: mgp) -> Optional[TermChange]:
        if previous.tropical.term.id != current.tropical.term.id:
            return TermChange(current.dt, previous, current)

    @staticmethod
    def _check_direction_change(
        previous: mgp, current: mgp
    ) -> Optional[DirectionChange]:
        if previous.direction != current.direction:
            return DirectionChange(current.dt, previous, current)

    @staticmethod
    def _check_nakshatra_change(
        previous: mgp, current: mgp
    ) -> Optional[NakshatraChange]:
        if previous.vedic.nakshatra.id != current.vedic.nakshatra.id:
            return NakshatraChange(current.dt, previous, current)

    def _check_changes(self, previous: mgp, current: mgp):
        ret = []
        for check_function in self.check_functions:
            event = check_function(previous, current)
            if event is not None:
                ret.append(event)
        return ret

    def _get_tropical_progressions(self, mps: List[mgp]) -> List[AstroEvent]:
        events = []
        for mp in mps:
            if integral_ends_with(5, mp.tropical.lon.decimal):
                events.append(TropicalProgression(mp.dt, mp, "50%"))
            elif integral_ends_with(7, mp.tropical.lon.decimal):
                events.append(TropicalProgression(mp.dt, mp, "70%"))
            elif integral_ends_with(3, mp.tropical.lon.decimal):
                events.append(TropicalProgression(mp.dt, mp, "30%"))

        groups = group_by(events, lambda x: int(x.mp.tropical.lon.decimal))

        closest = find_smallest_elements(groups, lambda x: x.mp.tropical.lon.decimal)

        filtered_closest = {
            k: v
            for k, v in closest.items()
            if str(v.mp.tropical.position).endswith("0")
        }
        return sorted(list(filtered_closest.values()), key=lambda x: x.mp.dt)

    def create_events(self, mps: List[mgp]) -> List[AstroEvent]:
        if len(mps) < 2:
            return []

        ret = []
        for i in range(1, len(mps)):
            ret += self._check_changes(mps[i - 1], mps[i])

        if self.event_types.__contains__(TropicalProgression):
            progs = self._get_tropical_progressions(mps)
            ret += progs
        return ret
