from typing import Dict, List

from aspects.aspectgen import Aspect
from price import Price


def aspect_map_to_markdown(aspect_map: Dict[Aspect, List[Price]]) -> str:
    for aspect, prices in aspect_map.items():
        # Define the header row
        header = f'{aspect.__repr__()}\n'
        p1 = aspect.angle.pos1.planet
        p2 = aspect.angle.pos2.planet
        asp_str = f'{p1} {aspect.asp_str} {p2}'

        separator = '-------------------\n'

        table = f"| {p1} | {p2} | {asp_str} |\n"
        table += "|-----|-------|-----------------|\n"

        for row in zip(prices[0], prices[1], prices[2]):
            table += "|"
            for price in row:
                table += f" **{price.level}** |" if price.harmonic == 0 else \
                    f" *{price.level}* |" if price.harmonic == 3 else \
                    f" {price.level} |"
            table += "\n"

    return header + separator + table


def to_md_file(aspect_map: Dict[Aspect, List[Price]], file_name: str) -> None:
    text = aspect_map_to_markdown(aspect_map)

    with open(file_name, 'w') as f:
        f.write(text)
