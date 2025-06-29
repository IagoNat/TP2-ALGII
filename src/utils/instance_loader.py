import csv

def load_low_dimensional(filepath):
  """
  Reads an instance of format Unicauca (.kp)
  Returns: values, weights, capacity
  """
  with open(filepath, 'r') as f:
    lines = f.readlines()

  n, capacity = map(float, lines[0].split())
  n = int(n)
  values = []
  weights = []

  for line in lines[1:n+1]:
    v, w = map(float, line.strip().split())
    values.append(v)
    weights.append(w)
  
  return values, weights, capacity

def load_large_scale(info_path, items_path):
  """
  Reads an instance of format Kaggle (2 files .csv)
  Returns: values, weights, capacity
  """
  with open(info_path, 'r') as f:
    reader = csv.reader(f)
    info_lines = list(reader)[:2]
    info = {row[0].strip(): int(row[1].strip()) for row in info_lines}
  capacity = info['c']

  values = []
  weights = []

  with open(items_path, 'r') as f:
    reader = csv.DictReader(f)
    reader.fieldnames = [name.strip() for name in reader.fieldnames]

    for row in reader:
      values.append(int(row['price'].strip()))
      weights.append(int(row['weight'].strip()))
  
  return values, weights, capacity