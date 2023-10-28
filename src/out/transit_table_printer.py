import pandas as pd
import numpy as np

from tools.transit_table import TransitTable

class TransitTablePrinter:
    def __init__(self, transit_table: TransitTable):
        self.transit_table = transit_table

    def print_to_console(self):
        # Extract diff from Angle objects and create DataFrame
        planets = list(self.transit_table.angles.keys())
        matrix = np.empty((len(planets), len(planets)), dtype=object)
        for i, planet1 in enumerate(planets):
            for j, planet2 in enumerate(planets):
                # Find the corresponding Angle or Aspect object
                angle = next((angle for angle in self.transit_table.angles[planet1] if angle.pos2.point == planet2), None)
                matrix[i, j] = round(angle.diff,3) if angle else ''
        angles_df = pd.DataFrame(matrix, index=planets, columns=planets)
        print("Angles:")
        print("-------")
        print(angles_df)

        # Extract asp_diff from Aspect objects and create DataFrame
        matrix = np.empty((len(planets), len(planets)), dtype=object)
        for i, planet1 in enumerate(planets):
            for j, planet2 in enumerate(planets):
                # Find the corresponding Angle or Aspect object
                aspect = next((aspect for aspect in self.transit_table.aspects[planet1] if aspect.angle.pos2.point == planet2), None)
                matrix[i, j] = round(aspect.asp_diff,3) if aspect else ''
        aspects_df = pd.DataFrame(matrix, index=planets, columns=planets)
        print("\nAspects:")
        print("--------")
        print(aspects_df)