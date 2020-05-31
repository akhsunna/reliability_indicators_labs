from generator import Generator
from solver import Solver
from graph_builder import GraphBuilder
from node import Node

import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt

alphas = [0.0005, 0.0004, 0.0003, 0.00025, 0.0005]

input alpha values
for i, a in enumerate(alphas, start=0):
  v = input('Enter a{} (default {}): '.format(i + 1, a))
  if v:
    alphas[i] = float(v)

module_i = input('Enter the number of the module to investigate: ')
if module_i:
  module_i = int(module_i) - 1

# init states
g = Generator()
g.init_nodes()
# show graph with states
b = GraphBuilder(g.nodes)
b.call()
# show system of equations
print('\n'.join(list(g.get_eqs())))

matrix = g.get_matrix(alphas)

s = Solver(matrix, len(g.nodes))

# show results in graphic
s.ps_state(10)

# show reliability rate graphic
# s.reliability(10, list(map(lambda n: n.pi, g.true_nodes())))

if module_i:
  diff = -0.0002
  input = alphas[module_i]
  labels = []
  for i in range(6):
    alphas[module_i] = input + diff
    labels.append('a{} = {}'.format(module_i, alphas[module_i]))
    matrix = g.get_matrix(alphas)
    s = Solver(matrix, len(g.nodes))
    arr = s.get_solutions(10, list(map(lambda n: n.pi, g.true_nodes())))
    plt.plot(arr[0], arr[1])
    diff = diff + 0.0001
  plt.legend(labels)
  plt.grid(True)
  plt.show()
