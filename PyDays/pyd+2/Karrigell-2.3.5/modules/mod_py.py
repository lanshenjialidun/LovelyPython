from k_script import BaseScript

class Script(BaseScript):
    """Python script"""
    def __init__(self, fileName):
        pc=open(fileName).read().rstrip()
        pc = pc.replace('\r\n','\n')     # normalize line separator
        BaseScript.__init__(self, fileName, pc, None)

