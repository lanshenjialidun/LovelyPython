import os, sys
import tokenize

from k_script import BaseScript, ParseError, HTTP_ERROR

from k_encodings import k_encoding
import urllib

class Error:
    def __init__(self,msg,errorLine):
        self.msg = msg
        self.errorLine = errorLine

class Script(BaseScript):
    """Karrigell Service"""
    def __init__(self, fileName):
        # Python script : read, normalize line separator
        source=open(fileName).readlines()
        source=[ elt.rstrip() for elt in source ]
        source='\n'.join(source)
        source=source+'\n'
        # list of functions available by a url
        self.functions = []
        self.flag = False # if True, next token is a function name
        try:
            for info in tokenize.generate_tokens(open(fileName).readline):
                self.get_functions(info)
        except tokenize.TokenError,msg:
            pass
        BaseScript.__init__(self, fileName, source, None)

    def get_functions(self,info):
        """Parse the file searching for functions names available for
        KS scripts. They must be defined at the beginning of a line"""
        token_type,token_string,(srow,scol),(erow, ecol), line_num = info
        if self.flag:
            if not token_string.startswith("_"):
                self.functions.append(token_string)
            self.flag = False
        if tokenize.tok_name[token_type] == "NAME" and token_string=="def" \
            and scol==0:
            self.flag = True # next token will be a valid function name

    def run_script(self,ns):
        moduleName = os.path.splitext(os.path.basename(self.name))[0]
        
        args  =",".join([ '%s=_%s'%(k,k) for k in ns["QUERY"].keys() ])
        # check if the function is defined in the KS script
        function = self.subpath[0]
        # function has to be in plain ascii, because python 
        # does not support 8-bit literals
        try:
            function = function.encode('ascii')
        except UnicodeEncodeError:
            # if it is not ascii, it will not be in self.functions anyway
            # so we encode it with xml entities, for better displaying
            function = function.encode('ascii', 'xmlcharrefreplace')
        self.subpath = self.subpath[1:]
        self.up = '../' * len(self.subpath)
        if not function in self.functions:
            raise HTTP_ERROR,(404,"Function %s not defined in script %s" \
                %(function, moduleName+".ks"))
        exec self.pythonCode() in ns
        exec("%s(%s)" %(function,args)) in ns
