"""Starts a GUI application to see how PIH files are
processed by PythonInsideHTML
The resulting Python script can be run and the HTML code saved
in a file with the same name as the pih file, with the extension .htm"""

import os,sys
# change dirs and sys.argv for compatibility with imported modules
os.chdir(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())
sys.argv=[os.path.join(os.getcwd(),"dummy")]

import PythonInsideHTML
import traceback,cStringIO,re,webbrowser

from Tkinter import *
from ScrolledText import ScrolledText
import tkFileDialog
import tkMessageBox

class SyntaxFile:
    """A class to read syntax definition files
    Has a sections attribute, a dictionary whose keys are
    section names and values a list of words for the section"""

    def __init__(self,filename):
        lines=open(filename).readlines()
        lines=[line.strip() for line in lines]
        self.sections={}
        section=''
        for line in lines:
            if line.startswith(";"):
                continue
            if line.startswith('['):
                section=line[1:line.find("]")]
                self.sections[section]=[]
            else:
                # option
                if not section:
                    continue
                if line:
                    self.sections[section].append(line)

class Output:

    def __init__(self,window):
        self.window=window

    def write(self,data):
        self.window.insert(END,data)

def openPih(event):
    f=tkFileDialog.askopenfilename(filetypes=[("PIH",".pih")],
        title="PIH file",initialdir=os.getcwd())
    if not f:
        return
    p=PythonInsideHTML.PIH(f)
    pihText.filename=f
    pihText.delete(1.0,END)
    for line in p.pihCode:
        pihText.insert(END,line)
    root.title("Python Inside HTML - %s" %f)
    showPih(p)

def savePih(event):
    """Saves pih to disk"""
    # first backup previous version
    backupname=os.path.splitext(pihText.filename)[0]+".bak"
    if not os.path.exists(backupname):
        os.rename(pihText.filename,backupname)
    else:
        override=tkMessageBox.askyesno("Override ?",
            "File %s already exists - Override ?" \
            %os.path.basename(backupname))
        if override:
            dest=open(backupname,"w")
            dest.write(open(pihText.filename).read())
            dest.close()
    # then save new version
    pihCode=pihText.get(1.0,END)
    f=open(pihText.filename,"w")
    f.write(pihCode)
    f.close()
    
def parse(event):
    """Parse the content in pihCode"""
    f=cStringIO.StringIO(pihText.get(1.0,END))
    p=PythonInsideHTML.PIH()
    p.parse(f)
    showPih(p)

def showPih(p):
    pihText.src=p
    pihText.selectedTag=''
    tagPih()
    showPython(p.pythonCode()+'\n')

def tagPih():
    """tags every line in pih source"""
    for tag in pihText.tag_names():
        pihText.tag_delete(tag)
    # tags for Python syntax
    lastLine=int(pihText.index(END).split('.')[0])
    for i in range(lastLine-1):
        lineStart=str(i+1)+".0"
        lineEnd=str(i+1)+".end"
        tagName="tag"+str(i+1)
        pihText.tag_config(tagName,background="white")
        pihText.tag_add(tagName,lineStart,lineEnd)  
    # tag Python chunks
    ix=0
    # tag definitions must be here, for some reason it doesn't work
    # if defined at module level
    # tag for all text between <% and %> including <%= %> and <%_ %>
    pihText.tag_config("pyTag",foreground="#A08050")
    # tags for Python reserved names
    # change options as you like !
    pihText.tag_config("py0",foreground="red")
    pihText.tag_config("py1",foreground="orange")
    pihText.tag_config("py2",foreground="#FF8080")
    pihText.tag_config("karrigell",foreground="blue")
    pc=pihText.get(1.0,END)
    while 1:
        chunk=pyChunkRE.search(pc,ix)
        if not chunk:
            break
        chunkStart=pihText.index("1.0"+"+%schars" %chunk.start())
        chunkEnd=pihText.index("1.0"+"+%schars" %chunk.end())
        pihText.tag_add("pyTag",chunkStart,chunkEnd)
        # colorize Python reserved words
        for section in pyKwRE.keys():
            pykwix=chunk.start()
            while 1:
                pykw=pyKwRE[section].search(pc,pykwix)
                if not pykw or pykw.start()>chunk.end():
                    break
                pykwStart=pihText.index("1.0"+"+%schars" %(pykw.start()+1))
                pykwEnd=pihText.index("1.0"+"+%schars" %(pykw.end()-1))
                pihText.tag_add(section,pykwStart,pykwEnd)
                pykwix=pykw.end()
        ix=chunk.end()

def showPython(pCode):
    pythonText.config(state=NORMAL,cursor="arrow")
    pythonText.delete(1.0,END)
    pythonText.selectedTag=''
    lines=pCode.split('\n')
    for i in range(len(lines)):
        tagName="tag"+str(i+1)
        pythonText.tag_config(tagName,background="white")
        pythonText.tag_bind(tagName,"<Button-1>",showLineMatches)
        pythonText.insert(END,str(i+1).ljust(4)+'\t'+lines[i]+'\n',tagName)
    pythonText.config(state=DISABLED)

def showLineMatches(event):
    if pythonText.selectedTag:
        pythonText.tag_config(pythonText.selectedTag,background="white")
    tags=event.widget.tag_names(event.widget.index(CURRENT))
    for tag in tags:
        if tag.lower()=="sel":
            continue
        pythonText.tag_config(tag,background="#E0E0E0")
        pythonText.selectedTag=tag
        
        # tags matching pih line
        if pihText.selectedTag:
            pihText.tag_config(pihText.selectedTag,background="white")
        try:
            pihLine=pihText.src.lineMapping[int(tag[3:])-1]+1
            tagName="tag%s" %pihLine
            pihText.tag_config(tagName,background="#E0E0E0")
            pihText.selectedTag=tagName
        except KeyError:
            pass

def run(event):
    """Run the script and shows the resulting HTML code in a
    new window
    If started with the "Make HTML" button, saves HTML output in
    a file"""
    pythonCode=pythonText.get(1.0,END)
    lines=pythonCode.split('\n')
    lines=map(lambda x:x[5:],lines)
    pythonCode='\n'.join(lines)
    execWindow=Toplevel()
    execText=ScrolledText(execWindow,width=40,height=40,bg="white",
        font=FONT)
    execText.pack()
    s=sys.stdout
    sys.stdout=Output(execText)
    try:
        exec(pythonCode) in globals()
        if event.widget is bRunHTML:
            htmlFilename=os.path.splitext(pihText.filename)[0]+".htm"
            if os.path.exists(htmlFilename):
                override=tkMessageBox.askyesno("Override ?",
                    "File %s already exists - Override ?" \
                    %os.path.basename(htmlFilename))
                if not override:
                    return
            f=open(htmlFilename,"w")
            f.write(execText.get(1.0,END))
            f.close()
            path=os.path.join(os.getcwd(),htmlFilename)
            webbrowser.open_new("file://"+path)
    except:
        traceback.print_exc(file=sys.stdout)
    sys.stdout=s

pyChunkRE=re.compile("<%.*?%>",re.DOTALL)

# python syntax
# copied from the python.syn file for TextPad
pySyntax={}
pySyntax["py0"]=['and', 'del', 'for', 'is', 'raise', 'assert', 'elif', 'from', 'lambda', 
    'return', 'break', 'else', 'global', 'not', 'try', 'class', 'except', 
    'if', 'or', 'while', 'continue', 'exec', 'import', 'pass', 'def', 
    'finally', 'in', 'print']
pySyntax["py1"]=['__init__', '__repr__', '__del__', '__doc__', '__dict__']
pySyntax["py2"]=['abs', 'int', 'long', 'float', 'complex', 'conjugate', 'divmod', 'pow', 
    'len', 'min', 'max', 'append', 'extend', 'count', 'index', 'insert', 'pop', 
    'remove', 'reverse', 'sort', 'clear', 'copy', 'has_key', 'items', 'keys', 
    'update', 'values', 'get', 'close', 'flush', 'isatty', 'ArithmeticError', 
    'AssertionError', 'AttributeError', 'EOFError', 'Ellipsis', 'EnvironmentError', 
    'Exception', 'FloatingPointError', 'IOError', 'ImportError', 'IndexError', 
    'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError', 
    'None', 'NotImplementedError', 'OSError', 'OverflowError', 'RuntimeError', 
    'StandardError', 'SyntaxError', 'SystemError', 'SystemExit', 'TypeError', 
    'ValueError', 'ZeroDivisionError', '_', '__debug__', '__doc__', '__import__', 
    '__name__', 'abs', 'apply', 'buffer', 'callable', 'chr', 'cmp', 'coerce', 
    'compile', 'complex', 'delattr', 'dir', 'divmod', 'eval', 'execfile', 'exit', 
    'filter', 'float', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id', 
    'input', 'int', 'intern', 'isinstance', 'issubclass', 'len', 'list', 'locals', 
    'long', 'map', 'max', 'min', 'oct', 'open', 'ord', 'pow', 'quit', 'range', 
    'raw_input', 'reduce', 'reload', 'repr', 'round', 'setattr', 'slice', 'str', 
    'tuple', 'type', 'vars', 'xrange']
pySyntax["karrigell"]=["HIP","RESPONSE","HEADERS",
    "AUTH_USER","AUTH_PASSWORD","QUERY","SET_COOKIE","ACCEPTED_LANGUAGES",
    "SCRIPT_END","HTTP_ERROR","HTTP_REDIRECTION","SERVER_DIR",
    "Session","Authentication","Include"]
    
# compile regular expression for Python keywords
# used for syntax coloring
pyKwRE={}

for special_name in pySyntax.keys():
    kwds="\W|\W".join(pySyntax[special_name])
    pyKwRE[special_name]=re.compile(r"(\W"+kwds+r"\W)")

FONT=("Courier new",8,"normal")
root=Tk()
root.title("Python Inside HTML")

up=Frame(root)

pihZone=Frame(up)

pihLabel=Frame(pihZone)
Label(pihLabel,text="PIH source").pack(side=LEFT,anchor=W)
pihLabel.pack(anchor=W)

pihButtonZone=Frame(pihZone)
bOpen=Button(pihButtonZone,text="Open...",relief=GROOVE)
bOpen.bind("<ButtonRelease-1>",openPih)
bOpen.pack(side=LEFT)
bSave=Button(pihButtonZone,text="Save",relief=GROOVE)
bSave.bind("<ButtonRelease-1>",savePih)
bSave.pack(side=LEFT)
bParse=Button(pihButtonZone,text="Parse",relief=GROOVE)
bParse.bind("<ButtonRelease-1>",parse)
bParse.pack(side=LEFT)
pihButtonZone.pack()

pythonZone=Frame(up)

pythonLabel=Frame(pythonZone)
Label(pythonLabel,text="Parsed Python code").pack(side=TOP,anchor=E)
Label(pythonLabel,text="(Click on a line to see source)").pack(side=BOTTOM,anchor=E)
pythonLabel.pack(anchor=E)

pythonButtonZone=Frame(pythonZone)
bRun=Button(pythonButtonZone,text="Run",relief=GROOVE)
bRun.bind("<ButtonRelease-1>",run)
bRun.pack(side=LEFT)
bRunHTML=Button(pythonButtonZone,text="Make HTML",relief=GROOVE)
bRunHTML.bind("<ButtonRelease-1>",run)
bRunHTML.pack(side=LEFT)
pythonButtonZone.pack()

pihZone.pack(side=LEFT)
pythonZone.pack(side=RIGHT)
up.pack(fill=BOTH)

texts=Frame(root)
pihText=ScrolledText(texts,bg="white",height=35,width=65,font=FONT,tabs="1c",wrap=NONE)
pihText.pack(side=LEFT)
pythonText=ScrolledText(texts,bg="white",height=35,width=65,font=FONT,tabs="1c",wrap=NONE)
pythonText.pack(side=LEFT)
texts.pack()

root.mainloop()
