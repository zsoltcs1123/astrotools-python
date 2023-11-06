from typing import Dict, List

NN = "north node"
SN = "south node"
MOON = "moon"
MEAN_NODE = 'MEAN_NODE'

PLANETS = [
    "sun",
    MOON,
    "mercury",
    "venus",
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune",
    "pluto",
]


NODES = [NN, SN]

ANGULARS = ["ASC", "MC", "IC", "DC"]


PLANETS_MAP = {
    "mercury": 1,
    "venus": 2,
    "mars": 3,
    "jupiter": 4,
    "saturn": 5,
    "uranus": 6,
    "neptune": 7,
    "pluto": 8,
    NN: 9,
}

ALL_POINTS = PLANETS + NODES

POINTS_NO_MOON = [planet for planet in PLANETS if planet != MOON] + [NN]


def get_default_angle_targets(point: str) -> List[str]:
    if point == "sun" or point == "moon":
        return list(PLANETS_MAP.keys())
    elif point == SN:
        return []
    else:
        return [k for k, v in PLANETS_MAP.items() if v > PLANETS_MAP[point]]
