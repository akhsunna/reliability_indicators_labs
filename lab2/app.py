from generator import Generator
from solver import Solver
from graph_builder import GraphBuilder
from node import Node

alphas = [0.0005, 0.0004, 0.0003, 0.00025, 0.0005]
mus = list(map(lambda x: x * 30, alphas))

# init states & matrix
g = Generator()
g.init_nodes()
print(len(g.nodes))
matrix = g.get_matrix(alphas + mus)

# show graph with states
b = GraphBuilder(g.nodes)
b.call()

# show system of equations
print('\n'.join(list(g.get_eqs())))

s = Solver(matrix, len(g.nodes))

# export results to csv
# s.export_solution()

# show results in graphic
# s.ps_state(10)

# show reliability rate graphic
s.reliability(10, list(map(lambda n: n.pi, g.true_nodes())))
