from parallelSwap import ParallelSwap
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



class RTM(object):
    def __init__(self,dim,agents):
        self.dim=dim
        self.agents=agents
        self.starts=[agent.current for agent in agents]
        self.goals=[agent.goal for agent in agents]
  
     

    def bi_matching(self,column_dict:dict):
        #bi matching for a single row
        B=nx.Graph()
        bottom_nodes=list(range(0,self.dim[1]))
        top_nodes=list(column_dict.keys())

        B.add_nodes_from(top_nodes, bipartite=0)
        B.add_nodes_from(bottom_nodes, bipartite=1)
        edges=[]
        arranged_agents=dict()
        for i in top_nodes:
            for j in range(self.dim[1]):
                for agent in column_dict[i]:
                  
                    #if i th column has color j
                    if agent.goal[1]==j:
                        edges.append((i,j))
                        #remove the agent
                        arranged_agents[(i,j)]=agent               
                        break
                
        B.add_edges_from(edges)
        #assert(nx.is_bipartite(B))
        perfect=nx.algorithms.bipartite.matching.hopcroft_karp_matching(B, top_nodes)

        for col in top_nodes:
            color=perfect[col]
            agent=arranged_agents[(col,color)]
            column_dict[col].remove(agent)
        return perfect,arranged_agents



   
    def check_feasible(self, agents):
        config=[agent.intermediate for agent in agents]
        config_set=set(config)
        if not len(config_set)==len(config):
            print(len(config_set))
            print(len(config))
        assert(len(config_set)==len(config))   
        
        config=[agent.current for agent in agents]
        config_set=set(config)
        if not len(config_set)==len(config):
            print(len(config_set))
            print(len(config))
        assert(len(config_set)==len(config))  


    def n_matching(self):

 
        column_dict=dict()
        for i in range(self.dim[1]):
            if i not in column_dict:
                column_dict[str(i)]=[]
            for agent in self.agents:
                if agent.current[1]==i:
                    column_dict[str(i)].append(agent)
            column_dict[str(i)].sort(key=lambda x:agent.goal[0])
            # fill with virtual agents
        #the colors in column i
        for i in range(self.dim[0]):
            matching,arranged_agents=self.bi_matching(column_dict)
            for color in range(0,self.dim[1]):
                column=matching[color]
                agent=arranged_agents[(column,color)]
                agent.intermediate=(i,int(column))   
                     
        #self.check_feasible(self.agents)    


        
    def y_fitting(self):
        #row shuffling
        #agent are now in the correct row, we need to put them in the correct columns.
        for agent in self.agents:
            agent.intermediate=(agent.current[0],agent.goal[1])
            #agent.path.append(agent.current)
        self.check_feasible(self.agents)   

    def x_fitting(self):
        for agent in self. agents:
            agent.intermediate=(agent.goal[0],agent.current[1])
            #agent.path.append(agent.current)
        self.check_feasible(self.agents)   
        
 
    def route_to_inter(self):
        for agent in self.agents:
            agent.current=agent.intermediate


    def y_shuffle(self):
      
        agents_dict=dict()
        for agent in self.agents:
            vid= agent.current[0]//3
            if vid not in agents_dict:
                agents_dict[vid]=[]
            agents_dict[vid].append(agent)
        for i in range(0,self.dim[0],3):
            vid=i//3
            swapper=ParallelSwap(i,i+2,0,self.dim[1]-1,agents_dict[vid],orientation='y')
            swapper.swap()
        maxspan=max([len(agent.path) for agent in self.agents])
        for agent in self.agents:
            while len(agent.path)<maxspan:
                agent.path.append(agent.path[-1])

    def x_shuffle(self):
        makespan=0
        agents_dict=dict()
        for agent in self.agents:
            vid= agent.current[1]//3
            
            if vid not in agents_dict:
                agents_dict[vid]=[]
            agents_dict[vid].append(agent)
  
     
        for i in range(0,self.dim[1],3):
            vid=i//3
            swapper=ParallelSwap(0,self.dim[0]-1,i,i+2,agents_dict[vid],orientation='x')
            swapper.swap()

        maxspan=max([len(agent.path) for agent in self.agents])
        for agent in self.agents:
            while len(agent.path)<maxspan:
                agent.path.append(agent.path[-1])
    
    def three_n_shuffle_sim(self):
        self.n_matching()
        self.x_shuffle()
        # for agent in self.agents:
        #     if agent.current!=agent.intermediate:
        #         print(agent)
        #     assert(agent.current==agent.intermediate)
        print("x1 shuffle done!")
        self.y_fitting()
        self.y_shuffle()
        print("y1 shuffle done!")
        self.x_fitting()
        self.x_shuffle()

        
        
        makespan=max(len(agent.path) for agent in self.agents)
        
        print('makespan=',makespan)
        




    #p.three_n_shuffle_rubik()
    #save_output(agents,0,'./test.yaml')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--f", help="filename")
    parser.add_argument("--o",help='output')
    args = parser.parse_args()
    
    if args.f:
        graph,starts,goals=pg.read_from_yaml(args.f)
        xmax = max([x for x, y in graph.nodes()]) + 1
        ymax = max([y for x, y in graph.nodes()]) + 1
        print(xmax,ymax)
        agents=agents_from_starts_and_goals(starts,goals)  
        
       # pg.save_instance_txt(graph,starts,goals,"./48x72.map","full_demo.scen")
        
        p=RTM([xmax,ymax],agents)
        t1=time.clock()
        p.three_n_shuffle_sim() 
        t2=time.clock()
        save_output(p.agents,computation_time=t2-t1,filename=args.o,save_path=False)
        #save_as_txt(agents,computation_time=t2-t1,filename=args.o,save_path=False)
        
    else:
        graph,starts,goals=pg.read_from_yaml('./90.yaml')
        xmax = max([x for x, y in graph.nodes()]) + 1
        ymax = max([y for x, y in graph.nodes()]) + 1
        agents=agents_from_starts_and_goals(starts,goals)  
        p=RTM([xmax,ymax],agents)
        #t1=time.clock()
        p.three_n_shuffle()
        #t2=time.clock()
        #graph=pg.generate_full_graph(12,2)
        #starts,goals=pg.generate_instance(graph,24)
        
        

if __name__=="__main__":
    #random_rubik_table_test(72,72)
    #test_nx()
    main()






