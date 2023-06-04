from typing import Dict, List, Any, Callable
import time
from typing import List
from typing import Any, Callable, Dict, List


def measure(func) -> None:
    start_time = time.time()
    func()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")


def ends_with(end: int, num: float) -> bool:
    return str(num).split('.')[0][-1] == str(end)


def group_by(lst: List[Any], key_func: Callable[[Any], Any]) -> Dict[Any, List[Any]]:
    result = {}
    for item in lst:
        key = key_func(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result


def find_smallest_elements(d: Dict[Any, List[Any]], key_func: Callable[[Any], float]) -> Dict[Any, Any]:
    return {k: min(v, key=key_func) for k, v in d.items()}
