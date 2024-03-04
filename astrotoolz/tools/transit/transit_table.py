from dataclasses import dataclass
from typing import Dict, List

from astrotoolz.core.angles.angle import Angle
from astrotoolz.core.events.aspect import Aspect
from astrotoolz.core.events.factory.aspect_factory import AspectFactory


@dataclass
class TransitTable:
    angles: Dict[str, List[Angle]]
    aspects: Dict[str, List[Aspect]]

    def __init__(self, angles: List[Angle]):
        self.angles = angles

        asp_factory = AspectFactory()
        self.aspects = asp_factory.find_exact_aspects(self.angles, 1, [30])
