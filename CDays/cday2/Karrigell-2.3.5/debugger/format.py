"""The function format(fileName, data, line) takes a file name,
data (usually the content of the file) and a line number,
and returns an HTML code with syntax highlighting"""

import re
import os
import pythonParser
import cStringIO
import cgi

def addTag(match):
    chunk=match.string[match.start()+2:match.end()-2]
    outStream=cStringIO.StringIO()
    pythonParser.Parser(chunk,None,out=outStream).format(None)
    return "<i>&lt;%"+outStream.getvalue()+"%&gt;</i>"

def render(in_data,showLine):
    output=[]
    for lineNum,line in enumerate(in_data.split('\n')):
        if lineNum==showLine:
            output.append('<span class="error">%s</span>' %line)
        else:
            output.append(line)
    return output

def format(fileName, data, line=-1):
    data=data.replace('&','&amp;')
    extension = os.path.splitext(fileName)[1].lower()

    if extension == ".pih":
        print '<br>Python chunks are in <i>italic</i>'
        # replace all < by &lt; except if followed by %
        data=re.sub("<(?!%)","&lt;",data)
        # regular expression for Python chunks. Cannot be written directly with
        # < followed by % because of parsing rules of this pih file...
        pyChunkRE=re.compile("<"+"%.*?%"+">",re.DOTALL)
        data=pyChunkRE.sub(addTag,data)
        code=render(data,line)
    elif extension in [".hip",".py",".ks"]:
        outStream=cStringIO.StringIO()
        p=pythonParser.Parser(cgi.escape(data),None,out=outStream)
        p.format(showLineNums=1)
        data=outStream.getvalue()
        code=render(data,line)
    else:
        code = [ cgi.escape(line) for line in data.split('\n') ]
    return code


