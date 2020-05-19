from generator import Generator
from solver import Solver
from graph_builder import GraphBuilder
from node import Node


a = [0.0005, 0.0004, 0.0003, 0.00025, 0.0005]

g = Generator()
g.init_nodes()
matrix = g.get_matrix(a)

s = Solver()
s.export_solution(matrix, 29)

b = GraphBuilder(g.nodes)
b.call()



