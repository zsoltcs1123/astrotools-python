from dataclasses import dataclass
from typing import List, Optional

from zodiac.degree_range import DegreeRange


@dataclass
class Division:
    id: int
    name: str
    degree_range: DegreeRange


class Decan(Division):
    pass


class Sign(Division):
    pass


class Term(Division):
    pass


def _get_division(degrees: float, lst: List[Division]) -> Optional[Division]:
    for decan in lst:
        if degrees in decan.degree_range:
            return decan
    return None


def map_sign(degrees: float) -> Optional[Sign]:
    return _get_division(degrees, SIGNS)


def map_decan(degrees: float) -> Optional[Decan]:
    return _get_division(degrees, DECANS)


def map_term(degrees: float) -> Optional[Term]:
    return _get_division(degrees, TERMS)


SIGNS = [
    Sign(1, 'Aries', DegreeRange(0, 30)),
    Sign(2, 'Taurus', DegreeRange(30, 60)),
    Sign(3, 'Gemini', DegreeRange(60, 90)),
    Sign(4, 'Cancer', DegreeRange(90, 120)),
    Sign(5, 'Leo', DegreeRange(120, 150)),
    Sign(6, 'Virgo', DegreeRange(150, 180)),
    Sign(7, 'Libra', DegreeRange(180, 210)),
    Sign(8, 'Scorpio', DegreeRange(210, 240)),
    Sign(9, 'Sagittarius', DegreeRange(240, 270)),
    Sign(10, 'Capricorn', DegreeRange(270, 300)),
    Sign(11, 'Aquarius', DegreeRange(300, 330)),
    Sign(12, 'Pisces', DegreeRange(330, 360))
]


DECANS = [
    Decan(1, "2W", DegreeRange(0, 10)),
    Decan(2, "3W", DegreeRange(10, 20)),
    Decan(3, "4W", DegreeRange(20, 30)),
    Decan(4, "5P", DegreeRange(30, 40)),
    Decan(5, "6P", DegreeRange(40, 50)),
    Decan(6, "7P", DegreeRange(50, 60)),
    Decan(7, "8S", DegreeRange(60, 70)),
    Decan(8, "9S", DegreeRange(70, 80)),
    Decan(9, "10S", DegreeRange(80, 90)),
    Decan(10, "2C", DegreeRange(90, 100)),
    Decan(11, "3C", DegreeRange(100, 110)),
    Decan(12, "4C", DegreeRange(110, 120)),
    Decan(13, "5W", DegreeRange(120, 130)),
    Decan(14, "6W", DegreeRange(130, 140)),
    Decan(15, "7W", DegreeRange(140, 150)),
    Decan(16, "8P", DegreeRange(150, 160)),
    Decan(17, "9P", DegreeRange(160, 170)),
    Decan(18, "10P", DegreeRange(170, 180)),
    Decan(19, "2S", DegreeRange(180, 190)),
    Decan(20, "3S", DegreeRange(190, 200)),
    Decan(21, "4S", DegreeRange(200, 210)),
    Decan(22, "5C", DegreeRange(210, 220)),
    Decan(23, "6C", DegreeRange(220, 230)),
    Decan(24, "7C", DegreeRange(230, 240)),
    Decan(25, "8W", DegreeRange(240, 250)),
    Decan(26, "9W", DegreeRange(250, 260)),
    Decan(27, "10W", DegreeRange(260, 270)),
    Decan(28, "2P", DegreeRange(270, 280)),
    Decan(29, "3P", DegreeRange(280, 290)),
    Decan(30, "4P", DegreeRange(290, 300)),
    Decan(31, "5S", DegreeRange(300, 310)),
    Decan(32, "6S", DegreeRange(310, 320)),
    Decan(33, "7S", DegreeRange(320, 330)),
    Decan(34, "8C", DegreeRange(330, 340)),
    Decan(35, "9C", DegreeRange(340, 350)),
    Decan(36, "10C", DegreeRange(350, 360))
]

TERMS = [
    Term(1, "Jupiter", DegreeRange(0, 6)),
    Term(2, "Venus", DegreeRange(6, 12)),
    Term(3, "Mercury", DegreeRange(12, 20)),
    Term(4, "Mars", DegreeRange(20, 25)),
    Term(5, "Saturn", DegreeRange(25, 30)),
    Term(6, "Venus", DegreeRange(30, 38)),
    Term(7, "Mercury", DegreeRange(38, 44)),
    Term(8, "Jupiter", DegreeRange(44, 52)),
    Term(9, "Saturn", DegreeRange(52, 57)),
    Term(10, "Mars", DegreeRange(57, 60)),
    Term(11, "Mercury", DegreeRange(60, 66)),
    Term(12, "Jupiter", DegreeRange(66, 72)),
    Term(13, "Venus", DegreeRange(72, 77)),
    Term(14, "Mars", DegreeRange(77, 84)),
    Term(15, "Saturn", DegreeRange(84, 90)),
    Term(16, "Mars", DegreeRange(90, 97)),
    Term(17, "Venus", DegreeRange(97, 103)),
    Term(18, "Mercury", DegreeRange(103, 109)),
    Term(19, "Jupiter", DegreeRange(109, 116)),
    Term(20, "Saturn", DegreeRange(116, 120)),
    Term(21, "Jupiter", DegreeRange(120, 126)),
    Term(22, "Venus", DegreeRange(126, 131)),
    Term(23, "Saturn", DegreeRange(131, 138)),
    Term(24, "Mercury", DegreeRange(138, 144)),
    Term(25, "Mars", DegreeRange(144, 150)),
    Term(26, "Mercury", DegreeRange(150, 157)),
    Term(27, "Venus", DegreeRange(157, 167)),
    Term(28, "Jupiter", DegreeRange(167, 171)),
    Term(29, "Mars", DegreeRange(171, 178)),
    Term(30, "Saturn", DegreeRange(178, 180)),
    Term(31, "Saturn", DegreeRange(180, 186)),
    Term(32, "Mercury", DegreeRange(186, 194)),
    Term(33, "Jupiter", DegreeRange(194, 201)),
    Term(34, "Venus", DegreeRange(201, 208)),
    Term(35, "Mars", DegreeRange(208, 210)),
    Term(36, "Mars", DegreeRange(210, 217)),
    Term(37, "Venus", DegreeRange(217, 221)),
    Term(38, "Mercury", DegreeRange(221, 229)),
    Term(39, "Jupiter", DegreeRange(229, 234)),
    Term(40, "Saturn", DegreeRange(234, 240)),
    Term(41, "Jupiter", DegreeRange(240, 252)),
    Term(42, "Venus", DegreeRange(252, 257)),
    Term(43, "Mercury", DegreeRange(257, 261)),
    Term(44, "Saturn", DegreeRange(261, 266)),
    Term(45, "Mars", DegreeRange(266, 270)),
    Term(46, "Mercury", DegreeRange(270, 277)),
    Term(47, "Jupiter", DegreeRange(277, 284)),
    Term(48, "Venus", DegreeRange(284, 292)),
    Term(49, "Saturn", DegreeRange(292, 296)),
    Term(50, "Mars", DegreeRange(296, 300)),
    Term(51, "Mercury", DegreeRange(300, 307)),
    Term(52, "Venus", DegreeRange(307, 313)),
    Term(53, "Jupiter", DegreeRange(313, 320)),
    Term(54, "Mars", DegreeRange(320, 325)),
    Term(55, "Saturn", DegreeRange(325, 330)),
    Term(56, "Venus", DegreeRange(330, 342)),
    Term(57, "Jupiter", DegreeRange(342, 346)),
    Term(58, "Mercury", DegreeRange(346, 349)),
    Term(59, "Mars", DegreeRange(349, 358)),
    Term(60, "Saturn", DegreeRange(358, 360))
]
