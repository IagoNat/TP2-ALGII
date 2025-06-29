import heapq
import time
import tracemalloc

def solve_branch_and_bound(values, weights, capacity, time_limit_sec):
  """
  Resolve o problema da mochila 0-1 usando branch-and-bound.

  Args:
    values (List[int]): lista de valores dos itens.
    weights (List[int]): lista de pesos dos itens.
    capacity (int): capacidade máxima da mochila.
    time_limit_sec (float, opcional): tempo máximo de execução.

  Returns:
    dict: {
      'value': valor total obtido,
      'time_sec': tempo em segundos,
      'memory_mb': memória usada em MB,
      'status': 'OK' ou 'TIMEOUT'
    }
  """
  start = time.perf_counter()
  tracemalloc.start()

  class Node:
    def __init__(self, level, value, weight, bound):
      self.level = level    # Index of the item considered    
      self.value = value    # Accumulated value
      self.weight = weight  # Accumulated weight
      self.bound = bound    # Superior estimatior of value
    
    def __lt__(self, other):
      return self.bound > other.bound # Prioritize biggest bound
    
    
  n = len(values)

  def bound(u):
    if u.weight >= capacity:
      return 0
    
    profit_bound = u.value
    j = u.level + 1
    totweight = u.weight

    while j < n and totweight + weights[j] <= capacity:
      totweight += weights[j]
      profit_bound += values[j]
      j += 1
    if j < n:
      profit_bound += (capacity - totweight) * (values[j] / weights[j])
    return profit_bound
  
  items = sorted(zip(values, weights), key=lambda x: x[0]/x[1], reverse=True)
  values, weights = zip(*items)

  Q = []
  v = Node(-1, 0, 0, 0)
  v.bound = bound(v)
  max_value = 0
  heapq.heappush(Q, v)

  status = "OK"

  while Q:
    if time_limit_sec and (time.perf_counter() - start) > time_limit_sec:
      status = "TIMEOUT"
      max_value = None
      break

    v = heapq.heappop(Q)
    if v.bound <= max_value:
      continue

    u = Node(v.level + 1, 0, 0, 0)

    # Include item
    u.weight = v.weight + weights[u.level]
    u.value = v.value + values[u.level]
    if u.weight <= capacity and u.value > max_value:
      max_value = u.value
    u.bound = bound(u)
    if u.bound > max_value:
      heapq.heappush(Q, u)
    
    # Exclude item
    u2 = Node(v.level + 1, v.value, v.weight, 0)
    u2.bound = bound(u2)
    if u2.bound > max_value:
      heapq.heappush(Q, u2)
  
  current, peak = tracemalloc.get_traced_memory()
  tracemalloc.stop()
  end = time.perf_counter()

  return {
    "value": max_value,
    "time_sec": round(end-start, 4),
    "memory_mb": round(peak / 1024 / 1024, 4),
    "status": status
  }      
