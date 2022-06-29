from prubik import RTM

from parallelSwap2x4 import *
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import problem_generator as pg
import json
import yaml
import argparse
import time
from common import *



class RTM2x4(RTM):
    def __init__(self, dim, agents):
        super().__init__(dim, agents)


    def y_shuffle(self):
        pass

    def x_shuffle(self):
        pass


    
