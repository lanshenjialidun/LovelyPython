import time
import locale
import ConfigParser
import datetime
from HTMLTags import *

import forumDb
db = forumDb.db

locale.setlocale(locale.LC_ALL,'')

print HEAD(TITLE("Karrigell forum demo")+
    LINK(rel="stylesheet",Type="text/css",href="../forum.css")+
    SCRIPT(src="../forum.js"))

def display(i,msg):
    if i % 2:
        print '<tr class="even">'
    else:
        print '<tr class="odd">'
    print '<td><a href="thread_frame?thread=%s">%s</a> (%s %s)' \
        %(msg["__id__"],msg["title"],msg["numChildren"],_('answers'))
    if Role():
        print '<a href="remove_thread?msgid=%s"><small>Remove</small></a>' \
            %msg["__id__"]
    print '</td>'
    print '<td>%s</td>' %msg["author"]
    print '<td>%s</td>' %msg["lastDate"].strftime('%x %H:%M')
    print '</tr>'

def index():
    print '<body>'
    threads=db._parent[-1]
    threads.sort(lambda x,y: cmp(y["lastDate"],x["lastDate"]))

    print A(IMG('',src="../../../doc/images/karrigell_skeudenn.png", border="0", width="100"),
        href="../../../")
    print H3(_("Karrigell forum demo"))
    print A(_("Start new thread"), href='new_thread')
    print P()
    print '<table class="forum">'
    print TR(TD("Title")+TD("By")+TD("Date"),Class="title")

    for i,msg in enumerate(threads):
        display(i,msg)

    print '</table>'
    print P()
    if Role() is not None:
        print Logout()
    else:
        print '<a href="login"><small>Admin</small></a>'
    print '</body>'

def login():
    import urlparse
    Login(role=["admin"],path=urlparse.urljoin(THIS.url,"index"))

def logout():
    Logout()
    
def new_thread():
    print '<body>'
    print H3(_("New message"))
    print '<table>'
    print FORM(INPUT(Type="hidden",name="parent",value="-1")+
        TR(TD(_("Your name"))+TD(INPUT(name="author")))+
        TR(TD(_("Title"))+TD(INPUT(name="title")))+
        TR(TD(_("Your message"),valign="top")+
            TD(TEXTAREA(name="content",rows="20",cols="80")))+
        TR(TD(INPUT(Type="submit",value="Ok"),colspan="2")+
           TD(INPUT(Type="button",value=_("Cancel"),
                onClick="location.href='index';"),align="right")
        ),
        action="save_message",method="post")
    print '</table></body>'

def save_message(parent,author,title,content):
    parent=int(_parent)
    # what thread does this message belong to ?
    if parent!=-1:
        thread=db[parent]["thread"]
    else:
        thread=-1

    # insert the message, return its id
    date=datetime.datetime.today()
    new_id = db.insert(parent=parent,thread=thread,author=_author,
        title=_title,content=_content,date=date,lastDate=date,
        numChildren=0)

    # increment number of children of all the parents of this message
    msg = None
    while parent!=-1:
        msg=db[parent]
        db.update(msg,numChildren = msg["numChildren"]+1)
        parent=msg["parent"]

    if thread == -1:
        db.update(db[new_id],thread=new_id)
    else:
        # update lastDate of the first message in the thread
        db.update(msg,lastDate=date)

    db.commit()
    raise HTTP_REDIRECTION,"index"

def thread_frame(thread):
    print FRAMESET(FRAME(name="right",src="thread_menu?thread=%s" %thread)+
            FRAME(name="right",src="../showThreadMessages.pih?thread=%s" %thread),
        cols="25%,*")

def thread_menu(thread):
    print SCRIPT("selectedMsg = null")

    def display_line(msg,indent):
        print '<br>%s<a class="msg" href="thread_messages?thread=%s#%s" target="right">%s</a>' \
            %("&nbsp;"*indent*2,thread,msg["__id__"],msg["author"])
        print '<small> %s</small>' %msg["date"].strftime('%x')
        if Role() and msg["parent"] != -1:
            print '<a href="remove_msg?msgid=%s&thread=%s" target="_top">' \
                %(msg["__id__"],_thread)
            print '<small>Remove</small></a>'

    def compDate(msg1,msg2):
        return cmp(msg1["date"],msg2["date"])

    def showThread(msg,indent):
        # shows the thread beginning at msg
        # only one line per message, indented
        #global indent
        display_line(msg,indent)
        res=[]
        res=[ m for m in threadMsgs if m["parent"]==msg["__id__"] ]   
        res.sort(compDate)
        for childmsg in res:
            showThread(childmsg,indent+1)

    # retrieves all messages of the thread
    threadMsgs=db._thread[int(_thread)]

    # root of the thread
    for msg in threadMsgs:
        if msg["parent"]==-1:
            break

    rootMsg=msg

    print A(_("Back to forum"),href="index",target="_top")
    print P()+B(rootMsg["title"])
    showThread(rootMsg,1)

answers = 0
def remove_msg(msgid,thread):
    def removeChildren(msg):
        global answers
        children = db._parent[msg["__id__"]]
        del db[msg["__id__"]]
        answers += 1
        for child in children:
            removeChildren(child)

    msg = db[int(_msgid)]
    removeChildren(msg)

    # decrement number of replies
    while True:
        parent = msg["parent"]
        if parent == -1:
            break
        p = db[parent]
        new_nc = p["numChildren"] - answers
        db.update(p,numChildren=new_nc)
        msg = p

    db.commit()
    raise HTTP_REDIRECTION,'thread_frame?thread=%s' %thread

def remove_thread(msgid):
    def removeChildren(msg):
        children = db._parent[msg["__id__"]]
        del db[msg["__id__"]]
        for child in children:
            removeChildren(child)

    msg = db[int(msgid)]
    removeChildren(msg)
    db.commit()

    raise HTTP_REDIRECTION,'index'