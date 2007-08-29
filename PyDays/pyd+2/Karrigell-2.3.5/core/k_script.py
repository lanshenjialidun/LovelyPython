import sys
import os
import cStringIO
import copy
import traceback

from k_stringio import KStringIO as StringIO
import k_config
import k_utils
import k_translation
import debugger

class HTTP_REDIRECTION(Exception):
    pass

class AUTH_ABORT(Exception):
    pass

class HTTP_ERROR(Exception):

    def __init__(self,code,message):
        self.code=code
        self.message=message

    def __str__(self):
        return self.code+self.message

class HTTP_RESPONSE(Exception):
    pass
    
class SCRIPT_END(Exception):
    pass

class SCRIPT_ERROR(Exception):
    pass

class ParseError(Exception):

    def __init__(self,value):
        self.msg=value.msg
        self.errorLine=value.errorLine
        
    def __str__(self):
        return self.msg

class RecursionError(Exception):

    def __init__(self,tree):
        self.tree=tree

    def __str__(self):
        """Return a tree-like view of the recursion problem"""
        return self.tree[0].name+"".join([ "\n"+" "*i+" includes "+s.name \
            for (i,s) in enumerate(self.tree[1:])])

class Output:
    """Used for output of scripts"""
    
    def __init__(self,script,status,value):
        """script is the script name
        status is 1 if no error in script, 0 if error
        value is the output of the script (the traceback if status==0)"""
        self.script=script
        self.status=status
        self.value=value
    
    def __str__(self):
        return self.value

class BaseScript:
    """An instance of Script is created for each script run by
    Karrigell
    This instance itself is available inside the script under the
    reserved name THIS, allowing the programmer to use all its
    attribute
    """

    def __init__(self,name,code,lineMapping):
        """lineMapping is a dictionnary mapping line numbers in python code to 
        lines in original script ; serves only for .pih scripts, in
        tracebacks"""
        self.name=os.path.normpath(name)
        self.basename=os.path.basename(name)
        if os.path.isdir(name):
            self.dirname=name
        else:
            self.dirname=os.path.dirname(name)
        self.code=code
        self.lineMapping=lineMapping
        # the parent and caller attributes are set for Included scripts
        self.parent=None

    def pythonCode(self):
        return self.code

    def loadTranslations(self, nameSpace, rep): 
        # translation 
        k_translation.install(rep,nameSpace.get("ACCEPTED_LANGUAGES",[]),
            k_config.outputEncoding)

    def render(self,nameSpace={},**args):
        """Run the script and return an instance of Output"""

        # build a list of parents and detect if there is a recursion error
        # if the script is included in itself
        s = self
        tree = [s]
        while s.parent is not None and hasattr(s.parent,"name"):
            tree.insert(0,s.parent)
            if s.parent.name == self.name:
                raise RecursionError,tree
            s = s.parent
            
        ns = nameSpace
        # put form fields in name space with a leading _
        if nameSpace.has_key("QUERY"):
            for item in nameSpace["QUERY"].keys():
                nameSpace["_"+item]=nameSpace["QUERY"][item]
        for n,v in nameSpace.items():
            ns[n] = v
        for n,v in args.items():
            ns[n] = v

        # adds a variable THIS in namespace = the Script instance itself
        ns['THIS']=self

        # translation
        self.loadTranslations(nameSpace, self.dirname) 

        # if script in protected zone, include AuthentScript
        pythonCode=self.pythonCode()
        (protectedDir,depth) = k_utils.pathInDirs(self.name,k_config.protectedDirs)
        if protectedDir is not None:
            self.code='RestrictToAdmin();' + self.pythonCode()

        saveStdout=sys.stdout
        sys.stdout=StringIO()
        saveNs=copy.copy(ns)
        status=1    # becomes 0 if error in script
        
        try:
            for globalScript in k_config.globalScripts:
                ns[globalScript]=sys.modules[globalScript]
            self.run_script(ns)
            # restore THIS if script was included
            ns['THIS']=self.parent
        except SCRIPT_END:
            # if SCRIPT_END, return the output produced 
            # before the exception occured
            pass
        except SCRIPT_ERROR, msg:
            sys.stdout = cStringIO.StringIO(str(msg))
        except (HTTP_REDIRECTION,HTTP_ERROR,AUTH_ABORT,HTTP_RESPONSE):
            # these exceptions must be relayed to Karrigell
            raise
        except:
            # an exception was raised when executing the script
            status=0
            # create an instance of the Error class in module debugger.k_debugger
            # for traceback printing and debugging
            key=k_utils.generateRandom(8)
            error=debugger.k_debugger.Error(tree,
                traceback.extract_tb(sys.exc_info()[2]),
                sys.exc_info(),
                copy.copy(ns),
                saveNs,
                key)
            traceback.print_exc(file=error.getRawTraceback())
            sys.stdout=StringIO()
            sys.stdout.write(error.HTML())
        output=sys.stdout.getvalue()
        sys.stdout=saveStdout
        return Output(self,status,output)

    def run_script(self,ns):
        """Overriden in subclasses"""
        exec self.pythonCode() in ns
        