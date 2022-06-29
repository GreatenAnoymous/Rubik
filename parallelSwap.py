from common import *
import json
import numpy as np

from local_graph import LocalGraph

f = open ('./2x3data.json', "r")
print("load 2x3 data")
figure8_data=json.load(f)

class ParallelSwap(object):
    def __init__(self,xmin,xmax,ymin,ymax,agents,orientation='x'):
        self.xmin=xmin
        self.xmax=xmax
        self.ymin=ymin
        self.ymax=ymax
 
        self.orientation=orientation
        self.agents=agents
    
    def check_if_reached(self):
        for r in self.agents:
            if r.current!=r.intermediate:
                return False
        return True


    def swap(self):
        if self.orientation=='x':
            self.swap_x()
        else:
            self.swap_y()


    def swap_x(self):
        for i in range(self.xmin,self.xmax):
            pre_dict=dict()
            # print("phase ",i)
           
            # robots.sort(key=lambda a:a.current[0])
            start_index=i%2
            for r in self.agents:
                fi=(r.current[0]+start_index)//2
                if fi not in pre_dict:
                    pre_dict[fi]=[]
                pre_dict[fi].append(r)
    
            for i in range(self.xmin+start_index,self.xmax,2):
                fi=(i+start_index)//2
                fig8=Figure3x2(pre_dict[fi],self.orientation)
                fig8.solve()
            self.fill_paths()
        for r in self.agents:

            assert(r.current==r.path[-1])
            if r.intermediate !=r.current:
                r.current=r.intermediate
            assert(r.intermediate==r.current)
        
    def swap_y(self):
        for i in range(self.ymin,self.ymax):
            pre_dict=dict()
            # robots.sort(key=lambda a:a.current[0])
            start_index=i%2
            for r in self.agents:
                fi=(r.current[1]+start_index)//2
                if fi not in pre_dict:
                    pre_dict[fi]=[]
                pre_dict[fi].append(r)
            # soc=0
            # for key,item in pre_dict.items():
            #     print(key,len(item),[r.current for r in item])
            #     soc=soc+len(item)
            # print("soc=",soc)
            for i in range(self.ymin+start_index,self.ymax,2):
                fi=(i+start_index)//2
                if len(pre_dict[fi])!=6:
                    print(fi,len(pre_dict[fi]))
                assert(len(pre_dict[fi])==6)
                fig8=Figure3x2(pre_dict[fi],self.orientation)
                fig8.solve()
            self.fill_paths()
        for r in self.agents:
            if r.intermediate !=r.current:
                r.current=r.intermediate
            assert(r.intermediate==r.current)

    def fill_paths(self):
        makespan=0
        for r in self.agents:
            makespan=max(makespan,len(r.path))
        for r in self.agents:
            while len(r.path)<makespan:
                r.path.append(r.path[-1])
            
            r.current=r.path[-1]
        

class Figure3x2(LocalGraph):
    def __init__(self,agents,orientation='x'):
        super().__init__(agents,orientation)
        if orientation=='x':
            self.vertices.sort(key=lambda v:self.greaterX(v))
        else:
            self.vertices.sort(key=lambda v:self.greaterY(v))
        

    def sortX(self,robots):
        goal_id=list(range(6))
        if robots[0].intermediate[0]>robots[3].intermediate[0]:
            goal_id[0],goal_id[3]=goal_id[3],goal_id[0]
        if robots[1].intermediate[0]>robots[4].intermediate[0]:
            goal_id[1],goal_id[4]=goal_id[4],goal_id[1]
        if robots[2].intermediate[0]>robots[5].intermediate[0]:
            goal_id[2],goal_id[5]=goal_id[5],goal_id[2]
        return goal_id
    
    def sortY(self,robots):
        goal_id=list(range(6))
        if robots[0].intermediate[1]>robots[3].intermediate[1]:
            goal_id[0],goal_id[3]=goal_id[3],goal_id[0]
        if robots[1].intermediate[1]>robots[4].intermediate[1]:
            goal_id[1],goal_id[4]=goal_id[4],goal_id[1]
        if robots[2].intermediate[1]>robots[5].intermediate[1]:
            goal_id[2],goal_id[5]=goal_id[5],goal_id[2]
        return goal_id


    def solve(self):
        robots=self.agents.copy()
        
        robots.sort(key=lambda a:self.get_id(a.current))
        # goal_id=list(range(6))
        # for r in robots:
        #     print(r.current, r.intermediate)
        # print('==================')
        # goal_id.sort(key=lambda a:self.get_vid(robots[a].intermediate))
        if self.orientation=='x':
            goal_id=self.sortX(robots)
        else:
            goal_id=self.sortY(robots)
        solution=figure8_data[str(tuple(goal_id))]
        for i in range(len(solution)):
            for v in solution[i]:
                robots[i].path.append(self.vertices[v])
        

    def get_id(self,v):
        return self.vertices.index(v)
    
    def get_vid(self, v):
        if self.orientation=='x':
            return v[1]+v[0]*1000
        else:  
            return v[0]+v[1]*1000  

    def greaterX(self,v):
        return v[0]*3+v[1]

    def greaterY(self,v):
        return v[1]*3+v[0]
        


    

    
       

    
