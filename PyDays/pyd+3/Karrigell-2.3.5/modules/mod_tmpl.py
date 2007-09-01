import os
from k_script import BaseScript
from Cheetah.Template import Template

class Script(BaseScript):
    """Cheetah template"""
    def __init__(self, fileName):
        # Python script : read, normalize line separator
        self.fileName = fileName
        source = open(fileName).readlines()
        source = [ elt.rstrip() for elt in source ]
        source = '\n'.join(source)
        source = source+'\n'
        BaseScript.__init__(self, fileName, source, None)

    def run_script(self,ns):
        for k in ns.keys():
            if k.startswith('_') and len(k)>1:
                ns[k[1:]] = ns[k]
        t = Template(self.pythonCode(),searchList=[ns])
        print t