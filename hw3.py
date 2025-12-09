import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import perf_counter

# Параметри задачі
MAX_N = 10_000_000 
NUM_THREADS = os.cpu_count() or 4  
CHUNK_SIZE = 50_000      


def collatz_steps(n: int) -> int:
    steps = 0
    while n != 1:
        if n & 1:       
            n = 3 * n + 1
        else:           
            n //= 2
        steps += 1
    return steps


def process_chunk(start: int, end: int) -> int:
    total = 0
    for x in range(start, end):
        total += collatz_steps(x)
    return total


def chunk_ranges(start: int, stop: int, chunk_size: int):
    """
    Генерує пари (start, end) для чанків у діапазоні [start, stop).
    """
    current = start
    while current < stop:
        nxt = min(current + chunk_size, stop)
        yield current, nxt
        current = nxt


def main():
    print(f"Обчислення кількості кроків Колатца для чисел 1..{MAX_N}")
    print(f"Кількість потоків: {NUM_THREADS}, розмір чанка: {CHUNK_SIZE}")

    t0 = perf_counter()

    total_steps = 0
    tasks = []

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        for start, end in chunk_ranges(1, MAX_N + 1, CHUNK_SIZE):
            future = executor.submit(process_chunk, start, end)
            tasks.append(future)

        for future in as_completed(tasks):
            total_steps += future.result()

    t1 = perf_counter()

    avg_steps = total_steps / MAX_N

    print(f"Сумарна кількість кроків: {total_steps}")
    print(f"Середня кількість кроків: {avg_steps:.4f}")
    print(f"Час виконання: {t1 - t0:.2f} секунд")


if __name__ == "__main__":
    main()
