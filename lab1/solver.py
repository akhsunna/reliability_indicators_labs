import os
from datetime import datetime
import numpy as np
from scipy.integrate import RK45
import pandas as pd


import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt


class Solver:
  def __init__(self, matrix, n):
    self.matrix = matrix
    self.n = n

  def multiply_vector(self, t, y):
      return np.array(self.matrix).dot(y)

  def export_solution(self):
    t0 = 0
    y0 = 1.0 / self.n
    y = np.repeat(y0, self.n)
    rk = RK45(self.multiply_vector, t0, y, 10000, vectorized=True)
    self.folder_name = datetime.now().strftime('%Y%m%d%H%M%S')
    os.mkdir('result/{}'.format(self.folder_name))
    for i in range(10):
      res = rk.y
      res = res / np.linalg.norm(res, ord=1)
      df = pd.DataFrame(res)
      filename = './result/{}/step_{}.csv'.format(self.folder_name, i)
      df.to_csv (filename, index=True, header=False)
      rk.step()

  def ps_state(self, step_n):
    t0 = 0
    y0 = 1.0 / self.n
    y = np.repeat(y0, self.n)
    rk = RK45(self.multiply_vector, t0, y, 10000, vectorized=True)
    for i in range(step_n):
      rk.step()
    res = rk.y
    res = res / np.linalg.norm(res, ord=1)
    ps = list(map(lambda x: 'P{}'.format(x), list(range(self.n))))
    plt.bar(ps, res, align='center',width = 0.5)
    plt.show()

  def reliability(self, step_n, pis):
    t0 = 0
    y0 = 1.0 / self.n
    y = np.repeat(y0, self.n)
    rk = RK45(self.multiply_vector, t0, y, 10000, vectorized=True)
    y_res = []
    x_res = []
    for i in range(step_n):
      sum = 0
      rk.step()
      res = rk.y
      res = res / np.linalg.norm(res, ord=1)
      for i, r in enumerate(res, start=0):
        if i in pis:
          sum = sum + r
      y_res.append(sum)
      x_res.append(rk.t)
    plt.plot(x_res, y_res)
    plt.grid(True)
    plt.show()
