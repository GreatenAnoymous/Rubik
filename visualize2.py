#!/usr/bin/env python3
import yaml
import matplotlib
# matplotlib.use("Agg")
from matplotlib.patches import Circle, Rectangle, Arrow
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import matplotlib.animation as manimation
import argparse
import math
from ast import literal_eval as make_tuple
scale=2
Colors = ['orange']#, 'blue', 'green']


def load_instance(input_txt):
    with open(input_txt, "r") as file_content:
        lines = file_content.readlines()
        starts = list()
        goals = list()
        map_line=lines[0].split('=')
        map_name=(map_line[1].split('.'))[0]
        map_sizeX=int((map_name.split('x'))[0])
        map_sizeY=int((map_name.split('x'))[1])
        for line in lines[6:]:
            x1, y1, x2, y2 = line.split(',')
            starts.append((int(x1), int(y1)))
            goals.append((int(x2), int(y2)))
        #graph=nx.grid_graph(dim=[map_size,map_size])
        # pg.write_graph(graph,'./tmp/tmp.map')
        # pg.write_instance(graph,starts,goals,'./tmp/tmp.map','./tmp/tmp.instance')
    return map_sizeX,map_sizeY,starts,goals
    
def load_map(map_txt):
    xmax=0
    ymax=0
    obstacles=[]
    with open(map_txt,"r") as file_content:
        lines=file_content.readlines()
    
        xmax=int(lines[1].split()[1])
        ymax=int(lines[2].split()[1])
        
        obstacles = list()
        for y, line in enumerate(lines[4:]):
            for x, char in enumerate(line):
                if char != ".":
                    obstacles.append((x, y))
        
        return xmax,ymax,obstacles
        

def load_schedule(file_name):
    soc=0
    makespan=0
    paths=[]
    with open(file_name, "r") as file_content:
        lines = file_content.readlines()
        #print(lines)
        for line in lines:
            substrx=line.split('=')
            try:
                if substrx[0]=='soc':
                    soc=int(substrx[1])
                if substrx[0]=='makespan':
                    makespan=int(substrx[1])       
            except:
                pass
            try:
                substr_sol=line.split(':')
                
                if len(substr_sol)>=2:
                    #print(substr_sol)
                    path=[]
                    path_string=substr_sol[1]
                    
                    vertex_strings=path_string.split('),')
             
                    for vs in vertex_strings:
                        if vs!='\n':
                            vertex=vs+')'
                            path.append(make_tuple(vertex))
                    
                paths.append(path)
            except:
                pass
    k=5
    for i in range(len(paths)):
        for j in range(k):
            paths[i].append(paths[i][-1])
    return paths

def color_for_goal(g,m,n):
    start_color=[1,0,0]
    start_color[1]=start_color[1]+g[0]/m
    start_color[2]=start_color[2]+g[1]/n
    start_color[0]=start_color[0]-(g[0]+g[1])/(2.5*m)
    
    return np.array(start_color)
    

class Animation:
  def __init__(self, map_sizeX,map_sizeY, paths):
    self.map_sizeX = map_sizeX
    self.map_sizeY= map_sizeY
    #self.schedule = schedule
    self.paths=paths
    self.obstacles=[]
    #aspect = map["map"]["dimensions"][0] / map["map"]["dimensions"][1]
    aspect=1
    sizex=16
    self.fig = plt.figure(frameon=False, figsize=(sizex * aspect, sizex))
    self.ax = self.fig.add_subplot(111, aspect='equal')
    self.fig.subplots_adjust(left=0,right=1,bottom=0,top=1, wspace=None, hspace=None)
    # self.ax.set_frame_on(False)

    self.patches = []
    self.artists = []
    self.agents = dict()
    self.agent_names = dict()
    # create boundary patch
    xmin = -0.5
    ymin = -0.5
    xmax = map_sizeX - 0.5
    ymax =map_sizeY - 0.5

    # self.ax.relim()
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    # self.ax.set_xticks([])
    # self.ax.set_yticks([])
    # plt.axis('off')
    # self.ax.axis('tight')
    # self.ax.axis('off')
    print("starting!")
   
    self.patches.append(Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, facecolor='none', edgecolor='red'))
    #self.generate_obs()
    #for o in map["map"]["obstacles"]:
    #  x, y = o[0], o[1]
    #  self.patches.append(Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor='black', edgecolor='red'))
    self.arrange_random_colors(map_sizeX,map_sizeY)
    #self.arrange_column_colors()
    #self.colors = np.random.rand(len(map["agents"]),3)
    # create agents:
    self.T = 0
    # draw goals first
    for  i in range(0,len(paths)):
      goali=self.paths[i][-1]
      self.patches.append(Rectangle((goali[0] - 0.25, goali[1] - 0.25), 0.5, 0.5, facecolor=self.colors[i%len(self.colors)], edgecolor='black', alpha=0.15))
      #self.patches.append(Rectangle((d["goal"][0] - 0.25, d["goal"][1] - 0.25), 0.5, 0.5, facecolor=self.colors[i%len(self.colors)], edgecolor='black', alpha=0.15))
    for i in range(0,len(paths)):
      #name = d["name"]
      starti=self.paths[i][0]
      self.agents[i] = Circle((starti[0], starti[1]), 0.3, facecolor=self.colors[i%len(self.colors)], edgecolor='black')
      self.agents[i].original_face_color = self.colors[i%len(self.colors)]
      self.patches.append(self.agents[i])
      self.T = max(self.T, len(paths[i])-1)
      #self.agent_names[name] = self.ax.text(d["start"][0], d["start"][1], name.replace('Robot', ''),fontsize=10)
      #self.agent_names[name].set_horizontalalignment('center')
      #self.agent_names[name].set_verticalalignment('center')
      #self.artists.append(self.agent_names[name])

    print("agents created!")

    # self.ax.set_axis_off()
    # self.fig.axes[0].set_visible(False)
    # self.fig.axes.get_yaxis().set_visible(False)

    # self.fig.tight_layout()
    self.init_func()
    #print(int(self.T+1) * scale)
    self.anim = animation.FuncAnimation(self.fig, self.animate_func,
                               init_func=self.init_func,
                               frames=int(self.T+1) * scale,
                               interval=scale,
                               blit=True,repeat=True)
    
    # FFwriter = animation.FFMpegWriter(fps=10)
    self.anim.save('example.mp4',fps=10)
    # self.anim.save("exmaple_full.gif",fps=10, writer='pillow')
    
  def generate_obs(self):
      for i in range(1,self.map_sizeX,3):
          for j in range(1,self.map_sizeY,3):
              self.patches.append(Rectangle((i - 0.5, j - 0.5), 1, 1, facecolor='black', edgecolor='red'))
          
  def arrange_square_colors(self):
    self.colors=[]
    color_dict=dict()
    for d, i in zip(map["agents"], range(0, len(map["agents"]))):
        si=(d["start"][0],d["start"][1])
        gi=(d["goal"][0],d["goal"][1])
        if si not in color_dict:
            color_dict[si]=np.random.rand(3)
            color_dict[gi]=np.random.rand(3)
        self.colors.append(color_dict[si])
        
  def arrange_block_colors(self):
       m=30
       dd=6
       self.colors=[]
       color_dict=dict()
       for d, i in zip(map["agents"], range(0, len(map["agents"]))):
           si=(d["start"][0],d["start"][1])
           s_id=(int(si[0]/dd),int(si[1]/dd))
           if s_id not in color_dict:
               color_dict[s_id]=np.random.rand(3)
           self.colors.append(color_dict[s_id])
        
           
  def arrange_column_colors(self):
      
      self.colors=[]
      color_dict=dict()
      for d, i in zip(map["agents"], range(0, len(map["agents"]))):
          si=(d["start"][0],d["start"][1])
          gi=(d["goal"][0],d["goal"][1])
          g_id=int(gi[0]/3)
          if g_id not in color_dict:
              color_dict[g_id]=np.random.rand(3)
          self.colors.append(color_dict[g_id])
   
        
  def arrange_random_colors(self,m,n):
      
      self.colors=[]

      
      for i in range(len(self.paths)):
          si=self.paths[i][0]
          gi=self.paths[i][-1]
         
          self.colors.append(color_for_goal(gi,m,n))     
        
  
  def save(self, file_name, speed):
    self.anim.save(
      file_name,
      "ffmpeg",
      fps=10 * speed,
      dpi=800),
      # savefig_kwargs={"pad_inches": 0, "bbox_inches": "tight"})

  def show(self):
    plt.show()

  def init_func(self):
    for p in self.patches:
      self.ax.add_patch(p)
    for a in self.artists:
      self.ax.add_artist(a)
    return self.patches + self.artists

  def animate_func(self, i):
    for k in range(0,len(self.paths)):
      #agent = schedule["schedule"][agent_name]
      path=self.paths[k]
      #pos = self.getState(i / scale, agent)
      pos = self.getState(i / scale, path)
      p = (pos[0], pos[1])
      self.agents[k].center = p
      #self.agent_names[agent_name].set_position(p)

    # reset all colors
    '''
    for _,agent in self.agents.items():
      agent.set_facecolor(agent.original_face_color)

    # check drive-drive collisions
   
    agents_array = [agent for _,agent in self.agents.items()]
    for i in range(0, len(agents_array)):
      for j in range(i+1, len(agents_array)):
        d1 = agents_array[i]
        d2 = agents_array[j]
        pos1 = np.array(d1.center)
        pos2 = np.array(d2.center)
        if np.linalg.norm(pos1 - pos2) < 0.7:
          d1.set_facecolor('red')
          d2.set_facecolor('red')
          print("COLLISION! (agent-agent) ({}, {})".format(i, j))
    '''
    return self.patches + self.artists


  def getState(self, t, d):
    idx = 0
    while idx < len(d) and idx < t:
      idx += 1
    if idx == 0:
      return np.array([float(d[0][0]), float(d[0][1])])
    elif idx < len(d):
      posLast = np.array([float(d[idx-1][0]), float(d[idx-1][1])])
      posNext = np.array([float(d[idx][0]), float(d[idx][1])])
    else:
      return np.array([float(d[-1][0]), float(d[-1][1])])
    #dt = d[idx]["t"] - d[idx-1]["t"]
    #t = (t - d[idx-1]["t"]) / dt
    t=t-(idx-1)
    pos = (posNext - posLast) * t + posLast
    return pos




def save_as_txt(agents,computation_time,filename,save_path=True,exra_step=0,extra_time=0,opt=0):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    makespan=max(len(agent.path) for agent in agents)
    paths=[agent.path for agent in agents]
    shrink_paths(paths)
    soc=sum([len(agent.path) for agent in agents])
    if opt==1:
        assign_tasks(agents)
    makespan_lb=eval_makespan_lowerbound(agents)
    soc_lb=eval_soc_lowerbound(agents)
    with open(filename, "w") as file_content:
        file_content.write("soc="+str(soc)+'\n')
        file_content.write("makespan="+str(makespan)+"\n")
        
        file_content.write("lb_soc="+str(soc_lb)+"\n")
        file_content.write("lb_makespan="+str(makespan_lb)+"\n")
        file_content.write("comp_time="+str(int((computation_time+extra_time)*1000))+"\n")
        if save_path==True:
            file_content.write("solution=\n")
            for agent in agents:
                file_content.write(str(agent.id)+':')
                for v in agent.path:
                    file_content.write('('+str(v[0])+','+str(v[1])+'),')
                file_content.write('\n')

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("map", help="input file containing map")
  parser.add_argument("schedule", help="schedule for agents")
  parser.add_argument('--video', dest='video', default=None, help="output video file (or leave empty to show on screen)")
  parser.add_argument("--speed", type=int, default=1, help="speedup-factor")
  args = parser.parse_args()



 
  #map_sizeX,map_sizeY,starts,goals=load_instance(args.map)
  map_sizeX,map_sizeY,obstacles=load_map(args.map)

  paths=load_schedule(args.schedule)
  #print(args.schedule)
  print("number of agents=",len(paths))
  animation = Animation(map_sizeX,map_sizeY, paths)

  if args.video:
    animation.save(args.video, args.speed)
  else:
    animation.show()
