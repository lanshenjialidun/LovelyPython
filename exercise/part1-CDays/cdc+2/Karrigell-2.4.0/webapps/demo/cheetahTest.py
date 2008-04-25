title = 'Cheetah test'

class Client:

    def __init__(self,surname,firstname,email):
        self.surname = surname
        self.firstname = firstname
        self.email = email
        
clients = [ Client('Proust','Marcel','marcel.proust@combray.fr'),
    Client('Salinger','J.D.','jd.salinger@nyc.rye')]

Include('cheetahTest.tmpl',**globals())