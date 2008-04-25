import PyDbLite
import os

db = PyDbLite.Base(os.path.join(r"c:\cygwin\home\karrigell","data","translations.pdl"))
db.open()

res = []
for s in strings:
    trans = db(original=unicode(s,'iso-8859-1'))
    if trans:
        res.append(TR(TD(s)+TD(trans[0]["iso639"])+
            TD(trans[0]["translation"].encode('iso-8859-1'))))
print TABLE(Sum(res))