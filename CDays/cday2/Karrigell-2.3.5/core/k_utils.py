import random, string, sys, os, md5, re

class LimitedDict(dict):
    """A dictionary which deletes the oldest elements if there are
    more than maxKeys keys"""
    
    def __init__(self,maxKeys):
        dict.__init__(self)
        self.maxKeys=maxKeys
        self.Keys=[]
        
    def __setitem__(self,key,value):
        dict.__setitem__(self,key,value)
        self.Keys.append(key)
        if len(self.Keys)>self.maxKeys:
            first=self.Keys.pop(0)
            del self[first]

class Node:
    """A class for a tree structure based on nodes"""

    def __init__(self,parent,name,value):
        self.parent=parent
        self.name=name
        self.value=value
        self.children=[]
        if parent:
            self.parent.addChild(self)
    
    def addChild(self,child):
        self.children.append(child)

class silent:
    """Used to replace sys.stderr and stdout on silent mode"""
    
    def write(self,data):
        pass

def generateRandom(length):
    """Return a random string of specified length
    Code by David Leung found on Active State site"""
    chars = string.ascii_letters + string.digits
    newpasswd=""
    for i in range(length):
        newpasswd = newpasswd + random.choice(chars)
    return newpasswd

def authTest(user,password,userDigest,passwordDigest):
    """Authentication test for the site administrator"""
    return (md5.new(user).digest()==userDigest \
        and md5.new(password).digest()==passwordDigest)

def applyQueryConvention(parsedQuery):
    """Returns the QUERY dictionary, similar to the result of cgi.parse_qs
    except that :
    - if the key ends with [], returns the value (a Python list)
    - if not, returns a string, empty if the list is empty, or with the
    first value in the list"""
    res={}
    for item in parsedQuery.keys():
        value=parsedQuery[item] # a Python list
        if item.endswith("[]"):
            res[item[:-2]]=value
        else:
            if len(value)==0:
                res[item]=''
            else:
                res[item]=value[0]
    return res

class CI_dict(dict):
    """Dictionary with case-insensitive keys
    Used for the RESPONSE variable in KarrigellRequestHandler
    """

    def __init__(self, dico):
        self._ci_dict = {}
        self._or_keys = {}
        for k in dico.keys():
            self._ci_dict[k.lower()] = dico[k]
            self._or_keys[k.lower()] = k
        
    def get(self,key,default=""):
        return self._ci_dict.get(key.lower(),default)
    
    def __getitem__(self,key):
        return self._ci_dict[key.lower()]
    
    def __setitem__(self,key,value):
        self._ci_dict[key.lower()] = value
        self._or_keys[key.lower()] = key
    
    def __contains__(self,key):
        return key.lower() in self._ci_dict

    def keys(self):
        return self._or_keys.values()

    def values(self):
        return self._ci_dict.values()
    
    def items(self):
        return [ (k,self._ci_dict[k.lower()]) for k in self.keys() ]

    def has_key(self,key):
        return self._ci_dict.has_key(key.lower())

    def __str__(self):
        return str(dict(self.items()))

    def __repr__(self):
        return repr(dict(self.items()))

meta_ct_pattern = re.compile('<\s*?META\s+?http-equiv.*?content-type.*?>',re.I)
def has_meta_ct(html_txt):
    """Searches if the html in html_txt has a META Content-type"""
    return meta_ct_pattern.search(html_txt)

def exists(path):
    """Like os.path.exists, but on Windows trailing dots are ignored"""
    if not os.path.exists(path):
        return False
    elif path.endswith('.'):
        if os.path.basename(path) in os.listdir(os.path.dirname(path)):
            return True
        else:
            return False
    else:
        return True

def urlInPaths(url,pathList):
    """Test if a url is in one of the paths in pathList, or in
    a subpath of one of them
    Return a tuple(path,depth) where path is the path
    or None, and depth is the number of subpaths where url stands below
    the path, or None
    """
    for path in pathList:
        if url.startswith(path):
            rest = url[len(path):]
            if rest.startswith('/'):
                rest = rest[1:]
            depth = rest.count('/')
            return path,depth
    return None,None

def pathInDirs(path,dirList):
    """Test if a path is in one of the directories in dirList, or in
    a subdirectory of one of them
    Return a tuple(directory,depth) where directory is the directory
    or None, and depth is the number of subdirs where path stands below
    the directory, or None
    """
    d = path
    if os.path.isfile(d):
        d = os.path.dirname(d)
    depth = 0
    while True:
        if d in dirList:
            return (d,depth)
        else:
            if d == os.path.dirname(d):
                return (None,None)
            else:
                d = os.path.dirname(d)
                depth += 1

#   Give each client a different standard output

import cStringIO

stdout_objs={}

class Stdout:

    def __init__(self,client_address):
        self.client = client_address
        stdout_objs[client_address]=cStringIO.StringIO()
        
    def write(self,arg):
        stdout_objs[self.client].write(arg)
        
    def getvalue(self):
        return stdout_objs[self.client].getvalue()

def trace(data):
    sys.stderr.write(str(data)+"\n")

import datetime
def log(line,_dir=None):
    if _dir is None:
        _dir = os.getcwd()
    path = os.path.join(_dir,"logs.txt")
    try:
        out = open(path,"a")
    except IOError:
        out = open(path,"w")
    out.write(datetime.datetime.now().strftime("[%d-%m-%y %H:%M:%S] ")+str(line)+"\n")
    out.close()

error_message_format="""\
    <head>
    <title>Error response</title>
    </head>
    <body>
    <h1>Error response</h1>
    <p>Error code %(code)d.
    <p>Message: %(message)s.
    <p>Error code explanation: %(code)s = %(explain)s.
    <p><i>Karrigell %(version)s - %(time)s</i>
    </body>
    """

if __name__=='__main__':
    # test CI_dict
    d = CI_dict({'One':1})
    print d.keys()
    print d.values()
    print d.items()
    print d
    print d['one'], d['oNE']
    d['OnE'] = 2
    print d
    d['two'] = 2
    print d
    
    # test exists
    print exists('k_utils.py')
    print exists('k_utils.py...')
    
    # test meta content type
    src = open(r'..\webapps\demo\tour.htm').read()
    print src[:100]
    print has_meta_ct(src)
    