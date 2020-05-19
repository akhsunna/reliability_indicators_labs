from node import Node
import numpy as np

class Generator:
  def init_nodes(self):
    node = Node(0,'11111')
    self.nodes = [node]
    self.generate_nodes(node)

  def generate_nodes(self,p_node):
    ch_nodes = []
    for i in range(5):
      if not p_node.new_child(i):
        continue
      new_binary = p_node.new_binary(i)
      node = None
      filtered = list(filter(lambda n: n.binary == new_binary, self.nodes))
      if len(filtered) > 0:
        node = filtered[0]
      
      if not node:
        node = Node(len(self.nodes), new_binary)
        self.nodes.append(node)
      node.add_element(i, p_node.pi) 
      p_node.add_element(i, p_node.pi)
      if node.state():
        ch_nodes.append(node)
    
    for n in ch_nodes:
      self.generate_nodes(n)

  def get_matrix(self, a):
    self.matrix = []
    for n in self.nodes:
      self.matrix.append(n.matrix_row(a))
    return self.matrix


          















