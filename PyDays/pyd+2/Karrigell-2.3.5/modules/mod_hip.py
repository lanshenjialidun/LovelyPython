import os
from k_script import BaseScript, ParseError
import HIP

class Script(BaseScript):
    """HTML inside Python"""
    def __init__(self, fileName):
        # hip (HTMLInsidePython) scripts
        try:
            hip=HIP.HIP(fileName)
        except HIP.ParseError,msg:
            raise ParseError,msg
        pc=hip.pythonCode()
        BaseScript.__init__(self, fileName, pc, None)
