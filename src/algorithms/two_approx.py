import time
import tracemalloc

def solve_two_approx(values, weights, capacity, time_limit_sec):
  start = time.perf_counter()
  tracemalloc.start()

  n = len(values)

  # 1. Best isolated item that fits
  best_single = 0
  for i in range(n):
    if time_limit_sec and (time.perf_counter() - start) > time_limit_sec:
      tracemalloc.stop()
      return {
        "value": None,
        "time_sec": round(time.perf_counter() - start, 4),
        "memory_mb": None,
        "status": "TIMEOUT"
      }
    if weights[i] <= capacity:
      best_single = max(best_single, values[i])

  # 2. Greedy by value/weight
  items = sorted(zip(values, weights), key=lambda x: x[0] / x[1], reverse=True)
  total_weight = 0
  total_value = 0
  for v, w in items:
    if time_limit_sec and (time.perf_counter() - start) > time_limit_sec:
      tracemalloc.stop()
      return {
        "value": None,
        "time_sec": round(time.perf_counter() - start, 4),
        "memory_mb": None,
        "status": "TIMEOUT"
      }
    if total_weight + w <= capacity:
      total_weight += w
      total_value += v
  
  best_solution = max(best_single, total_value)

  current, peak = tracemalloc.get_traced_memory()
  tracemalloc.stop()
  end = time.perf_counter()

  return {
    "value": best_solution,
    "time_sec": (end - start),
    "memory_mb": round(peak / 1024 / 1024, 4),
    "status": "OK"
  }