from msilib.schema import Class
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


class Fig3x3(object):
    def __init__(self,agents):
        self.agents=agents

    def solve(self):
        pass
    
    def getId(self,vertex):
        pass


    


class AVS(object):
    def __init__(self, dim, agents):
        self.dim=dim
        self.agents=agents


    def check_if_reached(self):
        for r in self.agents:
            if r.current!=r.goal:
                return False
        return True

    def fill_paths(self):
        makespan=0
        for r in self.agents:
            makespan=max(makespan,len(r.path))
        for r in self.agents:
            while len(r.path)<makespan:
                r.path.append(r.path[-1])
            r.current=r.path[-1]

    def solve(self):
        for i in range(self.ymin,self.ymax):
            pre_dict=dict()
            phase=i%2
            for r in self.agents:
                if phase==0:
                    fi=(r.current[0])//3,(r.current[1])//3
                else:
                    if (self.xmax+1)%3==0:
                        fi=(r.current[0]+2)//3,(r.current[1]+2)//3
                    else:
                        fi=(self.xmax-r.current[0])//3,(self.ymax-r.current[1])//3
                if fi not in pre_dict:
                    pre_dict[fi]=[]
                pre_dict[fi].append(r)
            for index,agents in pre_dict.items():
                fig8=Fig3x3(agents)
                fig8.solve()
            self.fill_paths()
            if self.check_if_reached():
                break
      

    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--f", help="filename")
    parser.add_argument("--o",help='output')
    args = parser.parse_args()
    
    if args.f:
        graph,starts,goals=pg.read_from_yaml(args.f)
        ymax = max([x for x, y in graph.nodes()]) + 1
        xmax = max([y for x, y in graph.nodes()]) + 1
        print(xmax,ymax)
        agents=agents_from_starts_and_goals(starts,goals)  
        
       # pg.save_instance_txt(graph,starts,goals,"./48x72.map","full_demo.scen")
        
        p=AVS([xmax,ymax],agents)
        t1=time.clock()
        p.solve()
        t2=time.clock()
        save_output(p.agents,computation_time=t2-t1,filename=args.o,save_path=False)
        #save_as_txt(agents,computation_time=t2-t1,filename=args.o,save_path=True)
        
    else:
        graph,starts,goals=pg.read_from_yaml('./90.yaml')
        xmax = max([x for x, y in graph.nodes()]) + 1
        ymax = max([y for x, y in graph.nodes()]) + 1
        agents=agents_from_starts_and_goals(starts,goals)  
        p=RTM3x3([xmax,ymax],agents)
        #t1=time.clock()
        p.three_n_shuffle()
        #t2=time.clock()
        #graph=pg.generate_full_graph(12,2)
        #starts,goals=pg.generate_instance(graph,24)

if __name__=="__main__":
    main()
