class Client:

    def __init__(self,surname,firstname,email):
        self.surname=surname
        self.firstname=firstname
        self.email=email

clients = ( Client('Dupont','Jean','jean.dupont@wanadoo.fr'),
    Client('Bertau','Cecile','cecile.bertau@wanadoo.fr') )

Include('htmlTagsTemplate.py',title='Clients',clients=clients)
