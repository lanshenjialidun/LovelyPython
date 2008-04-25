"""Classes used by Wiki"""

import time

class Page:

    def __init__(self,name,title,content):
        self.name=name
        self.title=title
        self.content=content
        self.editable=1
        self.nbvisits=0
        self.created=time.time()
        self.version=1
        self.lastmodif=self.created
