from core.angle import Angle
from core.position_factory import create_geo_position
from zodiac.mapped_geo_position import MappedGeoPosition as mp
from typing import Callable, Dict, List


def generate_angles_dict(
    mps: List[mp], target_selector: Callable[[str], List[str]]
) -> Dict[str, List[Angle]]:
    angles = {}
    for mp in mps:
        targets = target_selector(mp.point)

        angles[mp.point] = []

        for t in targets:
            target_mp = next((p for p in mps if p.point == t), None)
            if target_mp is not None:
                angle = Angle(mp, target_mp)
                angles[mp.point].append(angle)

    return angles


def generate_angles_list(
    mps: Dict[str, List[mp]], target_selector: Callable[[str], List[str]]
) -> List[Angle]:
    angles = []
    for p, mp_list in mps.items():
        targets = target_selector(p)

        for source_mp in mp_list:
            for t in targets:
                target_bp = create_geo_position(t, source_mp.dt)
                target_mp = mp(target_bp)
                angle = Angle(source_mp, target_mp)
                angles.append(angle)

    return angles
