from HTMLTags import *
import guess_type

# uncomment next line with the db declaration, like
#import PyDblite
import PyDbLite as PyDbLite
db = PyDbLite.Base("test.pdl").create("name","location","age",mode="open")

# specify field full names in a dictionary
fnames = dict((k,k) for k in db.fields)
#fnames.update({"Name":"Object name"}) # full names

# number of records per page
nbrecs = 20

style = STYLE("""body,td,th {font-family:sans-serif;
    font-size:13}
h2 {font-family: sans-serif;}

th { font-weight: bold; 
    background-color: #D0D0D0;
}
a.navig {background-color:#FF0088;
    text-decoration:none;}
""",Type="text/css")

def _header(title):
    return HEAD(TITLE(title)+style)

def index(start=0):
    print _header("List")
    body = H2("List")
    start=int(start)
    f1=f2=TEXT("&nbsp;")
    if not start==0:
        f1 = A("< Previous",Class="navig",href="index?start=%s" %(start-nbrecs))
    if not start+nbrecs>=len(db):
        f2 = A("Next >",href="index?start=%s" %(start+nbrecs),Class="navig")
    navig = TABLE(TR(TD(f1)+TD(f2,align="right")))

    lines = TR(Sum(TH(fnames[f]) for f in db.fields)+TD("&nbsp;"))
    recs = db()[start:start+nbrecs]
    for r in recs:
        lines += FORM(INPUT(Type="hidden",name="__id__",value=r["__id__"])+
            INPUT(Type="hidden",name="__version__",value=r["__version__"])+
            TR(Sum([TD(INPUT(name=k,value=r[k]),Class="cell") 
                for k in db.fields]) +
            TD(INPUT(Type="submit",value="Update"))),
            action="insert",method="post")
    new = A("New record",href="new")
    print BODY(body+navig+TABLE(lines)+BR(new))

def new():
    print _header ("New record")
    title = H2("New record")
    hidden = INPUT(name="__id__",Type="hidden",value=-1)
    lines = []
    for key in db.fields:
        lines.append(TR(TD(fnames[key])+TD(INPUT(name=key))))
    lines.append(TR(TD(INPUT(Type="submit",value="Ok"),colspan="2")))
    lines = title + FORM(hidden+TABLE(Sum(lines)),action="insert",method="post")
    print lines

def delete(recid):
    print _header("Delete record")
    print H2("Delete this record ?")
    record = db[int(recid)]
    print TABLE(Sum([TR(TH(f)+TD(record[f])) for f in db.fields]))
    print A("Yes",href="confirm_delete?recid=%s" %recid)
    print A("No",href="index")

def confirm_delete(recid):
    del db[int(recid)]
    db.commit()
    raise HTTP_REDIRECTION,"index"

def insert(**kw):
    recid = int(kw["__id__"])
    kw["__version__"] = int(kw.get("__version__",1))
    del kw["__id__"]
    for field in db.fields:
        kw[field] = guess_type.guess_type(kw.get(field,"")) or None
    if recid >= 0:
        r = db[recid]
        # concurrency control
        if r.setdefault("__version__",-1) != int(kw["__version__"]):
            raise Exception,"Can't update the record, "\
                "it was modified since you selected it"
        db.update(r,**kw)
    else:
        db.insert(**kw)
    db.commit()
    raise HTTP_REDIRECTION,"index"
