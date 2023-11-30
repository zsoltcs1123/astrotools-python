from objects.points import NN
from tools.horoscope.horoscope import Horoscope
from util.cached_property import CachedProperty
from zodiac.mapped_position import MappedPosition as mp


class VedicHoroscope(Horoscope):
    @CachedProperty
    def atmakaraka(self):
        result = self.calculate_atmakaraka()
        return result

    def calculate_atmakaraka(self) -> mp:
        sorted_mps = sorted(
            self.mps,
            key=lambda mp: int(mp.vedic.position[2:])
            if mp.point != NN
            else int(30 - mp.vedic.position[2:]),
        )
        return sorted_mps[0]
