import os
from datetime import datetime
import numpy as np
from scipy.integrate import RK45
import pandas as pd


class Solver:
  def export_solution(self, matrix, n):
    t0 = 0
    y0 = 1.0 / n
    y = np.repeat(y0, 29)
    def multiply_vector(t, y):
      return np.array(matrix).dot(y)
    rk = RK45(multiply_vector, t0, y, 10000, vectorized=True)
    self.folder_name = datetime.now().strftime('%Y%m%d%H%M%S')
    os.mkdir('result/{}'.format(self.folder_name))
    for i in range(10):
      res = rk.y
      df = pd.DataFrame(res)
      filename = './result/{}/step_{}.csv'.format(self.folder_name, i)
      df.to_csv (filename, index=True, header=False)
      rk.step()


