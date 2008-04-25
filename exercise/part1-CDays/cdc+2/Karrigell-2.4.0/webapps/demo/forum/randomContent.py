"""Generates a random forum content"""

import sys, string, re
sys.path.append("../..")
import RandomText
import gadflyStorage, random, forumClasses
import time

now=time.time()
msgNb=1000	# number of messages
authNb=30	# number of authors

t=open(r"c:\cygwin\home\e_vrenigenn_diwezhan.txt").read()
t=re.sub("\[.*\]","",t)

c=RandomText.RandomText(t,5)

parents=[-1]
authors=[]
db=gadflyStorage.Storage("messages","n")

for i in range(authNb):
	authors.append(c.sentence(8,1,string.whitespace+string.punctuation).strip())

nb=0
titles={}
msgs={}
step=0

msgs[step]=[]
# first step
parent=-1
nbchildren=50
for i in range(nbchildren):
	author=random.choice(authors)
	title=c.sentence(20,mode=1,startAfter=string.whitespace+string.punctuation).strip()
	content=c.sentence(random.randrange(300),mode=2)
	msg=forumClasses.Message(author,title,content,parent)
	msg.date=time.localtime(now-random.randrange(1000000))
	db.write(msg)
	msg.thread=msg.__id__
	titles[msg.__id__]=title
	msgs[step].append(msg)

db.set_key("__id__")
for msg in db.find():
	msg.thread=msg.__id__

	db[msg.__id__]=msg

db.commit()

def genChildren():
	global nb,step
	msgs[step+1]=[]
	for msg in msgs[step]:
		parent=msg.__id__
		thread=msg.thread
		t=time.mktime(msg.date)
		nbchildren=random.randrange(2/(step+1),6)
		for i in range(nbchildren):
			author=random.choice(authors)
			title="Re: "+titles[parent]
			content=c.sentence(random.randrange(300),mode=2)
			msg=forumClasses.Message(author,title,content,parent,thread)
			msg.date=time.localtime(t+random.randrange(int(now-t)))
			db.write(msg)

			msgs[step+1].append(msg)
			titles[msg.__id__]=title
			nb+=1

while nb<msgNb:
	genChildren()
	print "step %s nb %s" %(step,nb)
	step+=1
	
db.commit()

def countChildren(msg):
	global nb
	try:
		ch=db[msg.__id__]
		if type(ch)==type([]):
			#nb+=len(ch)
			for c in ch:
				nb+=1
				countChildren(c)
		else:
			nb+=1
			countChildren(ch)
	except gadflyStorage.StorageError:
		return 0
	return nb

db.set_key("parent")
heads=db[-1]
print heads

db.set_key("thread")
for msg in heads:
	msg.numChildren=len(db.find(where="thread=%s" %msg.__id__))
	print msg.title,msg.numChildren
	db.update(msg,where="__id__=%s" %msg.__id__)

db.commit()
