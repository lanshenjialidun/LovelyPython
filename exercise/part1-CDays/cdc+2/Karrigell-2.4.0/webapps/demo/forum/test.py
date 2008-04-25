import time
import locale
import ConfigParser
import datetime
import PyDbLite

locale.setlocale(locale.LC_ALL,'')

db = PyDbLite.Base('entries')

db.open()

print db.indices["thread"]

r = db[2]
print r["thread"]
db.update(r,thread=1)
print db.indices["thread"]
