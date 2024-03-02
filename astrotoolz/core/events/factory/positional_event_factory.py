from typing import Callable, List, Optional

from astrotoolz.core.enums import CoordinateSystem
from astrotoolz.core.events.astro_event import (
    AstroEvent,
    DecanChange,
    DirectionChange,
    NakshatraChange,
    PositionalEvent,
    SiderealSignChange,
    TermChange,
    TropicalProgression,
    TropicalSignChange,
)
from astrotoolz.core.zodiac.mapped_position import MappedPosition as mp
from astrotoolz.util.common import find_smallest_elements, group_by, integral_ends_with
from astrotoolz.util.logger_base import LoggerBase

CheckFunction = Callable[[mp, mp, CoordinateSystem], Optional[AstroEvent]]


class PositionalEventFactory(LoggerBase):

    def __init__(self, event_types: List[type], coord_system: CoordinateSystem):
        self.event_types = event_types
        self.coord_system = coord_system
        self.check_functions = self._get_check_functions()

    def create_events(self, mps: List[mp]) -> List[PositionalEvent]:
        if len(mps) < 2:
            return []

        ret = []
        for i in range(1, len(mps)):
            ret += self._check_changes(mps[i - 1], mps[i])

        if self.event_types.__contains__(TropicalProgression):
            progs = self._get_tropical_progressions(mps)
            ret += progs
        return ret

    def _get_check_functions(
        self,
    ) -> List[CheckFunction]:
        check_functions = []

        for event_type in self.event_types:
            if not issubclass(event_type, AstroEvent):
                raise ValueError(
                    f"{event_type.__name__} is not a subclass of AstroEvent"
                )
            else:
                if event_type == DecanChange:
                    check_functions.append(self._check_decan_change)
                elif event_type == TropicalSignChange:
                    check_functions.append(self._check_tropical_sign_change)
                elif event_type == SiderealSignChange:
                    check_functions.append(self._check_sidereal_sign_change)
                elif event_type == TermChange:
                    check_functions.append(self._check_term_change)
                elif event_type == NakshatraChange:
                    check_functions.append(self._check_nakshatra_change)
                elif event_type == DirectionChange:
                    check_functions.append(self._check_direction_change)
        return check_functions

    def _check_changes(
        self,
        previous: mp,
        current: mp,
    ) -> List:
        ret = []
        for check_function in self.check_functions:
            event = check_function(previous, current, self.coord_system)
            if event is not None:
                ret.append(event)
        return ret

    @staticmethod
    def _check_decan_change(
        previous: mp, current: mp, coord_system: CoordinateSystem
    ) -> Optional[DecanChange]:
        if previous.tropical.decan.id != current.tropical.decan.id:
            return DecanChange(current, previous, coord_system)

    @staticmethod
    def _check_tropical_sign_change(
        previous: mp, current: mp, coord_system: CoordinateSystem
    ) -> Optional[TropicalSignChange]:
        if previous.tropical.sign.id != current.tropical.sign.id:
            return TropicalSignChange(current, previous, coord_system)

    @staticmethod
    def _check_sidereal_sign_change(
        previous: mp, current: mp, coord_system: CoordinateSystem
    ) -> Optional[SiderealSignChange]:
        if previous.vedic.sign.id != current.vedic.sign.id:
            return SiderealSignChange(current, previous, coord_system)

    @staticmethod
    def _check_term_change(
        previous: mp, current: mp, coord_system: CoordinateSystem
    ) -> Optional[TermChange]:
        if previous.tropical.term.id != current.tropical.term.id:
            return TermChange(current, previous, coord_system)

    @staticmethod
    def _check_direction_change(
        previous: mp, current: mp, coord_system: CoordinateSystem
    ) -> Optional[DirectionChange]:
        if previous.direction != current.direction:
            return DirectionChange(current, previous, coord_system)

    @staticmethod
    def _check_nakshatra_change(
        previous: mp, current: mp, coord_system: CoordinateSystem
    ) -> Optional[NakshatraChange]:
        if previous.vedic.nakshatra.id != current.vedic.nakshatra.id:
            return NakshatraChange(current, previous, coord_system)

    @staticmethod
    def _get_tropical_progressions(
        mps: List[mp], coord_system: CoordinateSystem
    ) -> List[PositionalEvent]:
        events = []
        for mpos in enumerate(mps):
            if integral_ends_with(5, mpos.tropical.lon.decimal):
                events.append(TropicalProgression("50%", mp, coord_system))
            elif integral_ends_with(7, mpos.tropical.lon.decimal):
                events.append(TropicalProgression("70%", mp, coord_system))
            elif integral_ends_with(3, mpos.tropical.lon.decimal):
                events.append(TropicalProgression("30%", mp, coord_system))

        groups = group_by(events, lambda x: int(x.mp.tropical.lon.decimal))

        closest = find_smallest_elements(groups, lambda x: x.mp.tropical.lon.decimal)

        filtered_closest = {
            k: v
            for k, v in closest.items()
            if str(v.mp.tropical.position).endswith("0")
        }
        return sorted(list(filtered_closest.values()), key=lambda x: x.mp.dt)
