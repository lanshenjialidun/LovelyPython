import os
from PyDbLite import Base

db = { 'users':Base(os.path.join(os.getcwd(),'data','users.pdl')), 
    'news':Base(os.path.join(os.getcwd(),'data','news.pdl')) }
db['users'].create('login','password','bgcolor','fontfamily',
    mode="open")
db['news'].create('login','title','body','date',mode="open")