from typing import Dict


PLANETS = ['sun', 'moon', 'mercury', 'venus', 'mars',
           'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']

NN = 'north node'
SN = 'south node'

NODES = [NN, SN]

ANGULARS = ['ASC', 'MC', 'IC', 'DC']


PLANETS_MAP = {
    'mercury': 1,
    'venus': 2,
    'mars': 3,
    'jupiter': 4,
    'saturn': 5,
    'uranus': 6,
    'neptune': 7,
    'pluto': 8
}


def get_outer_planets_map(planet: str) -> Dict[str, int]:
    if planet == 'sun' or planet == 'moon':
        return PLANETS_MAP
    else:
        return {k: v for k, v in PLANETS_MAP.items() if v > PLANETS_MAP[planet]}
