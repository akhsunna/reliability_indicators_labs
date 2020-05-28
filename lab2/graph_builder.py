import networkx as nx
import matplotlib.pyplot as plt

NODE_COLOR = {'true': 'green', 'false': 'pink'}

class GraphBuilder:
  def __init__(self, nodes):
    self.nodes = nodes

  def call(self):
    DG=nx.OrderedDiGraph()

    edge_labels = self.get_edge_labels()
    edge_colors = self.get_edge_colors()

    levels = {}
    for n in self.nodes:

      if n.state():
        color = '#9bba5e' if n.first_fixed else '#5eba7d'
      else:
        color = '#d0d0d0'
      DG.add_node(n.pi, label=n.s_binary(), color=color)
      if n.level() in levels:
        levels[n.level()] = levels[n.level()] + 1
      else:
        levels[n.level()] = 1
      for p in list(n.elements.keys()):
        if n.pi != p:
          DG.add_edge(p, n.pi)

    node_positions = {}
    tmp = levels.copy()
    for n in self.nodes:
      l = n.level()
      st = - 50 * l
      sp = (400 + l * 100)/(levels[l] + 1)
      node_positions[n.pi] = (sp * (levels[l] - tmp[l] + 1) + st, -50 * l)
      tmp[l] = tmp[l] - 1

    colors = list(map(lambda n: n[1]['color'], DG.nodes(data=True)))
    labels = {node[0]:node[1]['label'] for node in DG.nodes(data=True)}

    edge_colors_ord = list(map(lambda e: edge_colors[e[0], e[1]], DG.edges(data=True)))

    plt.figure(figsize=(10,8)) 
    nx.draw(DG, connectionstyle='arc3, rad = 0.03', node_size=600, node_color=colors, pos=node_positions, prog='dot', labels=labels, edge_color=edge_colors_ord, font_size=7)
    nx.draw_networkx_edge_labels(DG,node_positions,edge_labels=edge_labels,font_size=6,label_pos=0.25)

#     plt.axis('off')
    plt.show()

  def get_edge_labels(self):
    arr = {}
    for n in self.nodes:
      for p in list(n.elements.keys()):
        if n.pi != p:
          i = n.elements[p][0]
          str = ''
          if i > 4:
            str = 'm{}'.format(i - 4)
          else:
            str = 'a{}'.format(i + 1)
          arr[p, n.pi] = str
    return arr

  def get_edge_colors(self):
    arr = {}
    for n in self.nodes:
      for p in list(n.elements.keys()):
        if n.pi != p:
          color = 'black'
          if n.elements[p][0] > 4:
            color = 'red'
          arr[p, n.pi] = color
    return arr



