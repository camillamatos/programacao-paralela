import multiprocessing
import time
import random
import matplotlib.pyplot as plt
import math
import numpy as np

def createCircle(x, y, color):
  fig, ax = plt.subplots()
  ax.plot(x, y, marker='.', ls='', color=color )
  plt.axis('square')
  plt.show

def createPoints(total_points, worker_id):
  inside_qnt = 0
  inside = []
  np.random.seed(worker_id)

  for i in range(total_points):
    x = np.random.uniform(-1, 1)
    y = np.random.uniform(-1, 1)

    if np.sqrt(x**2 + y**2) < 1:
        inside.append((x, y))
        inside_qnt += 1
  
  return [inside_qnt, total_points, inside]

def worker(worker_id, return_dict, total_points ):
    pi = createPoints(total_points, worker_id);
    print("Task " + str(worker_id) + ": " + str(pi[0]) + " pontos dentro do circulo")
    return_dict[worker_id] = pi


manager = multiprocessing.Manager()
return_dict = manager.dict()
jobs = []
num_tasks = 5
num_points = 500000

for i in range(num_tasks):
    p = multiprocessing.Process(target=worker, args=(i, return_dict, num_points))
    jobs.append(p)
    p.start()

for proc in jobs:
    proc.join()

circle_count = 0
total_points = 0
circle_complete = []
fig, ax = plt.subplots()

colors = ['red', 'blue', 'green', 'black', 'yellow']
j = 0

for points in return_dict.values():
    circle_count += points[0]
    total_points += points[1]
    newInside = points[2]
    createCircle([x[0] for x in newInside], [x[1] for x in newInside], colors[j])
    ax.plot([x[0] for x in newInside], [x[1] for x in newInside], marker='.', ls='', color=colors[j])
    j+= 1

plt.show
pi_estimate = 4.0 * float(circle_count)/total_points

print("\nValor estimado do PI :", pi_estimate)
print("Taxa de erro:", abs(pi_estimate-math.pi))