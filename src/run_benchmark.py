import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
import csv
from time import time
from utils.instance_loader import load_low_dimensional, load_large_scale
from algorithms.branch_and_bound import solve_branch_and_bound
from algorithms.fptas import solve_fptas
from algorithms.two_approx import solve_two_approx
from functools import partial

ALGORITHMS = {
  'bnb': solve_branch_and_bound,
  'fptas_05': partial(solve_fptas, epsilon=0.5),
  'fptas_01': partial(solve_fptas, epsilon=0.1),
  'fptas_001': partial(solve_fptas, epsilon=0.01),
  'fptas_0001': partial(solve_fptas, epsilon=0.001),
  '2approx': solve_two_approx,
}

RESULTS_PATH = "benchmarks/results.csv"
INSTANCES_PATH = "instances/"
TIME_LIMIT = 30*60

def load_cache(path):
  if not os.path.exists(path):
    return set(), []
  
  rows = []
  cache_keys = set()

  with open(path, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
      key = (row["instance"], row["type"], row["algorithm"])
      cache_keys.add(key)
      rows.append(row)
  return cache_keys, rows

def run_all():
  os.makedirs("benchmarks", exist_ok=True)
  
  cache_keys, cached_rows = load_cache(RESULTS_PATH)
  new_rows = []

  files = os.listdir(INSTANCES_PATH)

  # LOW-DIMENSIONAL
  for file in files:
    if file.endswith(".kp"):
      path = os.path.join(INSTANCES_PATH, file)
      try:
        values, weights, capacity = load_low_dimensional(path)
        for algo_name, algo_fn in ALGORITHMS.items():
          key = (file, "low", algo_name)
          if key in cache_keys:
            print(f"[SKIP] {key}")
            continue

          print(f"[LOW] {file} - {algo_name}")
          result = algo_fn(values, weights, capacity, TIME_LIMIT)
          new_rows.append({
            "instance": file, 
            "type": "low", 
            "algorithm": algo_name,
            "n_items": len(values), 
            "capacity": capacity,
            "value": result['value'], 
            "time_sec": result['time_sec'], 
            "memory_mb": result['memory_mb'], 
            "status": result['status']
          })
      except Exception as e:
        print(f"Error in {file}: {e}")
  
  # LARGE-SCALE
  info_files = [f for f in files if f.endswith("_info.csv")]
  items_files = [f for f in files if f.endswith("_items.csv")]

  paired = [(info, item) for info in info_files for item in items_files 
            if info.replace("_info.csv", "") == item.replace("_items.csv", "")]

  for info_file, item_file in paired:
    base = info_file.replace("_info.csv", "")
    info_path = os.path.join(INSTANCES_PATH, info_file)
    item_path = os.path.join(INSTANCES_PATH, item_file)
    try:
      values, weights, capacity = load_large_scale(info_path, item_path)
      for algo_name, algo_fn in ALGORITHMS.items():
        key = (base, "large", algo_name)
        if key in cache_keys:
          print(f"[SKIP] {key}")
          continue

        print(f"[LARGE] {base} - {algo_name}")
        result = algo_fn(values, weights, capacity, TIME_LIMIT)
        new_rows.append({
            "instance": base, 
            "type": "large", 
            "algorithm": algo_name,
            "n_items": len(values), 
            "capacity": capacity,
            "value": result['value'], 
            "time_sec": result['time_sec'], 
            "memory_mb": result['memory_mb'], 
            "status": result['status']
          })
    except Exception as e:
      print(f"Error in {base}: {e}")
  
  # 3. Save CSV
  with open(RESULTS_PATH, 'w', newline='') as f:
    fieldnames = ["instance", "type", "algorithm", "n_items", "capacity", "value", "time_sec", "memory_mb", "status"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cached_rows)
    writer.writerows(new_rows)
  
  print(f"\nResults saved in {RESULTS_PATH}")

if __name__ == "__main__":
  run_all()