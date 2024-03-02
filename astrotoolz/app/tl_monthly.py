import enum  # Import the enum module at the top of your file
import json
import logging
from datetime import date, datetime
from types import (
    BuiltinFunctionType,
    BuiltinMethodType,
    MappingProxyType,
    MethodDescriptorType,
    WrapperDescriptorType,
)

from astrotoolz.core.enums import CoordinateSystem, NodeCalc, Zodiac
from astrotoolz.core.events.astro_event import (
    DecanChange,
    DeclinationExtreme,
    DirectionChange,
    LatitudeExtreme,
    SpeedExtreme,
    TermChange,
    TropicalSignChange,
)
from astrotoolz.core.points import NN
from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.core.zodiac.division import Division
from astrotoolz.core.zodiac.mapped_position import MappedPosition
from astrotoolz.core.zodiac.tropical_attributes import TropicalAttributes
from astrotoolz.core.zodiac.vedic_attributes import VedicAttributes
from astrotoolz.out.file import to_text_file
from astrotoolz.timeline.timeline import Timeline
from astrotoolz.timeline.timeline_config import AspectsConfig, TimelineConfig
from astrotoolz.timeline.timeline_factory_builder import build_timeline_factory
from astrotoolz.util.common import measure

logging.basicConfig(level=logging.DEBUG)


def timeline():

    cfg = TimelineConfig(
        CoordinateSystem.GEO,
        datetime(2024, 3, 1),
        datetime(2024, 4, 1),
        60,
        [
            "sun",
            "mercury",
            "venus",
            "mars",
            "jupiter",
            "saturn",
            "uranus",
            "neptune",
            "pluto",
            NN,
        ],
        [
            TropicalSignChange,
            DecanChange,
            TermChange,
            DeclinationExtreme,
            LatitudeExtreme,
            SpeedExtreme,
            DirectionChange,
        ],
        [
            AspectsConfig(30, True, 0.1),
        ],
        [Zodiac.TROPICAL],
        NodeCalc.MEAN,
    )

    factory = build_timeline_factory(cfg)

    timeline = factory.create_timeline(cfg)

    timeline_json = json.dumps(timeline, cls=CustomJSONEncoder)

    to_text_file(
        "json_march.txt",
        timeline_json,
    )
    # print(timeline_json)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # logging.debug(f"Trying to serialize an object of type: {type(obj)}")

        if isinstance(obj, Timeline):
            return {"events": obj.events}

        if isinstance(obj, Division):
            return {"name": obj.name}

        if isinstance(obj, MappedPosition):
            dic = {
                "point": obj.point,
                "lon": obj.lon.decimal,
                "lat": obj.lat.decimal,
                "speed": obj.speed.decimal,
                "ra": obj.ra.decimal if obj.ra is not None else None,
                "dec": obj.dec.decimal if obj.dec is not None else None,
            }

            if obj.vedic:
                dic["vedic"]: obj.vedic

            if obj.tropical:
                dic["tropical"]: obj.tropical

            return dic

        if isinstance(obj, BasePosition):
            dic = {
                "point": obj.point,
                "lon": obj.lon.decimal,
                "lat": obj.lat.decimal,
                "speed": obj.speed.decimal,
                "ra": obj.ra.decimal,
                "dec": obj.dec.decimal,
            }

            if obj.vedic:
                dic["vedic"]: obj.vedic

            if obj.tropical:
                dic["tropical"]: obj.tropical

            return dic

        if isinstance(obj, TropicalAttributes):
            return {
                "zodiacal_position": obj.zodiacal_position,
                "sign": obj.sign.name,
                "sign_ruler": obj.sign_ruler,
                "decan": obj.decan.name,
                "term": obj.term.name,
                "house": obj.house,
            }

        if isinstance(obj, VedicAttributes):
            return {
                "zodiacal_position": obj.zodiacal_position,
                "sign": obj.sign.name,
                "sign_ruler": obj.sign_ruler,
                "nakshatra": obj.nakshatra.name,
                "nakshatra_lord": obj.nakshatra_ruler,
                "house": obj.house,
            }

        if isinstance(obj, (datetime, date)):  # Updated line
            return obj.isoformat()
        elif isinstance(obj, enum.Enum):
            return obj.name
        elif hasattr(obj, "__dict__"):
            return dict(obj.__dict__)
        elif isinstance(obj, MappingProxyType):
            return dict(obj)
        elif isinstance(
            obj,
            (
                BuiltinFunctionType,
                BuiltinMethodType,
                WrapperDescriptorType,
                MethodDescriptorType,
            ),
        ):
            logging.warning(
                f"Skipping serialization of builtin function or method: {obj}"
            )
            return None
        else:
            logging.error(f"Cannot serialize object of type: {type(obj)}")
            return super().default(obj)


if __name__ == "__main__":
    measure(lambda: timeline())