import os

import PyDbLite
from HTMLTags import *

db = PyDbLite.Base(os.path.join(CONFIG.serverDir,"admin","localize","translations.pdl"))
db.create("original","iso639","translation",mode="open")

for dirpath, dirnames, filenames in os.walk(CONFIG.rootDir):
    if dirpath.endswith("translations"):
        for f in [ f for f in filenames if f.startswith("translation_")
            and f.endswith(".kt") ]:
                print B(f)
                iso = os.path.splitext(f)[0][-2:]
                print iso
                lines = open(os.path.join(dirpath,f)).readlines()
                dico = dict([(lines[i].strip(),lines[i+1].strip())
                    for i in range(0,len(lines),2)])
                print TABLE(Sum([TR(TD(k)+TD(v)) for k,v in dico.iteritems()]))
                
                for k,v in dico.iteritems():
                    if not db(original=unicode(k,'utf-8'),iso639=iso):
                        db.insert(unicode(k,'utf-8'),iso,unicode(v,'utf-8'))
                    else:
                        print "duplicate translation for %s in %s" %(k,iso)
db.commit()

