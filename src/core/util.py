import time


def measure(func) -> None:
    start_time = time.time()
    func()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
