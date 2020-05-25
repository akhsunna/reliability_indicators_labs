import networkx as nx
import matplotlib.pyplot as plt

NODE_COLOR = {'true': 'green', 'false': 'pink'}

class GraphBuilder:
  def __init__(self, nodes):
    self.nodes = nodes

  def call(self):
    DG=nx.OrderedDiGraph()

    edge_labels = self.get_edge_labels()

    levels = {}
    for n in self.nodes:
      color = '#5eba7d' if n.state() else '#d0d0d0'
      DG.add_node(n.pi,label=n.pi,color=color)
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
      node_positions[n.pi] = (sp * (levels[l] - tmp[l] + 1) + st, -10 * l)
      tmp[l] = tmp[l] - 1

    colors = list(map(lambda n: n[1]['color'], DG.nodes(data=True)))
    labels = {node[0]:node[1]['label'] for node in DG.nodes(data=True)}

    plt.figure(figsize=(10,8)) 
    nx.draw(DG,node_size=600,node_color=colors,pos=node_positions,prog='dot',labels=labels)
    nx.draw_networkx_edge_labels(DG,node_positions,edge_labels=edge_labels)

    plt.axis('off')
    plt.show()

  def get_edge_labels(self):
    arr = {}
    for n in self.nodes:
      for p in list(n.elements.keys()):
        if n.pi != p:
          arr[p, n.pi] = 'a{}'.format(n.elements[p][0] + 1)
    return arr



