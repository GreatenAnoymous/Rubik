from sympy import true
from common import save_as_txt, save_output
from parallelSwap import ParallelSwap

import json
import numpy as np

from local_graph import LocalGraph

f = open ('./3x2data.json', "r")
figure8_data=json.load(f)

print("load 3x2 data")

class ParallelSwap3x2(ParallelSwap):
    def __init__(self, xmin, xmax, ymin, ymax, agents, orientation='x'):
        super().__init__(xmin, xmax, ymin, ymax, agents, orientation)


    def swap_x(self):    
        # print(len(self.agents))
        for i in range(self.xmin,self.xmax+1):
            pre_dict=dict()
            phase=i%2
            for r in self.agents:
                if phase==0:
                    fi=(r.current[0])//3
                else:
                    if (self.xmax+1)%3==0:
                     
                        fi=(r.current[0]+2)//3
                    else:
                        fi=(self.xmax-r.current[0])//3
                if fi not in pre_dict:
                    pre_dict[fi]=[]
                pre_dict[fi].append(r)
    
            for index,agents in pre_dict.items():
                # fi=(i+start_index)//2
                fig8=Figure3x2(agents,self.orientation)
                fig8.solve()
            self.fill_paths()
            if self.check_if_reached():
                break

        for r in self.agents:
            assert(r.current==r.path[-1])
            if r.intermediate !=r.current:
                print(r.current,r.intermediate,r.id,"Not arrrived" )
                # raise Exception("not arrived!")
                r.current=r.intermediate

        # save_as_txt(self.agents,0,"./debug.txt",True)
        # exit(0)

    def check_if_reached(self):
        for r in self.agents:
            if r.current!=r.intermediate:
                return False
        return True

    def swap_y(self):
       
        for i in range(self.ymin,self.ymax):
            pre_dict=dict()
            phase=i%2
            for r in self.agents:
                if phase==0:
                    fi=(r.current[1])//3
                else:
                    if (self.ymax+1)%3==0:
                        fi=(r.current[1]+2)//3
                    else:
                        fi=(self.ymax-r.current[1])//3
                if fi not in pre_dict:
                    pre_dict[fi]=[]
                pre_dict[fi].append(r)
            for index,agents in pre_dict.items():

                fig8=Figure3x2(agents,self.orientation)
                fig8.solve()
            self.fill_paths()
            if self.check_if_reached():
                break
        for r in self.agents:
            if r.intermediate !=r.current:
                r.current=r.intermediate
                raise Exception("not arrived!")
            assert(r.intermediate==r.current)


    def swap(self):
        if self.orientation=='x':
            self.swap_x()
        else:
            self.swap_y()





class Figure3x2(LocalGraph):
    def __init__(self, agents, orientation='x'):
        super().__init__(agents, orientation)
        if orientation=='x':
            self.vertices.sort(key=lambda v:self.greaterX(v))
        else:
            self.vertices.sort(key=lambda v:self.greaterY(v))
     
      


    def solve(self):
        robots=self.agents
        
        robots.sort(key=lambda a:self.get_id(a.current))
        # for r in robots:
        #     print(r.current,r.intermediate,r.id)
        
        if self.orientation=='x':
            goal_id=self.sortX(robots)
          
        else:
            goal_id=self.sortY(robots)
        # print(goal_id)
        if goal_id==None:
            return
        solution=figure8_data[str(tuple(goal_id))]
        for i in range(len(solution)):
            for v in solution[i]:
                robots[i].path.append(self.vertices[v])

    def sortX(self,robots):
        if len(robots)<6:
             return None
        up_list=[i for i in range(0,3)]
       

        down_list=[i for i in range(3,6)]
        up_list.sort(key=lambda i:robots[i].intermediate[0])
   
        down_list.sort(key=lambda i:robots[i].intermediate[0])
        
        result=[up_list.index(i) for i in range(0,3)]+[down_list.index(i)+3 for i in range(3,6)]
   
        return result


    def sortY(self,robots):
        if len(robots)<6:
             return None
        up_list=[i for i in range(0,3)]
       

        down_list=[i for i in range(3,6)]
        up_list.sort(key=lambda i:robots[i].intermediate[1])
   
        down_list.sort(key=lambda i:robots[i].intermediate[1])
        
        result=[up_list.index(i) for i in range(0,3)]+[down_list.index(i)+3 for i in range(3,6)]
        return result

    def get_vid(self, v):
        if self.orientation=='x':
            return v[1]*1000+v[0]
        else:  
            return v[0]*1000+v[1]


    def get_id(self,v):
        return self.vertices.index(v)
  

    def greaterX(self,v):
        return v[0]+v[1]*3

    def greaterY(self,v):
        return v[1]+v[0]*3