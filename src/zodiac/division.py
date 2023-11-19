from dataclasses import dataclass
from typing import List, Optional
from core.degree import Degree
from zodiac.degree_range import DegreeRange as DR


@dataclass
class Division:
    id: int
    name: str
    degree_range: DR


class Decan(Division):
    pass


class Sign(Division):
    ruler: str


class Term(Division):
    pass


class Nakshatra(Division):
    pass


def _get_division(degrees: float, lst: List[Division]) -> Optional[Division]:
    for div in lst:
        if degrees in div.degree_range:
            return div
    return None


def map_sign(degrees: float) -> Optional[Sign]:
    return _get_division(degrees, SIGNS)


def map_decan(degrees: float) -> Optional[Decan]:
    return _get_division(degrees, DECANS)


def map_term(degrees: float) -> Optional[Term]:
    return _get_division(degrees, TERMS)


def map_nakshatra(degrees: float) -> Optional[Nakshatra]:
    return _get_division(degrees, NAKSHATRAS)


def _deg(d: int, m: int, s: int) -> Degree:
    return Degree.from_dms(d, m, s)

def _dr_floats(start, end) -> Degree:
    return DR.from_floats(start, end)

def _dr_degs(start, end) -> Degree:
    return DR.from_degrees(start, end)


NAKSHATRAS = [
    Nakshatra(1, 'Aswini', _dr_degs(_deg(0, 0, 0), _deg(13, 20, 0))),
    Nakshatra(2, 'Bharani', _dr_degs(_deg(13, 20, 0), _deg(26, 40, 0))),
    Nakshatra(3, 'Krittika', _dr_degs(_deg(26, 40, 0), _deg(40, 0, 0))),
    Nakshatra(4, 'Rohini', _dr_degs(_deg(40, 0, 0), _deg(53, 20, 0))),
    Nakshatra(5, 'Mrigashirsha', _dr_degs(_deg(53, 20, 0), _deg(66, 40, 0))),
    Nakshatra(6, 'Ardra', _dr_degs(_deg(66, 40, 0), _deg(80, 0, 0))),
    Nakshatra(7, 'Punarvasu', _dr_degs(_deg(80, 0, 0), _deg(93, 20, 0))),
    Nakshatra(8, 'Pushya', _dr_degs(_deg(93, 20, 0), _deg(106, 40, 0))),
    Nakshatra(9, 'Ashlesha', _dr_degs(_deg(106, 40, 0), _deg(120, 0, 0))),
    Nakshatra(10, 'Magha', _dr_degs(_deg(120, 0, 0), _deg(133, 20, 0))),
    Nakshatra(11, 'Purva Phalguni', _dr_degs(_deg(133, 20, 0), _deg(146, 40, 0))),
    Nakshatra(12, 'Uttara Phalguni', _dr_degs(_deg(146, 40, 0), _deg(160, 0, 0))),
    Nakshatra(13, 'Hasta', _dr_degs(_deg(160, 0, 0), _deg(173, 20, 0))),
    Nakshatra(14, 'Chitra', _dr_degs(_deg(173, 20, 0), _deg(186, 40, 0))),
    Nakshatra(15, 'Swati', _dr_degs(_deg(186, 40, 0), _deg(200, 0, 0))),
    Nakshatra(16, 'Vishakha', _dr_degs(_deg(200, 0, 0), _deg(213, 20, 0))),
    Nakshatra(17, 'Anuradha', _dr_degs(_deg(213, 20, 0), _deg(226, 40, 0))),
    Nakshatra(18, 'Jyeshtha', _dr_degs(_deg(226, 40, 0), _deg(240, 0, 0))),
    Nakshatra(19, 'Mula', _dr_degs(_deg(240, 0, 0), _deg(253, 20, 0))),
    Nakshatra(20, 'Purva Ashadha', _dr_degs(_deg(253, 20, 0), _deg(266, 40, 0))),
    Nakshatra(21, 'Uttara Ashadha', _dr_degs(_deg(266, 40, 0), _deg(280, 0, 0))),
    Nakshatra(22, 'Shravana', _dr_degs(_deg(280, 0, 0), _deg(293, 20, 0))),
    Nakshatra(23, 'Dhanishta', _dr_degs(_deg(293, 20, 0), _deg(306, 40, 0))),
    Nakshatra(24, 'Shatabhisha', _dr_degs(_deg(306, 40, 0), _deg(320, 0, 0))),
    Nakshatra(25, 'Purva Bhadrapada', _dr_degs(_deg(320, 0, 0), _deg(333, 20, 0))),
    Nakshatra(26, 'Uttara Bhadrapada', _dr_degs(_deg(333, 20, 0), _deg(346, 40, 0))),
    Nakshatra(27, 'Revati', _dr_degs(_deg(346, 40, 0), _deg(360, 0, 0)))
]



SIGNS = [
    Sign(1, 'Aries', _dr_floats(0, 30)),
    Sign(2, 'Taurus', _dr_floats(30, 60)),
    Sign(3, 'Gemini', _dr_floats(60, 90)),
    Sign(4, 'Cancer', _dr_floats(90, 120)),
    Sign(5, 'Leo', _dr_floats(120, 150)),
    Sign(6, 'Virgo', _dr_floats(150, 180)),
    Sign(7, 'Libra', _dr_floats(180, 210)),
    Sign(8, 'Scorpio', _dr_floats(210, 240)),
    Sign(9, 'Sagittarius', _dr_floats(240, 270)),
    Sign(10, 'Capricorn', _dr_floats(270, 300)),
    Sign(11, 'Aquarius', _dr_floats(300, 330)),
    Sign(12, 'Pisces', _dr_floats(330, 360))
]


DECANS = [
    Decan(1, "2W", _dr_floats(0, 10)),
    Decan(2, "3W", _dr_floats(10, 20)),
    Decan(3, "4W", _dr_floats(20, 30)),
    Decan(4, "5P", _dr_floats(30, 40)),
    Decan(5, "6P", _dr_floats(40, 50)),
    Decan(6, "7P", _dr_floats(50, 60)),
    Decan(7, "8S", _dr_floats(60, 70)),
    Decan(8, "9S", _dr_floats(70, 80)),
    Decan(9, "10S", _dr_floats(80, 90)),
    Decan(10, "2C", _dr_floats(90, 100)),
    Decan(11, "3C", _dr_floats(100, 110)),
    Decan(12, "4C", _dr_floats(110, 120)),
    Decan(13, "5W", _dr_floats(120, 130)),
    Decan(14, "6W", _dr_floats(130, 140)),
    Decan(15, "7W", _dr_floats(140, 150)),
    Decan(16, "8P", _dr_floats(150, 160)),
    Decan(17, "9P", _dr_floats(160, 170)),
    Decan(18, "10P", _dr_floats(170, 180)),
    Decan(19, "2S", _dr_floats(180, 190)),
    Decan(20, "3S", _dr_floats(190, 200)),
    Decan(21, "4S", _dr_floats(200, 210)),
    Decan(22, "5C", _dr_floats(210, 220)),
    Decan(23, "6C", _dr_floats(220, 230)),
    Decan(24, "7C", _dr_floats(230, 240)),
    Decan(25, "8W", _dr_floats(240, 250)),
    Decan(26, "9W", _dr_floats(250, 260)),
    Decan(27, "10W", _dr_floats(260, 270)),
    Decan(28, "2P", _dr_floats(270, 280)),
    Decan(29, "3P", _dr_floats(280, 290)),
    Decan(30, "4P", _dr_floats(290, 300)),
    Decan(31, "5S", _dr_floats(300, 310)),
    Decan(32, "6S", _dr_floats(310, 320)),
    Decan(33, "7S", _dr_floats(320, 330)),
    Decan(34, "8C", _dr_floats(330, 340)),
    Decan(35, "9C", _dr_floats(340, 350)),
    Decan(36, "10C", _dr_floats(350, 360))
]

TERMS = [
    Term(1, "Jupiter", _dr_floats(0, 6)),
    Term(2, "Venus", _dr_floats(6, 12)),
    Term(3, "Mercury", _dr_floats(12, 20)),
    Term(4, "Mars", _dr_floats(20, 25)),
    Term(5, "Saturn", _dr_floats(25, 30)),
    Term(6, "Venus", _dr_floats(30, 38)),
    Term(7, "Mercury", _dr_floats(38, 44)),
    Term(8, "Jupiter", _dr_floats(44, 52)),
    Term(9, "Saturn", _dr_floats(52, 57)),
    Term(10, "Mars", _dr_floats(57, 60)),
    Term(11, "Mercury", _dr_floats(60, 66)),
    Term(12, "Jupiter", _dr_floats(66, 72)),
    Term(13, "Venus", _dr_floats(72, 77)),
    Term(14, "Mars", _dr_floats(77, 84)),
    Term(15, "Saturn", _dr_floats(84, 90)),
    Term(16, "Mars", _dr_floats(90, 97)),
    Term(17, "Venus", _dr_floats(97, 103)),
    Term(18, "Mercury", _dr_floats(103, 109)),
    Term(19, "Jupiter", _dr_floats(109, 116)),
    Term(20, "Saturn", _dr_floats(116, 120)),
    Term(21, "Jupiter", _dr_floats(120, 126)),
    Term(22, "Venus", _dr_floats(126, 131)),
    Term(23, "Saturn", _dr_floats(131, 138)),
    Term(24, "Mercury", _dr_floats(138, 144)),
    Term(25, "Mars", _dr_floats(144, 150)),
    Term(26, "Mercury", _dr_floats(150, 157)),
    Term(27, "Venus", _dr_floats(157, 167)),
    Term(28, "Jupiter", _dr_floats(167, 171)),
    Term(29, "Mars", _dr_floats(171, 178)),
    Term(30, "Saturn", _dr_floats(178, 180)),
    Term(31, "Saturn", _dr_floats(180, 186)),
    Term(32, "Mercury", _dr_floats(186, 194)),
    Term(33, "Jupiter", _dr_floats(194, 201)),
    Term(34, "Venus", _dr_floats(201, 208)),
    Term(35, "Mars", _dr_floats(208, 210)),
    Term(36, "Mars", _dr_floats(210, 217)),
    Term(37, "Venus", _dr_floats(217, 221)),
    Term(38, "Mercury", _dr_floats(221, 229)),
    Term(39, "Jupiter", _dr_floats(229, 234)),
    Term(40, "Saturn", _dr_floats(234, 240)),
    Term(41, "Jupiter", _dr_floats(240, 252)),
    Term(42, "Venus", _dr_floats(252, 257)),
    Term(43, "Mercury", _dr_floats(257, 261)),
    Term(44, "Saturn", _dr_floats(261, 266)),
    Term(45, "Mars", _dr_floats(266, 270)),
    Term(46, "Mercury", _dr_floats(270, 277)),
    Term(47, "Jupiter", _dr_floats(277, 284)),
    Term(48, "Venus", _dr_floats(284, 292)),
    Term(49, "Saturn", _dr_floats(292, 296)),
    Term(50, "Mars", _dr_floats(296, 300)),
    Term(51, "Mercury", _dr_floats(300, 307)),
    Term(52, "Venus", _dr_floats(307, 313)),
    Term(53, "Jupiter", _dr_floats(313, 320)),
    Term(54, "Mars", _dr_floats(320, 325)),
    Term(55, "Saturn", _dr_floats(325, 330)),
    Term(56, "Venus", _dr_floats(330, 342)),
    Term(57, "Jupiter", _dr_floats(342, 346)),
    Term(58, "Mercury", _dr_floats(346, 349)),
    Term(59, "Mars", _dr_floats(349, 358)),
    Term(60, "Saturn", _dr_floats(358, 360))
]
