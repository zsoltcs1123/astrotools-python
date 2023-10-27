from typing import Tuple
from zodiac.division import map_sign


def calculate_dmm_lon(lon: float) -> Tuple[int, float]:
    degrees = int(lon)
    minutes = ((lon - degrees) * 60)
    return (degrees, minutes)


def calculate_dms_lon(lon: float) -> Tuple[int, int, float]:
    degrees = int(lon)
    minutes = int((lon - degrees) * 60)
    seconds = (lon - degrees - minutes / 60) * 3600
    return (degrees, minutes, seconds)


def float_to_zodiacal(lon: float) -> str:
    sign_name = map_sign(lon).name
    sign_nr = (int)(lon / 30)
    deg = (int)(lon - sign_nr * 30)
    mins = round(calculate_dmm_lon(lon)[1])
    return f"{deg}{sign_name[:3]}{mins}"
