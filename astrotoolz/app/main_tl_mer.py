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

from astrotoolz.core.enums import CoordinateSystem
from astrotoolz.core.events.astro_event import (
    DeclinationExtreme,
    LatitudeExtreme,
    SpeedExtreme,
)
from astrotoolz.core.positions.geo_position import GeoPosition
from astrotoolz.core.zodiac.division import Division
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
        datetime(2023, 1, 1),
        datetime(2024, 1, 1),
        10,
        ["mercury"],
        events=[DeclinationExtreme],
    )

    factory = build_timeline_factory(cfg)

    timeline = factory.create_timeline(cfg)

    timeline_json = json.dumps(timeline, cls=CustomJSONEncoder)

    to_text_file(
        "json.txt",
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

        if isinstance(obj, GeoPosition):
            return {
                "lon": obj.lon.decimal,
                "lat": obj.lat.decimal,
                "speed": obj.speed.decimal,
                "ra": obj.ra.decimal,
                "dec": obj.dec.decimal,
            }

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
