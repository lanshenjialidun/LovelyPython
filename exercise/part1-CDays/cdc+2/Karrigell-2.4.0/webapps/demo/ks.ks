class Record:
    def __init__(self,Empresa,Contacto,Pais):
        self.Empresa=Empresa
        self.Contacto=Contacto
        self.Pais=Pais

res = [Record('Renault','Dupond','France')]

def index():
    Include('../tmp.tmpl', **globals())
    
