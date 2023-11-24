from typing import List

from tools.dasa.dasa import Dasa


def print_dasas(dasas: List[Dasa], level: int = 0):
    for dasa in dasas:
        print(
            "  " * level
            + f"{dasa.level.name}: {dasa.planet}, start: {dasa.start_date.strftime('%b %d, %Y')}, end: {dasa.end_date.strftime('%b %d, %Y')}"
        )
        print_dasas(dasa.sub_dasas, level + 1)
