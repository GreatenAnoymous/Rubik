from tracemalloc import start
from prubik import RTM

from parallelSwap3x2 import *
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



class RTM3x2(RTM):
    def __init__(self, dim, agents):
        super().__init__(dim, agents)


    def y_shuffle(self):
        agents_dict=dict()
        for agent in self.agents:
            vid= agent.current[0]//2
            if vid not in agents_dict:
                agents_dict[vid]=[]
            agents_dict[vid].append(agent)
        for i in range(0,self.dim[0],2):
            vid=i//2
            swapper=ParallelSwap3x2(i,i+1,0,self.dim[1]-1,agents_dict[vid],orientation='y')
            swapper.swap()
        maxspan=max([len(agent.path) for agent in self.agents])
        for agent in self.agents:
            while len(agent.path)<maxspan:
                agent.path.append(agent.path[-1])

    def x_shuffle(self):
       
        agents_dict=dict()
        for agent in self.agents:
            vid= agent.current[1]//2
            
            if vid not in agents_dict:
                agents_dict[vid]=[]
            agents_dict[vid].append(agent)
  
     
        for i in range(0,self.dim[1],2):
            vid=i//2
            swapper=ParallelSwap3x2(0,self.dim[0]-1,i,i+1,agents_dict[vid],orientation='x')
            swapper.swap()

        maxspan=max([len(agent.path) for agent in self.agents])
        for agent in self.agents:
            while len(agent.path)<maxspan:
                agent.path.append(agent.path[-1])

    # def three_n_shuffle_sim(self):
    #     self.n_matching()
    #     self.x_shuffle()
    #     # for agent in self.agents:
    #     #     if agent.current!=agent.intermediate:
    #     #         print(agent)
    #     #     assert(agent.current==agent.intermediate)
    #     print("x1 shuffle done!")
    #     self.y_fitting()
    #     self.y_shuffle()
    #     print("y1 shuffle done!")
    #     self.x_fitting()
    #     self.x_shuffle()

        
        
    #     makespan=max(len(agent.path) for agent in self.agents)
        
    #     print('makespan=',makespan)
        


def debug():
    robots=[]
    xmax=15
    starts1=[(x,0) for x in range(xmax)]
    starts2=[(x,1) for x in range(xmax)]
    goals1=[(x,0) for x in range(xmax)]
    goals2=[(x,1) for x in range(xmax)]
  
    np.random.shuffle(starts1)
    np.random.shuffle(starts2)
    starts=starts1+starts2
    goals=goals1+goals2
    for i in range(len(starts)):
        r=Agent(i,starts[i],goals[i])
        r.current=starts[i]
        r.intermediate=goals[i]
        robots.append(r)
    swapper=ParallelSwap3x2(0,xmax-1,0,1,robots,orientation="x")
    swapper.swap()

    

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
        
        p=RTM3x2([xmax,ymax],agents)
        t1=time.clock()
        p.three_n_shuffle_sim() 
        t2=time.clock()
        save_output(p.agents,computation_time=t2-t1,filename=args.o,save_path=False)
        #save_as_txt(agents,computation_time=t2-t1,filename=args.o,save_path=True)
        
    else:
        graph,starts,goals=pg.read_from_yaml('./90.yaml')
        xmax = max([x for x, y in graph.nodes()]) + 1
        ymax = max([y for x, y in graph.nodes()]) + 1
        agents=agents_from_starts_and_goals(starts,goals)  
        p=RTM3x2([xmax,ymax],agents)
        #t1=time.clock()
        p.three_n_shuffle()

        


if __name__=="__main__":
    main()
    # debug()
