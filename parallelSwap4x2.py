from parallelSwap import ParallelSwap

import json
import numpy as np

from local_graph import LocalGraph

f = open ('./4x2data.json', "r")
print("4x2 data")
figure8_data=json.load(f)

class ParallelSwap4x2(ParallelSwap):
    def __init__(self, xmin, xmax, ymin, ymax, agents, orientation='x'):
        super().__init__(xmin, xmax, ymin, ymax, agents, orientation)


    def swap_x(self):
        for r in self.agents:
            assert(r.current[1]==r.intermediate[1])
        for i in range(self.xmin,2*self.xmax+1):
            pre_dict=dict()
            phase=i%2
            for r in self.agents:
                
                if phase==0:
                    fi=(r.current[0])//4
                else:
                    if (self.xmax+1)%4==0:
                     
                        fi=(r.current[0]+2)//4
                    else:
                        fi=(self.xmax-r.current[0])//4
                if fi not in pre_dict:
                    pre_dict[fi]=[]
                pre_dict[fi].append(r)
    
            for index,agents in pre_dict.items():
                # fi=(i+start_index)//2
                fig8=Figure4x2(agents,self.orientation)
                fig8.solve()
            self.fill_paths()
            if self.check_if_reached():
                
                break

        for r in self.agents:
            assert(r.current==r.path[-1])
            if r.intermediate !=r.current:
                print(r.current,r.intermediate,r.id,"Not arrrived" )
                print(self.xmin,self.xmax,self.ymin,self.ymax)
                #raise Exception("not arrived!")
                r.current=r.intermediate


    def swap_y(self):
        for i in range(self.ymin,2*self.ymax+1):
            pre_dict=dict()
            phase=i%2
            for r in self.agents:
                assert(r.intermediate[0]==r.current[0])
                if phase==0:
                    fi=(r.current[1])//4
                else:
                    if (self.ymax+1)%4==0:
                        fi=(r.current[1]+2)//4
                    else:
                        fi=(self.ymax-r.current[1])//4
                if fi not in pre_dict:
                    pre_dict[fi]=[]
                pre_dict[fi].append(r)
            for index,agents in pre_dict.items():

                fig8=Figure4x2(agents,self.orientation)
                fig8.solve()
            self.fill_paths()
            if self.check_if_reached():
                break
        for r in self.agents:
            if r.intermediate !=r.current:
               # print(r.current,r.intermediate,r.id,"Not arrrived" )
                r.current=r.intermediate

                raise Exception("not arrived!")
            assert(r.intermediate==r.current)





class Figure4x2(LocalGraph):
    def __init__(self, agents, orientation='x'):
        super().__init__(agents, orientation)
        if orientation=='x':
            self.vertices.sort(key=lambda v:self.greaterX(v))
        else:
            self.vertices.sort(key=lambda v:self.greaterY(v))


    def sortX(self,robots):
        if len(robots)<8:
             return None
        up_list=[i for i in range(0,4)]
       

        down_list=[i for i in range(4,8)]
        up_list.sort(key=lambda i:robots[i].intermediate[0])
   
        down_list.sort(key=lambda i:robots[i].intermediate[0])
        
        result=[up_list.index(i) for i in range(0,4)]+[down_list.index(i)+4 for i in range(4,8)]
   
        return result

    def sortY(self,robots):
        if len(robots)<8:
             return None
        up_list=[i for i in range(0,4)]
        down_list=[i for i in range(4,8)]
        up_list.sort(key=lambda i:robots[i].intermediate[1])
        down_list.sort(key=lambda i:robots[i].intermediate[1])
        result=[up_list.index(i) for i in range(0,4)]+[down_list.index(i)+4 for i in range(4,8)]
        return result

    def solve(self):
        robots=self.agents
        robots.sort(key=lambda a:self.get_id(a.current))    
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


    def get_id(self,v):
        return self.vertices.index(v)
  

    def greaterX(self,v):
        return v[0]+v[1]*4

    def greaterY(self,v):
        return v[1]+v[0]*4

    def get_vid(self, v):
        if self.orientation=='x':
            return v[1]*1000+v[0]
        else:  
            return v[0]*1000+v[1]