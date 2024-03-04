import time
from typing import Any, Callable, Dict, List

import pytz

from astrotoolz.core.units.degree import Degree
from astrotoolz.core.units.degree_converter import degree_from_decimal


def measure(func) -> None:
    start_time = time.time()
    func()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")


def integral_ends_with(end: int, num: float) -> bool:
    return str(num).split(".")[0][-1] == str(end)


def decimal_ends_with(end: int, num: float) -> bool:
    return str(num).split(".")[1][-1] == str(end)


def group_by(lst: List[Any], key_func: Callable[[Any], Any]) -> Dict[Any, List[Any]]:
    result: Dict[Any, List[Any]] = {}
    for item in lst:
        key = key_func(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result


def to_degree(*args: float) -> List[Degree]:
    return [degree_from_decimal(arg) for arg in args]


def find_smallest_elements(
    d: Dict[Any, List[Any]], key_func: Callable[[Any], float]
) -> Dict[Any, Any]:
    return {k: min(v, key=key_func) for k, v in d.items()}


def get_utc_datetime(local_dt, timezone_str):
    timezone = pytz.timezone(timezone_str)
    local_dt = timezone.localize(local_dt)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt
