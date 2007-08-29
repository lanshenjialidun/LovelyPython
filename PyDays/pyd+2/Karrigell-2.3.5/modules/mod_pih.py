import os
from k_script import BaseScript, ParseError
import PythonInsideHTML

class Script(BaseScript):
    """Python inside HTML"""
    def __init__(self, fileName):
        # pih (PythonInsideHTML) scripts : parse
        try:
            pih=PythonInsideHTML.PIH(fileName)
        except PythonInsideHTML.PIH_ParseError,msg:
            raise ParseError,msg
        pc=pih.pythonCode()
        BaseScript.__init__(self, fileName, pc, pih.getLineMapping())
    

