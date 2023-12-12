from core.angle import Angle
from zodiac.mapped_position import MappedPosition as mp
from typing import Callable, Dict, List


def generate_angles_from_mps(
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
