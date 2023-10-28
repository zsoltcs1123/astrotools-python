from zodiac.degree_converter import float_to_zodiacal
from zodiac.horoscope import Horoscope


class HoroscopePrinter:
    def __init__(self, horoscope: Horoscope):
        self.horoscope = horoscope

    def print_to_console(self):
        print(f"Name: {self.horoscope.name}")
        print(f"Date and Time: {self.horoscope.dt}")
        print(f"Longitude: {self.horoscope.lon}")
        print(f"Latitude: {self.horoscope.lat}")
        print(f"House System: {self.horoscope.house_system}")
        print(f"Zodiac System: {self.horoscope.zodiac_system}")
        print(f"Coordinate System: {self.horoscope.coord_system}")

        print("\nPoints:")
        print("--------")
        print("Name\t\tDegrees\tHouse\tTerm\tTarot")
        for point in self.horoscope.points:
            print(f"{point.position.planet}\t{(' R' if point.retrograde else '')}\t{float_to_zodiacal(point.position.lon)}\t{point.house(self.horoscope.cusps)}\t{point.term.name}\t{point.decan.name}")

        print("\nAspects:")
        print("--------")
        for asp in self.horoscope.aspects:
            print(f"{asp.angle.print_no_time()}, {asp.asp_str}")

    def print_to_markdown(self, filename: str):
        with open(filename, 'w') as f:
            f.write(f"## Name: {self.horoscope.name}\n")
            f.write(f"## Date and Time: {self.horoscope.dt}\n")
            f.write(f"## Longitude: {self.horoscope.lon}\n")
            f.write(f"## Latitude: {self.horoscope.lat}\n")
            f.write(f"## House System: {self.horoscope.house_system}\n")
            f.write(f"## Zodiac System: {self.horoscope.zodiac_system}\n")
            f.write(f"## Coordinate System: {self.horoscope.coord_system}\n")

            f.write("\n### Points:\n")
            f.write("--------\n")
            f.write("| Name | Degrees | House | Term | Tarot |\n")
            f.write("| --- | --- | --- | --- | --- |\n")
            for point in self.horoscope.points:
                f.write(f"| {point.position.planet} {('R' if point.retrograde else '')} | {float_to_zodiacal(point.position.lon)} | {point.house(self.horoscope.cusps)} | {point.term.name} | {point.decan.name} |\n")

            f.write("\n### Aspects:\n")
            f.write("--------\n")
            for asp in self.horoscope.aspects:
                f.write(f"- {asp.angle.print_no_time()}, {asp.asp_str}\n")

