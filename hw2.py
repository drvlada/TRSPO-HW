import threading
import multiprocessing as mp
import random
import time

# === ФУНКЦІЯ ДЛЯ ОБЧИСЛЕННЯ  ===
def monte_carlo_pi_part(points):
    inside_circle = 0
    for _ in range(points):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:
            inside_circle += 1
    return inside_circle

# === THREADING ===
def monte_carlo_pi_threads(total_points, num_threads):
    points_per_thread = total_points // num_threads
    threads = []
    results = [0] * num_threads

    def worker(i):
        results[i] = monte_carlo_pi_part(points_per_thread)

    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total_inside = sum(results)
    return 4 * total_inside / total_points

# === MULTIPROCESSING ===
def monte_carlo_pi_processes(total_points, num_procs):
    points_per_proc = total_points // num_procs
    with mp.Pool(processes=num_procs) as pool:
        results = pool.map(monte_carlo_pi_part, [points_per_proc] * num_procs)
    total_inside = sum(results)
    return 4 * total_inside / total_points


if __name__ == "__main__":
    total_points = 1_000_000
    workers = [1, 2, 4, 8, 16, 32, 64]

    print(f"{'Workers':<8} | {'Threads π':<12} | {'Time':<8} | {'Proc π':<12} | {'Time':<8}")
    print("-" * 60)

    for n in workers:
        # Threads
        start = time.time()
        pi_threads = monte_carlo_pi_threads(total_points, n)
        t_time = time.time() - start

        # Processes
        start = time.time()
        pi_procs = monte_carlo_pi_processes(total_points, n)
        p_time = time.time() - start

        print(f"{n:<8} | {pi_threads:<12.6f} | {t_time:<8.4f} | {pi_procs:<12.6f} | {p_time:<8.4f}")



  #Результати
  #Workers | Threads π | Time   | Proc π   | Time
  #------------------------------------------------------------ 
  #1       | 3.142124  | 0.1641 | 3.141580 | 0.2880 
  #2       | 3.141292  | 0.1514 | 3.141076 | 0.1806 
  #4       | 3.145720  | 0.1558 | 3.141116 | 0.1805 
  #8       | 3.139364  | 0.1501 | 3.143296 | 0.2602 
  #16      | 3.141364  | 0.2290 | 3.140892 | 0.4213 
  #32      | 3.144536  | 0.2139 | 3.144160 | 0.5223 
  #64      | 3.139572  | 0.1797 | 3.142528 | 0.7269

  #Threading для обчислювальних задач не дає виграшу через GIL. Час роботи не зменшується, навіть навпаки, трохи зростає при великій кількості потоків.
  #За допомогою multiprocessing прискорення можливе лише до кількості процесів, кількості фізичних ядер CPU. Далі накладні витрати на створення та координацію процесів роблять програму повільнішою.
