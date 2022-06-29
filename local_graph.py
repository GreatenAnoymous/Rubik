
class LocalGraph(object):
    def __init__(self,agents,orientation='x'):
        self.orientation=orientation
        self.agents=agents
        self.vertices=[agent.current for agent in self.agents]
        # if orientation=='x':
        #     self.vertices.sort(key=lambda v:self.greaterX(v))
        # else:
        #     self.vertices.sort(key=lambda v:self.greaterY(v))
        

    def sortX(self,robots):
        pass
    
    def sortY(self,robots):
        pass


    def solve(self):
        pass
        

    def get_id(self,v):
        return self.vertices.index(v)
    
    def get_vid(self, v):
        pass

    def greaterX(self,v):
        pass

    def greaterY(self,v):
        pass





