"""Used in case of errors or exceptions in scripts"""

import cStringIO
import cgi
import types

from core import k_config, k_utils

Errors=k_utils.LimitedDict(100)

class Error:
    """An instance of Error is created every time Template handles
    an error or an exception
    The instances are kept in the dictionary Errors, with keys generated
    at random. The key is used by the debugger scripts"""
    
    def __init__(self,tree,tb,exc_info,namespace,initialNs,key):
        """Instances are created from 
        - tree : tree[0] is the script (instance of the Script class
        in Template) where the error occured. If it is included in other 
        scripts, the following items are its parents
        - tb and exc_info : traceback elements
        - initialNs : a copy of the namespace before the script ran
        - namespace : a copy of the namespace after the script has run
        - key : random string generated in Template""" 
        
        self.namespace={0:id(namespace),
            id(namespace):k_utils.Node(None,"namespace",namespace)}
        self.initialNs=initialNs
        self.tree=tree
        self.script=tree[-1]
        
        # browses traceback upwards
        errorLine=0
        for i in range(len(tb)):
            (filename,errorLine,x,y)=tb[len(tb)-i-1]
            if filename=="<string>":
                break
        [exc_type,exc_value]=exc_info[:2]
        try:
            stype = exc_type.__name__
        except AttributeError:
            stype = str(exc_type)
        if exc_type in [SyntaxError,IndentationError]:
            exc_type_value=stype
            try:
                errorMsg,(filename, lineno, offset, line) = exc_value
                errorLine=lineno
            except:
                pass
        else:
            exc_type_value=str(stype)+": "+str(exc_value)

        if self.script.lineMapping is None:
            originLineNum=errorLine-1
        else:
            try:
                originLineNum=self.script.lineMapping[errorLine-1]
            except KeyError:
                originLineNum=errorLine-1
        try:
            originErrorLine=open(self.script.name).read().split("\n")[originLineNum]
        except IndexError:
            originErrorLine= '--error fetching error origin line --' 
        self.exc_type_value=exc_type_value
        self.originLineNum=originLineNum
        self.originErrorLine=originErrorLine
        self.pythonLine=errorLine
        self.key=key
        Errors[key]=self

    def getRawTraceback(self):
        """Used from Template to write the raw Python traceback"""
        self.raw_traceback=cStringIO.StringIO()
        return self.raw_traceback

    def errorText(self):
        """Return the HTML code giving minimal info about the error :
        name of the script, name and message of the exception,
        line number in script"""
        errorText=cStringIO.StringIO()
        errorText.write('<font face="verdana" color="red">')
        errorText.write('<b>Error in %s</b></font><p>\n' %self.script.url)
        # if script is included, show tree
        if len(self.tree)>1:
            inclusionTree="".join(["\n"+" "*i+" includes "+s.url for i,s in enumerate(self.tree[1:])])
            errorText.write("<p><pre>"+self.tree[0].url+inclusionTree+'</pre><p>')
        errorText.write('<table border="1">\n<tr><td bgColor="#FFFFCC">\n')
        errorText.write('<pre>Script <b>%s</b><hr>' %self.script.url)
        errorText.write(cgi.escape(self.exc_type_value)+'\n\n')
        errorText.write('Line %s' %(self.originLineNum+1)+"&nbsp;"*4+"\n")
        errorText.write(cgi.escape(self.originErrorLine).strip())
        errorText.write('</pre></td></tr></table>')
        errorText.write("<pre>\n%s\n</pre>\n" %cgi.escape(self.raw_traceback.getvalue()))
        return errorText.getvalue()
        
    def HTML(self):
        """Return the complete HTML code, including a button to launch the
        debugger scripts"""
        HTML=cStringIO.StringIO()
        HTML.write(self.errorText())
        # if debug is set, show the "Debug" button
        if k_config.debug:
            # base url
            debuggerUrl=k_config.base + "/debugger/frame_debug.pih"
            HTML.write("""<form action="%s" target="_blank">
            <input type="hidden" name="key" value="%s">
            <input type="submit" value="Debug">
            </form>""" %(debuggerUrl,self.key))
        return HTML.getvalue()
