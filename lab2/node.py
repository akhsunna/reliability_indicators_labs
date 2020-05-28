from functools import reduce
from copy import copy
import numpy as np

class Node:
  def __init__(self, pi, binary, **kw_args):
    self.pi = pi
    self.binary = binary
    self.elements = kw_args.get('elements', dict())
    self.first_fixed = kw_args.get('first_fixed', False)

  def add_element(self, ai, cpi, **kw_args):
    mu = kw_args.get('mu', False)
    if mu:
      ai = ai + 5
    if cpi not in self.elements:
      self.elements[cpi] = []
    if ai not in self.elements[cpi]:
      self.elements[cpi].append(ai)

  def binary_list(self):
    return map(lambda x: int(x), list(self.binary))   

  def new_child(self, i):
    return self.binary[i] == '1'

  def s_binary(self):
    index = 1
    if self.first_fixed:
      return self.binary[:index] + '*' + self.binary[index:]
    else:
      return self.binary

  def new_binary(self, i, **kw_args):
    one = kw_args.get('one', False)
    str = copy(self.binary)
    if one:
      str = str[:i] + '1' + str[i + 1:]
    else:
      str = str[:i] + '0' + str[i + 1:]
    return str

  def state(self):
    u1, u2, u3, u4, u5 = map(lambda x: int(x), self.binary_list())
    return bool(((u1 and u2) or u3) and (u4 or u5))

  def level(self):
    return self.binary.count('0')

  def matrix_row(self, a, n):
    arr = []
    for i in range(n):
      if i in self.elements:
        v = reduce(lambda sum,c: sum + a[c], self.elements[i], 0)
        if i == self.pi:
          v = -1*v
        arr.append(v)
      else:
        arr.append(0)
    return arr 

  def eq_str(self):
    equation = 'dP{}(t)/dt = '.format(self.pi)
    def to_string(i, ais):
      r = ' + '.join(map(lambda ai: ('m{}'.format(ai - 4) if ai > 4 else 'a{}'.format(ai + 1)), ais))
      if len(ais) > 1:
        r = '({})'.format(r)     
      r = '{} * P{}(t)'.format(r,i)
      r = (" - " if i == self.pi else " + ") + r
      return r
    n_elements = list({k: to_string(k, v) for k, v in self.elements.items()}.values())
    return equation + ''.join(n_elements)[3:]
