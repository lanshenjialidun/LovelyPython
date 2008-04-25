import datetime
import calendar
import locale
locale.setlocale(locale.LC_ALL,'')

print '<html><head>'
print '<title>Blog</title>'
print '<link rel="stylesheet" type="text/css" href="../blog.css">'
print '</head><body>'
print '<a href="../../..">'
print '<img src="/doc/images/karrigell_skeudenn.png" border="0" width="100">'
print '</a>'
print '<form action = "new_entry"><input type="submit" value="New">'
print '</form>'
print '<p>'
print '<div class="header">'
print '<div class="blogtitle">Karrigell Blog Demo</div></div>'

from PyDbLite import Base
db = Base('blog.pdl').create('parent','title','author','text','date',
    mode="open")
db.create_index('parent')

is_logged = hasattr(Session(),"blog_admin")

try:
    set([])
except NameError:
    from sets import Set as set
    
def index(year=None,month=None):
    """Print all the threads for specified month"""
    if year is None:
        today = datetime.date.today()
        year,month = today.year,today.month
    else:
        year,month = int(year),int(month)
    Session().year = year
    Session().month = month
    # get all threads
    threads = db._parent[-1]
    months = set([(t["date"].year,t["date"].month) for t in threads ])
    # only threads for current month
    threads = [ t for t in threads if t["date"].year == year
        and t["date"].month == month ]
    # sort by date
    threads.sort(lambda t1,t2:cmp(t2["date"],t1["date"]))
    days = set([t["date"].day for t in threads ])

    # print current month calendar
    print '<table cellspacing="10">'
    print '<tr><td valign="top">'
    print datetime.date(year,month,1).strftime('%B %Y')+'<br>'
    print '<pre>'
    print calendar.weekheader(3)
    for week in calendar.monthcalendar(year,month):
        ws = ''
        for day in week:
            if day == 0:
                ws += '    '
            elif day in days:
                ws += '<a class="days" href="#msg%s">%3s</a> ' %(day,day)
            else:
                ws += '%3s '%day
        print ws
    print '</pre>'
    
    print '<p>Archives'
    arch = list(months)
    arch.sort()
    for line in arch:
        d = datetime.date(line[0],line[1],1)
        print '<br><a class="archive" href="index?year=%s&month=%s">%s</a>' %(d.year,
            d.month,d.strftime('%B %Y'))
    # admin
    if is_logged:
        print '<p><small><a href="../admin.pih">Logout</a></small>'    
    else:
        print '<p><small><a href="../admin.pih">Admin</a></small>'
    print '</td>'
    
    # print threads for current month
    print '<td valign="top">'
    for r in threads:
        comments = db._parent[r["__id__"]]
        print '<a name="msg%s">' %r["date"].day
        print '<div class="day">%s</div>' %r["date"].strftime('%x')
        print '<div class="title">%s</div>' %r["title"]
        print '<p><div class="text">',r["text"],'</div>'
        print '<p><div class="posted">Posted by %s at %s' \
            %(r["author"],r["date"].strftime('%H:%M:%S'))
        if is_logged:
            print '<small><a href="remove?rec_id=%s">Remove</a></small>' %r["__id__"]
        print '</div><p><div class="posted">'
        print '<a class="comments" href="showComments?parent=%s">' \
            '%s comments</a></div><p>' %(r["__id__"],len(comments))
    print '</td></tr></table>'
    print '</body></html>'

def showComments(parent):
    parent = int(parent)
    r_parent = db[parent]
    p_date = r_parent["date"]
    comments = db._parent[parent]
    for comment in comments:
        print '<div class="title">'+comment["title"]+'</div>'
        print '<p><div class="text">'+comment["text"]+'</div>'
        print '<p><div class="posted">Posted by %s %s</div><p>' %(comment["author"],
            comment["date"].strftime('%x at %H:%M:%S'))
        if is_logged:
            print '<p><small><a href="remove?rec_id=%s">Remove</a></small>' \
                %comment["__id__"]
    print '<hr>'
    new_entry(title=r_parent["title"],parent=parent)
    print '<a href="index?year=%s&month=%s">' %(p_date.year,p_date.month)
    print 'Cancel</a>'

def new_entry(title='',parent=-1):
    print '<form action="insert_entry" method="post">'
    print '<input type="hidden" name="parent" value="%s">' %parent
    print '<table>'
    print '<tr><td>Name</td><td><input name="author"></tr>'
    print '<tr><td>Title</td><td><input name="title" size="50" value="%s"></tr>' %title
    print '<tr><td>Text</td>'
    print '<td><textarea name="text" rows="20" cols="50"></textarea></td></tr>'
    print '</table>'
    print '<input type="submit" value="Ok"></form>'

def insert_entry(**kw):
    kw['parent'] = int(kw['parent'])
    if kw['parent'] == -1:
        t_date = datetime.date.today()
    else:
        t_date = db[kw['parent']]["date"]
    kw['date'] = datetime.datetime.now()
    # replace blank lines by <p>
    kw["text"] = kw["text"].replace("\r\n\r\n","<p>")
    db.insert(**kw)
    db.commit()
    raise HTTP_REDIRECTION,"index?year=%s&month=%s" %(t_date.year,t_date.month)

def remove(rec_id):
    if is_logged:
        rec_id = int(rec_id)
        del db[rec_id]
        db.delete([r for r in db._parent[rec_id]])
        db.commit()
    raise HTTP_REDIRECTION,"index?year=%s&month=%s" \
        %(Session().year,Session().month)