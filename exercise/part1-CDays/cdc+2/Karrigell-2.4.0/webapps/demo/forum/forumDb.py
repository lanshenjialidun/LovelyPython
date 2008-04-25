import PyDbLite
db = PyDbLite.Base('entries.pdl')

db.create('parent','thread','author','title','content','date',
    'lastDate','numChildren',mode="open")
db.create_index('parent','thread')
