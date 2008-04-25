import os
import k_pygettext
import PythonInsideHTML
import HIP

from HTMLTags import *

# compatibility with Python 2.3
try:
    set([])
except NameError:
    from sets import Set as set

strings = set([])
for dirpath, dirnames, filenames in os.walk(CONFIG.rootDir):
    for f in filenames:
        ext = os.path.splitext(f)[1]
        path = os.path.join(dirpath,f)
        if ext in [".py",".ks"]:
            pyCode=open(path).read()
        elif ext==".pih":
            pyCode=PythonInsideHTML.PIH(path).pythonCode()
        elif ext==".hip":
            pyCode=HIP.HIP(path).pythonCode()

        kpg=k_pygettext.Gettext(pyCode,f)
        strings = strings.union(set(kpg.extracts()))

print len(strings),"traductions"
print "<P>",strings

import PyDbLite
db = PyDbLite.Base(os.path.join(CONFIG.serverDir,"data","translations.pdl"))
db.open()

res = []
for s in strings:
    trans = db(original=unicode(s,'iso-8859-1'))
    if trans:
        res.append(TR(TD(s)+TD(trans[0]["iso639"])+
            TD(trans[0]["translation"].encode('iso-8859-1'))))
print TABLE(Sum(res))