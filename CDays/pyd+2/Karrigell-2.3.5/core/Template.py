"""Karrigell templating

Written by Pierre Quentel quentel.pierre@wanadoo.fr
Refactored by Didier Wenzek didier.wenzek@free.fr
(Code moved from Karrigell.py)

Published under the BSD licence. See the file LICENCE.txt
"""

import sys, os, urlparse, copy, cStringIO, traceback, imp
import urllib, gettext, cgi, tokenize

import debugger.k_debugger
import k_config, PythonInsideHTML, HIP, URLResolution, k_utils
from k_script import BaseScript, Output, ParseError
from k_script import SCRIPT_END,SCRIPT_ERROR,HTTP_REDIRECTION, \
     HTTP_ERROR,HTTP_RESPONSE,AUTH_ABORT

# use built-in set in Python2.4+ and sets.Set for Python2.3
try:
    set([1])
except:
    from sets import Set as set

# import the modules for handled extensions
for mod in k_config.handled_extensions:
    try:
        exec ('import mod_%s' %mod)
    except ImportError:
        pass

def list_directory(path,dirName):
    script = getScript('core/listDirectory.pih')
    return script.render({'path':path,'dirName':dirName,
        'serverDir':k_config.serverDir,
        'allow':k_config.allow_directory_listing}).value
    
def execScript(fileName, **args):
    """Runs the script and all the included scripts.
    Sends its output on current standard output"""
    ExecContext(getScript(fileName), args)()

def getScript(fileName):
    """Returns the Script instance matching filename"""
    base,extension=os.path.splitext(fileName)
    extension=extension[1:].lower()
    module = sys.modules['mod_%s' %extension]
    script = module.Script(fileName)
    script.extension=extension
    script.url = '[%s]' %fileName
    return script
        
class ExecContext:
    def __init__(self, script, nameSpace, path='',requestHandler=None):
        self.script = script
        self.nameSpace = copy.copy(nameSpace)
        self.nameSpace['Include'] = self.Include
        # set exceptions, only for use as a templating system
        self.nameSpace['SCRIPT_END']=SCRIPT_END
        self.nameSpace['SCRIPT_ERROR']=SCRIPT_ERROR
        self.nameSpace['HTTP_REDIRECTION']=HTTP_REDIRECTION
        self.nameSpace['HTTP_ERROR']=HTTP_ERROR
        self.nameSpace['HTTP_RESPONSE']=HTTP_RESPONSE
        self.nameSpace['AUTH_ABORT']=AUTH_ABORT
        self.nameSpace['THIS']=script
        self.stack = []
        self.output = []
        self.path = path
        self.requestHandler=requestHandler

    def __call__(self):
        ns0 = set(self.nameSpace.keys())
        self.stack = [self.script]
        output=self.script.render(self.nameSpace)
        self.output.append(output)
        self.stack = []
        errors = [ out for out in self.output if not out.status ]
        # if error in one of the scripts, only print the trace of this script
        if errors:
            output=errors[0]
        for k in set(self.nameSpace.keys())-ns0:
            if not k == '__builtins__':
                del self.nameSpace[k]
                del k
        return str(output)

    def getCurrentScript(self):
        if len(self.stack): return self.stack[-1]
        else: return self.script

    def Include(self,includedUrl,**args):
        """Include a document inside the current script output
        The other document is searched in current script directory
        If it's a script, it is run in the same namespace as the script ; if
        additional args are supplied they are added to the namespace
        If it's a plain document its content is sent to the standard output
        """
        url=urlparse.urljoin(self.path,includedUrl)
        url_without_qs,qs=URLResolution.split_query(url)
        qs=k_utils.applyQueryConvention(qs)
        args.update(qs)
        fileName=URLResolution.translate_path(url_without_qs)
        if not fileName:
            raise IOError
        if os.path.isdir(fileName):
            # search an index file
            # if no one or more than one is found, an exception is raised
            indexFile=URLResolution.indexFile(fileName)
            fileName=os.path.join(fileName,indexFile)
            if url.endswith("/"):
                url=urlparse.urljoin(url,indexFile)
            else:
                url=urlparse.urljoin(url+"/",indexFile)
        elif not os.path.exists(fileName):
            # search for a file with name fileName.ext
            # with extension in htm, html, py, pih, hip, ks
            # if no one or more than one is found, an exception is raised
            ext=URLResolution.search(url_without_qs,fileName)
            fileName+=ext
        fileExt=os.path.splitext(fileName)[1][1:]
        if not fileExt.lower() in k_config.handled_extensions:
            script=BaseScript(fileName,open(fileName).read(),{})
            output=Output(script,1,script.code)
        else:
            # create a Script object and keep track of the script from which
            # it was called (to localize errors when debugging)
            script=getScript(fileName)
            # set attributes for the included script
            script.url=url_without_qs
            script.parent=self.stack[-1]
            self.stack.append(script)
            # before execution, chdir to script dir
            saveDir=os.getcwd()
            thisDir=os.path.dirname(fileName)
            os.chdir(thisDir)
            if not thisDir in sys.path:
                sys.path.append(thisDir)
            output=script.render(self.nameSpace,**args)
            os.chdir(saveDir)
            script.loadTranslations(self.nameSpace,saveDir) 
            self.stack.pop()
        sys.stdout.write(str(output))
        self.output.append(output)

if __name__ == '__main__':
    if len(sys.argv) <= 1 :
        print "Usage : python Template.py script"
    else:
        execScript(sys.argv[1])
