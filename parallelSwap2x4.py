from parallelSwap import ParallelSwap

import json
import numpy as np

from local_graph import LocalGraph

f = open ('./2x4data.json', "r")
figure8_data=json.load(f)

class ParallelSwap3x2(ParallelSwap):
    def __init__(self, xmin, xmax, ymin, ymax, agents, orientation='x'):
        super().__init__(xmin, xmax, ymin, ymax, agents, orientation)


    def swap_x(self):
        pass


    def swap_y(self):
        pass





class Figure3x2(LocalGraph):
    def __init__(self, agents, orientation='x'):
        super().__init__(agents, orientation)
        if orientation=='x':
            self.vertices.sort(key=lambda v:self.greaterX(v))
        else:
            self.vertices.sort(key=lambda v:self.greaterY(v))


    def sortX(self,robots):
        pass

    def sortY(self,robots):
        pass

    def solve(self):
        pass


    def get_id(self,v):
        pass
  

    def greaterX(self,v):
        pass

    def greaterY(self,v):
        pass