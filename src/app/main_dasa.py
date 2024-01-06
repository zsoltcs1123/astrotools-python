from datetime import datetime

import requests
import pytz
from core.positions.position_factory import create_geo_position
from out.file import to_text_file
from tools.dasa.dasa import Dasa, DasaLevel
from tools.dasa.dasa_factory import generate_dasas
from tools.dasa.dasa_printer import print_dasas
from core.objects.points import MOON
from core.zodiac.positions.mapped_geo_position import MappedGeoPosition


def get_coin_dasa(symbol: str):
    response = requests.get(f"http://localhost:8001/birthdate?symbol={symbol}")
    birth_date = response.json()["birth_date"]

    if birth_date is None:
        return

    birth_date = datetime.strptime(birth_date, "%Y-%m-%dT%H:%M:%S%z").astimezone(
        pytz.utc
    )

    moon_position = create_geo_position(MOON, birth_date)
    moon_mapped = MappedGeoPosition(moon_position)
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
    dasa_str += f"Moon longitude: {moon_mapped.sidereal.lon}\n"
    dasa_str += f"Moon position: {moon_mapped.sidereal.position}\n"
    dasa_str += f"Moon Nakshatra: {moon_mapped.sidereal.nakshatra.name}\n"
    dasa_str += f"Moon Nakshatra ruler: {moon_mapped.sidereal.nakshatra.ruler}\n"
    dasa_str += f"Current Maha dasa: {current_maha_dasa}\n"
    dasa_str += "\n"

    dasa_str += print_dasas(current_bhukti)

    to_text_file(f"dasa_{symbol}.txt", dasa_str)


if __name__ == "__main__":
    for symbol in [
        "aix",
        "cre",
        "hot",
        "olas",
        "unibot",
        "xgpt",
        "wik",
        "trendx",
    ]:
        print(f"Getting dasa for {symbol}")
        get_coin_dasa(symbol)
