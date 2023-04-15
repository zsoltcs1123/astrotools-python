from itertools import groupby
from aspects.aspectgen import get_aspects


def get_aspects_best_fit(angles):
    aspects = get_aspects(angles)

    groups = groupby(aspects, key=lambda asp: asp.asp_diff)

    aspects = []

    for key, group in groups:
        min_diff_asp = min(group, key=lambda asp: abs(
            asp.angle.diff - asp.asp_diff))

        aspects.append(min_diff_asp)

    return aspects
