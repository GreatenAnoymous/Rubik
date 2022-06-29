import numpy as np
import json
import yaml
import os
import errno
from LBAP import *


def distance(v1,v2):
    return abs(v1[0]-v2[0])+abs(v1[1]-v2[1])






class Agent(object):
    def __init__(self,id,start,goal,virtual=False,current=None,group_id=None):
        self.id=id
        if current is None:
            self.current=start
        else:
            self.current=current
        self.start=start
        self.goal=goal
        self.path=[self.current]
        self.intermediate=None
        self.virtual=virtual
        self.inter_start=start
        self.inter_goal=goal
        self.group_id=group_id
        self.inter_path=None

    def __eq__(self,other):
        if isinstance(other,Agent):
            return self.id==other.id
        return False
    
    def __repr__(self):
        return str((self.id,self.current,self.goal))

    def __str__(self):
        return str((self.id,self.current,self.goal))

    def __hash__(self):
        return hash(self.id)


def lbap_assignment(agents):
    tmp_goal=[agent.goal for agent in agents]
    cost_matrix=[[distance(agents[i].start,agents[j].goal) for j in range(0,len(agents))]for i in range(len(agents))]
    row_ind,col_ind,_=labp_solve(cost_matrix)
    for i in row_ind:
        agents[i].goal=tmp_goal[col_ind[i]]


def assign_tasks(agents):
    id_dict=dict()
    for agent in agents:
        if agent.group_id not in id_dict:
            id_dict[agent.group_id]=[]
        id_dict[agent.group_id].append(agent)
    
    for id,groups in id_dict.items():
        lbap_assignment(groups)

def check_paths_feasibility(paths):
    maxspan=max([len(p) for p in paths])
    #check vertex  conficts
    for t in range(0,maxspan):
        occupied=[]
        for p in paths:
            if p[t] in occupied:
                print("vertex conflicts")
                return False
            else:
                occupied.append(p[t])
    #check consistency
    for p in paths:
        for t in range(0,len(p)-1):
            if distance(p[t],p[t+1])>1:
                print("in-consistency",p[t],p[t+1])
                return False
    return True

def check_agents_feasibility(agents):
    maxspan=max([len(agent.path) for agent in agents])
    #check vertex  conficts
    for t in range(0,maxspan):
        occupied=[]
        for agent in agents:
            if agent.path[t] in occupied:
                print("vertex conflicts")
                return False
            else:
                occupied.append(agent.path[t])
    #check consistency
    for agent in agents:
        for t in range(0,len(agent.path)-1):
            if distance(agent.path[t],agent.path[t+1])>1:
                print("in-consistency",agent.path[t],agent.path[t+1],agent)
                return False
    return True

def agents_from_starts_and_goals(starts,goals):
    agents=[]
    for i in range(0,len(starts)):
        agent=Agent('agent'+str(i),starts[i],goals[i])
        agents.append(agent)
    return agents

def save_output(agents,computation_time,filename,save_path=True,exra_step=0,extra_time=0,opt=0):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    # for agent in agents:
    #     if agent.current!=agent.intermediate:
    #         print(agent.current,agent.intermediate)
        #assert(agent.current==agent.goal)
    output=dict()
    makespan=max(len(agent.path) for agent in agents)
    if opt==1:
        assign_tasks(agents)
    makespan_lb=eval_makespan_lowerbound(agents)
    output['schedule']=dict()
    statistics=dict()
    
    statistics['makespan']=makespan+exra_step
    statistics['makespanLB']=makespan_lb
    statistics['runtime']=computation_time+extra_time
    output['statistics']=statistics
    if save_path==True:
        for agent in  agents:
            agent_path=[]
            for t in range(0,len(agent.path)):
                vertex=dict()
                vertex['x']=int(agent.path[t][0])
                vertex['y']=int(agent.path[t][1])
                vertex['t']=t
                
                agent_path.append(vertex)
            name='agent'+str(agent.id)
            output['schedule'][name]=agent_path
    #print(output['schedule'])
    with open(filename, 'w') as nf:
        yaml.dump(output, nf,sort_keys=False)#, Dumper=yaml.RoundTripDumper)
    print('Saved successfully')


def check_valid(agents):
    paths=[agent.path for agent in agents]
    makespan=max(len(p) for p in paths)
    #print(makespan)
    for t in range(0,makespan):
        used_vertex=dict()
        for agent in agents:
            if agent.path[t] in used_vertex:
                print("vertex collision! at time step ",agent,used_vertex[agent.path[t]],t,agent.path[t],used_vertex[agent.path[t]].path[t])
                return False
            else:
                used_vertex[agent.path[t]]=agent
    # for agent in agents:
    #     if agent.path[-1]!=agent.intermediate:
    #         print("not reach the intermeidate goal")
    #         return False
    return True

def eval_makespan_lowerbound(agents):
    maxspan=max([distance(agent.start,agent.goal)for agent in agents])
    return maxspan


def save_yaml(instance,filename='./test.yaml',obstacles=[]):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    nodes = list(instance.graph.nodes())
    w = max([x for x, y in nodes]) + 1
    h = max([y for x, y in nodes]) + 1
    contents=dict() 
    agents=[]
  
    numAgents=len(instance.starts)
  
    for i in range(0,numAgents):
        agent=dict() 
        agent["goal"]=[int(instance.goals[i][0]),int(instance.goals[i][1])]
        agent["name"]="agent"+str(i)
        agent["start"]=[int(instance.starts[i][0]),int(instance.starts[i][1])]
        agents.append(agent)
    contents["agents"]=agents
    maps=dict()
    maps["dimensions"]=[w,h] 
    maps["obstacles"]=[]
    for obs in obstacles:
        maps["obstacles"].append([obs[0],obs[1]]) 
    contents["map"]=maps
    
    with open(filename, 'w') as nf:
        yaml.dump(contents, nf)


def save_as_txt(agents,computation_time,filename,save_path=True,exra_step=0,extra_time=0,opt=0):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    makespan=max(len(agent.path) for agent in agents)
    
    soc=sum([len(agent.path) for agent in agents])
    if opt==1:
        assign_tasks(agents)
    makespan_lb=eval_makespan_lowerbound(agents)
 
    with open(filename, "w") as file_content:
        file_content.write("soc="+str(soc)+'\n')
        file_content.write("makespan="+str(makespan)+"\n")
        
        # file_content.write("lb_soc="+str(soc_lb)+"\n")
        file_content.write("lb_makespan="+str(makespan_lb)+"\n")
        file_content.write("comp_time="+str(int((computation_time+extra_time)*1000))+"\n")
        if save_path==True:
            file_content.write("solution=\n")
            for agent in agents:
                file_content.write(str(agent.id)+':')
                for v in agent.path:
                    file_content.write('('+str(v[0])+','+str(v[1])+'),')
                file_content.write('\n')

def save_yaml_agents(dimensions,agents,obstacles,filename='./test.yaml'):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
 
    w = dimensions[0]
    h = dimensions[1]
    contents=dict() 
    agent_list=[]
    numAgents=len(agents)
  
    for i in range(0,numAgents):
        agenti=agents[i]
        agent=dict() 
        agent["goal"]=[int(agenti.goal[0]),int(agenti.goal[1])]
        agent["name"]="agent"+str(i)
        agent["start"]=[int(agenti.start[0]),int(agenti.start[1])]
        if agenti.group_id is not None:
            agent['group_id']=int(agenti.group_id)
        agent_list.append(agent)
    contents["agents"]=agent_list
    maps=dict()
    maps["dimensions"]=[w,h] 
    maps["obstacles"]=[[obs[0],obs[1]] for obs in obstacles]
    contents["map"]=maps
    
    with open(filename, 'w') as nf:
        yaml.dump(contents, nf)
  

def read_output(filename):
    paths=[]
    with open(filename) as file:
        input = yaml.safe_load(file)
        schedule=input['schedule']
        dict=OrderedDict()
        for name,vertices in schedule.items():
            path=[]
            for vertex in vertices:
                # print(vertex)
                path.append((int(vertex['x']),int(vertex['y'])))
            paths.append([])
            dict[int(name[5:])]=path
        for key,val in dict.items():
            paths[key]=val
                   
    return paths


def agents_from_starts_and_goals(starts,goals):
    agents=[]
    for i in range(0,len(starts)):
        agent=Agent('agent'+str(i),starts[i],goals[i])
        agents.append(agent)
    return agents

def check_feasible(starts):
    used=dict()
    for s in starts:
        if s not in used:
            used[s]=1
        else:
            return False
    return True   
