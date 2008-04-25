class cvpool:
    """Cheetah templet usage class
    """
    def __init__(self):
        self.d = {}
    def push(self,name,data):
        self.d[name] = data

def index():
    v = cvpool()
    v.push("foo","Foooooo")
    Include("../idx.tmpl",**{'v':v})