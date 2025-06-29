import time
import tracemalloc

def solve_fptas(values, weights, capacity, time_limit_sec, epsilon=0.1):
  start = time.perf_counter()
  tracemalloc.start()

  n = len(values)
  vmax = max(values)
  mu = epsilon * vmax / n

  # Step 1: Scale the values
  scaled_values = [int(v // mu) for v in values]

  # Step 2: Dynamic programming by value
  V = sum(scaled_values)
  INF = float('inf')
  dp = [INF] * (V + 1)
  dp[0] = 0

  for i in range(n):
    vi = scaled_values[i]
    wi = weights[i]
    for x in range(V, vi - 1, -1):
      if time_limit_sec and (time.perf_counter() - start) > time_limit_sec:
        tracemalloc.stop()
        return {
          "value": None,
          "time_sec": round(time.perf_counter() - start, 4),
          "memory_mb": None,
          "status": "TIMEOUT"
        }
      if dp[x - vi] + wi <= capacity:
        dp[x] = min(dp[x], dp[x - vi] + wi)

  # Step 3: Find biggest viable value
  for v in range(V, -1, -1):
    if dp[v] <= capacity:
      approx_value = int(v * mu)
      break
  else:
    approx_value = 0
  
  current, peak = tracemalloc.get_traced_memory()
  tracemalloc.stop()
  end = time.perf_counter()

  return {
    "value": approx_value,
    "time_sec": round(end - start, 4),
    "memory_mb": round(peak / 1024 / 1024, 4),
    "status": "OK"
  }