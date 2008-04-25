import PyDbLite

db=PyDbLite.Base('records.pdl')
db.create("title","artist",mode="open")

def index():
    if len(db):
        Include("../recordsHeader.pih",title="My record collection")
        print '<h1>My record collection</h1>'
        print '<table class="main" cellpadding="3" cellspacing="0">'
        print '<tr><th>Title</th><th>Artist</th>'
        print '<th>&nbsp;</th><th>&nbsp;</th></tr>\n'
        for record in db:
            print '<tr>'
            print '<td class="main">%s</td><td class="main">%s</td>' %(record['title'],record['artist'])
            print '<td class="main"><a href="removeRecord?recordId=%s">' %record['__id__']
            print 'Remove</a></td>'
            print '<td class="main"><a href="editRecord?recordId=%s">' %record['__id__']
            print 'Edit</a></td>'
            print '</tr>'
        print '</table>'
    else:
        print "No record in this collection"

    print '<p><a href="editRecord?recordId=-1">New record</a>'
    print '</body>\n</html>'

def editRecord(recordId):
    recordId=int(recordId)
    if recordId>-1:
        record=db[recordId]
        title,artist=record['title'],record['artist']
        Include("../recordsHeader.pih",title="Editing record %s" %recordId)
        print "<h1>Editing a record</h1>"
    else:
        title,artist='',''
        Include("../recordsHeader.pih",title="New record")
        print "<h1>New record</h1>"
    
    print '<form action="insertRecord">'

    print '<input type="hidden" name="recordId" value="%s">' %recordId
    print '<table>'
    print '<tr><td>Title</td><td><input name="title" size="40" value="%s"></td></tr>' %title
    print '<tr><td>Artist</td><td><input name="artist" size="40" value="%s"></td></tr>' %artist
    print '</table>'
    print '<input type="submit" value="Ok">'
    print '</form>'
    print '</body>\n</html>'

def insertRecord(recordId,title,artist):
    recordId=int(recordId)
    if recordId==-1:
        db.insert(title=title,artist=artist)
    else:
        db.update(db[recordId],title=title,artist=artist)
    db.commit()
    raise HTTP_REDIRECTION,"index"

def removeRecord(recordId):
    del db[int(recordId)]
    db.commit()
    raise HTTP_REDIRECTION,"index"
