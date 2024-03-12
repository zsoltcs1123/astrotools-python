from datetime import datetime

import pytz
import requests

from astrotoolz.core.enums import NodeCalc, Zodiac
from astrotoolz.core.points import MOON
from astrotoolz.core.positions.factory.geo_factory import GeoFactory
from astrotoolz.core.zodiac.mapper.position_mapper import PositionMapper
from astrotoolz.out.file import to_text_file
from astrotoolz.tools.dasa.dasa import DasaLevel
from astrotoolz.tools.dasa.dasa_factory import generate_dasas
from astrotoolz.tools.dasa.dasa_printer import print_dasas


def get_coin_dasa(symbol: str):
    response = requests.get(
        "http://localhost:8001/birthdate?contract_address=0x6c6ee5e31d828de241282b9606c8e98ea48526e2"
    )
    birth_date = response.json()["birth_date"]

    if birth_date is None:
        return

    birth_date = datetime.strptime(birth_date, "%Y-%m-%dT%H:%M:%S%z").astimezone(
        pytz.utc
    )

    position_factory = GeoFactory(NodeCalc.MEAN)
    position_mapper = PositionMapper()
    moon_position = position_factory.create_position(MOON, birth_date)
    moon_mapped = position_mapper.map_position(moon_position, [Zodiac.SIDEREAL])

    res = generate_dasas(moon_mapped, DasaLevel.Pratyantar)

    current_date = datetime.now().astimezone(pytz.utc)
    current_maha_dasa = [d for d in res if d.start_date <= current_date <= d.end_date][
        0
    ]
    current_bhukti = [
        d
        for d in current_maha_dasa.sub_dasas
        if d.start_date <= current_date <= d.end_date
    ]

    dasa_str = ""
    dasa_str += f"Coin: {symbol}\n"
    dasa_str += f"Birth date: {birth_date}\n"
    dasa_str += f"Moon longitude: {moon_mapped.vedic.lon}\n"
    dasa_str += f"Moon position: {moon_mapped.vedic.zodiacal_position}\n"
    dasa_str += f"Moon Nakshatra: {moon_mapped.vedic.nakshatra.name}\n"
    dasa_str += f"Moon Nakshatra ruler: {moon_mapped.vedic.nakshatra.ruler}\n"
    dasa_str += f"Current Maha dasa: {current_maha_dasa}\n"
    dasa_str += "\n"

    dasa_str += print_dasas(current_bhukti)

    to_text_file(f"dasa_{symbol}.txt", dasa_str)


if __name__ == "__main__":
    print("Getting dasa for HOT")
    get_coin_dasa("HOT")
