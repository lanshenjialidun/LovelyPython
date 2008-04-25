import os
import random
import datetime
import string

from PyDbLite import Base

def word(m):
    res = ''
    ln = random.randint(1,m)
    for i in range(ln):
        res += random.choice(string.letters)
    return res

def sentence(n,m):
    ln = random.randint(1,n)
    res = []
    for i in range(ln):
        res.append(word(m))
    return ' '.join(res)
    
os.remove('blog')
db = Base('blog').create('parent','title','author','text','date')
db.create_index('parent')

nbthreads = 200
for i in range(nbthreads):
    # generate thread
    author = 'pierre'
    title = sentence(10,10)
    text = sentence(100,10)
    date = datetime.datetime(random.randint(2004,2006),random.randint(1,12),
        random.randint(1,28),random.randint(0,23),random.randint(0,59),
        random.randint(0,59))
    thread_id = db.insert(parent=-1,author=author,title=title,text=text,date=date)

    # generate comments
    nbcomments = random.randint(0,5)
    for i in range(nbcomments):
        author = word(10)
        text = sentence(50,10)
        tdelta = datetime.date(2007,1,1) - date.date()
        c_date = date + datetime.timedelta(random.randint(1,tdelta.days))
        c_date = datetime.datetime(c_date.year,c_date.month,c_date.day,
            random.randint(0,23),random.randint(0,59),
            random.randint(0,59))
        db.insert(parent=thread_id,author=author,title=title,text=text,date=c_date)
db.commit()
