from core.util import measure
from datetime import datetime
from core.planetary_position import get_planetary_positions


def main():
    start_time = datetime(2023, 9, 1)
    end_time = datetime(2023, 9, 30)
    positions = get_planetary_positions('mars', start_time, end_time, 1440)

    for p in positions:
        print(p)

if __name__ == "__main__":
    #measure(lambda: main())
    

