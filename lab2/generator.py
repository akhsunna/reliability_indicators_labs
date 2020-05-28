from node import Node
import numpy as np

class Generator:
  def init_nodes(self):
    node = Node(0,'11111')
    self.nodes = [node]
    self.generate_nodes(node, False)

  def generate_nodes(self,p_node,is_first_fixed):
    for i in range(5):
      if not p_node.new_child(i):
        continue

      new_binary = p_node.new_binary(i)

      node = None
      filtered = list(filter(lambda n: n.binary == new_binary and n.first_fixed == is_first_fixed, self.nodes))
      if len(filtered) > 0:
        node = filtered[0]

      is_new_node = False
      if not node:
        node = Node(len(self.nodes), new_binary, first_fixed=is_first_fixed)
#         print(node.s_binary())
        self.nodes.append(node)
        is_new_node = True
      node.add_element(i, p_node.pi) 
      p_node.add_element(i, p_node.pi)

      if is_new_node:
        if node.state():
          self.generate_nodes(node,is_first_fixed)

      if i != 0:
        node.add_element(i, node.pi, mu=True)
        p_node.add_element(i, node.pi, mu=True)
      elif not is_first_fixed:
        self.fix_first(node)

  def fix_first(self, p_node):
    i = 0
    new_binary = p_node.new_binary(i,one=True)

    print('fix first', p_node.binary, new_binary)

    node = None
    filtered = list(filter(lambda n: n.binary == new_binary and n.first_fixed, self.nodes))
    if len(filtered) > 0:
      node = filtered[0]

    is_new_node = False
    if not node:
      node = Node(len(self.nodes), new_binary, first_fixed=True)
#       print(node.s_binary())
      self.nodes.append(node)
      is_new_node = True

    p_node.add_element(i, p_node.pi, mu=True)
    node.add_element(i, p_node.pi, mu=True)

    if is_new_node:
      self.generate_nodes(node,True)

  def get_matrix(self, a):
    self.matrix = []
    for n in self.nodes:
      self.matrix.append(n.matrix_row(a, len(self.nodes)))
    return self.matrix

  def get_eqs(self):
    return map(lambda n: n.eq_str(), self.nodes)

  def true_nodes(self):
    return list(filter(lambda n: n.state(), self.nodes))
