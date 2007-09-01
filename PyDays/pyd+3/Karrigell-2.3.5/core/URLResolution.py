"""Resolution of URL into a file path
Depending on infos provided in .ini file"""

import sys, os, string, urllib, cgi, posixpath
import k_utils
import k_config
from k_encodings import k_encoding

alias=k_config.alias

class DuplicateIndexError(Exception):

    def __init__(self,indexFiles):
        self.indexFiles=indexFiles
    
    def __str__(self):
        return str(self.indexFiles)

class NoIndexError(Exception):
    pass

class DuplicateExtensionError(Exception):

    def __init__(self,msg):
        self.path=msg[0]
        self.extFiles=[ os.path.basename(fileName) for fileName in msg[1] ]
    
    def __str__(self):
        info="%s files matching path %s, with extensions : " %(len(self.extFiles),self.path)
        info+=", ".join(self.extFiles)
        return info

class NoExtensionError(Exception):
    pass

def split_query(path):
    # if there is a Query String in path, return (path without qs, qs)
    path_without_qs,qs=path,''
    if path.find('?')>=0:
        [path_without_qs,qs]=path.split("?",1)
    return path_without_qs,cgi.parse_qs(qs,1)

def translate_path(path):
    """Overrides SimpleHTTPServer's translate_path to handle aliases
    Returns the path to a file name"""
    path = posixpath.normpath(urllib.unquote(path))
    path = path[len(k_config.base):]    # remove base beginning the url
    words = path.split('/')
    words = filter(None, words)

    # for scripts, path ends at the word ending with the script extension
    w1,w2=[],[]
    for i,word in enumerate(words):
        w1.append(word)
        ext = os.path.splitext(word)[1]
        if ext and ext[1:] in k_config.handled_extensions:
            w2=words[i+1:]
            break
    words=w1
    if words and words[0] in alias.keys():
        path=os.path.normpath(alias[words[0]])
        path=os.path.join(alias[words[0]],string.join(words[1:],"/"))
    else:
        path=os.path.join(k_config.rootDir,string.join(words,"/"))
    return os.path.normpath(path)

def getScriptElements(path):
    """If the path contains a script name, return a list with the
    script name first and the remaining url parts after"""

    path = posixpath.normpath(urllib.unquote(path))

    path_encoding = k_encoding.try_encoding(path, 
           ['ascii', 'utf-8', 'iso8859_1_ncc', 'cp1252', 'macroman'])
    if not path_encoding:
        # very broken browser or something is wrong
        # remove the non ascii characters and hope that at least
        # the name of function is ok
        path = ''.join([x for x in path if ord(x)<128])
        path_encoding = 'ascii'
    upath = unicode(path, path_encoding)

    words = upath.split('/')
    words = filter(None, words)
    # for scripts, path ends at the word ending with the extension
    w1,w2=words,[]
    for i,word in enumerate(words):
        for mod in k_config.handled_extensions:
            if word.lower().endswith("."+mod):
                w2=words[i+1:]
                w1=words[:i]
    return "/".join(w1)+"/",w2

def indexFile(dirPath):
    """Search for a file index.html, .htm, .py, .pih or .hip
    in the directory dirPath. If several index files are found,
    raise a DuplicateIndexError exception"""
    indexFiles=[]
    for index in [ "index.%s" %ext for ext in ("html", "htm", "py", "pih", "hip", "ks") ]:
        fullIndex = os.path.join(dirPath, index)
        if os.path.exists(fullIndex):
            indexFiles.append(index)
    if not indexFiles:
        raise NoIndexError
    if len(indexFiles) > 1:
        raise DuplicateIndexError,indexFiles
    return indexFiles[0]

def search(path_without_qs,fileName):
    """Search a file with name fileName and extension
    in htm, html, py, pih, hip, ks"""
    extFiles=[]
    for ext in "html", "htm", "py", "pih", "hip", "ks":
        fullName = "%s.%s" %(fileName, ext)
        if os.path.exists(fullName):
            extFiles.append("."+ext)
    if not extFiles:
        raise IOError,"No script found for url %s" %path_without_qs
    if len(extFiles) > 1:
        raise DuplicateExtensionError,[path_without_qs,extFiles]
    return extFiles[0]

def trace(data):
    sys.stderr.write("%s\n" %data)
