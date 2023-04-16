PLANETS = ["sun", "moon", "mercury", "venus", "mars",
           "Jupiter barycenter", "Saturn barycenter", "Uranus barycenter", "Neptune barycenter", "Pluto barycenter"]


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


def get_angle_targets(planet):
    if planet == 'sun' or planet == 'moon':
        return PLANETS_MAP
    else:
        return filter(PLANETS_MAP, lambda p: PLANETS_MAP[p] > PLANETS_MAP[planet])
