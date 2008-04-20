""" Translates HTML Inside Python source code into Python scripts
A HIP script is made of normal Python code, but the lines beginning with 
quotes are converted into a print statement (replaced by "print "+ the line 
content)

It's the opposite of a PIH file where the default language is HTML and Python 
code is included inside the <% %> tags

The output is produced so that line number in it matches exactly the line 
number in original file
"""

import os,string,cStringIO,tokenize,token, cgi

#from k_stringio import KStringIO as StringIO

class HTMLStream:
    """Instances of this class are used in Python scripts to produce HTML
    with this syntax :
    import k_utils
    H=k_utils.HTMLStream()
    H + '<br>' - type(somevar)

    The last line above will send <br> and cgi.escape(type(somevar)) to the
    standard output"""

    def __add__(self,data):
        if isinstance(data, unicode):
            print data
        else:
            print str(data)
        return self
    
    def __sub__(self,data):
        if isinstance(data, unicode):
            d = data
        else:
            d = str(data)
        print cgi.escape(d)
        return self

class ParseError(Exception):

    def __init__(self,msg):
        self.msg=msg
        self.errorLine=0    # compatibility with Template.ParseError
    
    def __str__(self):
        return self.msg

class HIP:

    def __init__(self,fileName,indent=""):
        self.fileName=fileName
        self.indent=indent  # used by the Include() function
        hipCode=open(fileName).readlines()
        hipCode=map(string.rstrip,hipCode)
        hipCode=string.join(hipCode,'\n')
        hipCode=hipCode+'\n'
        hipCode=cStringIO.StringIO(hipCode).readline    # argument for tokenize
        [nom,ext]=os.path.splitext(fileName)
        self.output=cStringIO.StringIO()
        self.sourceline={}
        self.handledLine={}
        self.lastHandledLine=0
        self.line=cStringIO.StringIO()
        try:
            tokenize.tokenize(hipCode,self.analyse)
        except tokenize.TokenError,msg:
            raise ParseError,'Script %s - %s' %(os.path.basename(fileName),msg)

    def analyse(self,typ,chaine,deb,fin,ln):
        token_name=token.tok_name[typ]
        lineno=deb[0]
        # this is used for strings on several lines with """string"""
        self.sourceline[lineno]=ln
        if not self.lastHandledLine==lineno-1:
            ln=self.sourceline[self.lastHandledLine+1]
        if token_name=="NL":        # for instructions on several lines
            self.line.write(ln)
            self.handledLine[lineno]=1
            self.lastHandledLine=lineno
        elif token_name=="NEWLINE":
            self.line.write(ln)
            self.handledLine[lineno]=1
            self.lastHandledLine=lineno
            indent,reste=self.separeIndent(self.line.getvalue())
            l=indent+reste
            if reste.startswith('"') or reste.startswith("'") or reste.startswith('u"') or reste.startswith("u'"):
                l=indent+"print "+reste
            self.output.write(self.indent+l)
            self.line=cStringIO.StringIO() # this has to be raw 8-bit cStringIO, because we are assembling a python code from file
        elif token_name=="COMMENT":
            if string.lstrip(ln).startswith("#"):
                self.output.write(ln)
                self.handledLine[lineno]=1
                self.lastHandledLine=lineno

    def separeIndent(self,line):
        """Returns (indent,rest) depending on line indentation"""
        p=0
        while p<len(line) and line[p] in string.whitespace:
            p=p+1
        rest=line[p:]
        return line[:p],rest

    def pythonCode(self):
        # returns Python code
        return self.output.getvalue()

if __name__=="__main__":
    hip=HIP("demo/importTest.hip")
    print hip.pythonCode()
