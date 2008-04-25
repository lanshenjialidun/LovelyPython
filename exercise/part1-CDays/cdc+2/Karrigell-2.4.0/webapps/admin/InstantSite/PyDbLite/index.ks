import os
import PyDbLite
from HTMLTags import *

def index():
    print HEAD(LINK(rel="stylesheet",href="../default.css"))
    existing = [ db for db in os.listdir(os.path.join(os.getcwd(),"applications"))
        if db.endswith(".pdl") ]
    lines = [H3("PyDbLite management")]
    if existing:
        lines += [TEXT("Existing databases")]
    lines += [BR(A(db,href="edit?db=%s" %os.path.splitext(db)[0])) for db in existing]
    lines += [FORM(TEXT("New database")+INPUT(name="db")+
        INPUT(Type="submit",name="new",value="Ok"),
        action="edit",method="post")]
    print BODY(Sum(lines))

def edit(**kw):
    print HEAD(LINK(rel="stylesheet",href="../default.css"))

    db_name = kw["db"]
    path = os.path.join(os.getcwd(),"applications",db_name)+".pdl"
    db = PyDbLite.Base(path)
    path = os.path.join(os.getcwd(),"applications",db_name)+".conf"
    info = PyDbLite.Base(path)
    if "new" in kw: # new database
        db.create()
        db.commit()
        info.create("field","empty",mode="override")
        info.commit()
    else:
        db.open()
        info.open()

    db_name = os.path.splitext(os.path.basename(db.name))[0]

    fields = [TR(TD(H3(_("Current fields")),colspan=4))]
    fields += [TR(TH(_("Field name"))+TH(_("Can be empty"))+TD("&nbsp;")*3)]
    for f in db.fields:
        field_info = info(field=f)
        if field_info:
            empty = field_info[0]["empty"]
        else:
            empty = True
        line = TR(TD(f)+
            TD(TEXT("yes")+
               INPUT(Type="radio",name="empty",value=1,checked=empty is True)+
               TEXT("no")+
               INPUT(Type="radio",name="empty",value=0,checked=empty is False))+
            TD(INPUT(Type="submit",name="subm",value=_("Update")))+
            TD(A(_("Drop field"),href="update?subm=Drop&db=%s&field=%s"
                %(db_name,f))))
        fields += [FORM(INPUT(Type="hidden",name="db",value=db_name)+
            INPUT(Type="hidden",name="field",value=f)+ line,
            action="update",method="post")]
    fields += [TR(TD(H3(_("Add new field")),colspan=4))]
    fields += [TR(TH(_("Field name"))+TH(_("Can be empty"))+TH("Default value")+TD("&nbsp;"))]
    new_field = FORM(INPUT(Type="hidden",name="db",value=db_name)+
        TR(TD(INPUT(name="field"))+
            TD(TEXT("yes")+INPUT(Type="radio",name="empty",value=1,checked=True)+
               TEXT("no")+INPUT(Type="radio",name="empty",value=0))+
            TD(INPUT(name="default"))+
               TD(INPUT(Type="submit",value="New"))),
        action="new_field",method="post")
    fields += [new_field]

    lines = [A("PyDbLite management",href="index")]
    lines += [H2("Editing base %s" %db_name)]
    lines += [TABLE(Sum(fields))]

    lines += [A("Generate script",href="gen_script?db=%s" %db_name)]
    
    print BODY(Sum(lines))

def new_field(field,empty,default,db):
    path = os.path.join(os.getcwd(),"applications",db)+".pdl"
    pydb = PyDbLite.Base(path).open()
    pydb.add_field(field,default=default or None)
    raise HTTP_REDIRECTION,"edit?db=%s" %db

def update(subm,field,empty,db):
    if subm.startswith("Drop"): # drop field
        path = os.path.join(os.getcwd(),"applications",db)+".pdl"
        pydb = PyDbLite.Base(path).open()
        pydb.drop_field(field)
    else:
        # update info database
        path = os.path.join(os.getcwd(),"applications",db)+".conf"
        info = PyDbLite.Base(path).create("field","empty",mode="open")
        rec = info(field=field)
        empty = bool(int(empty))
        if rec:
            info.update(rec[0],empty=empty)
        else:
            info.insert(field,empty)
        info.commit()
    raise HTTP_REDIRECTION,"edit?db=%s" %db

def gen_script(db):
    path = os.path.join(os.getcwd(),"applications",db)+".pdl"
    pydb = PyDbLite.Base(path).open()
    path = os.path.join(os.getcwd(),"applications",db)+".conf"
    info = PyDbLite.Base(path).create("field","empty",mode="open")
    not_empty_fields = [ r["field"] for r in info(empty=False) ]

    params = {'db_name':'"%s"' %(db+'.pdl'),
        'db_fields':','.join(['"%s"' %name for name in pydb.fields]),
        'db_engine':'PyDbLite',
        'not_empty':','.join(['"%s"' %name for name in not_empty_fields])}

    _in = open("generic.tmpl","rb").read()
    ks = _in %params

    out = open(os.path.join(os.getcwd(),"applications",db)+".ks","w")
    out.write(ks)
    _in = open("generic.ks","rb").read()
    out.write(_in)
    out.close()

    print "Management script generated. "
    print A("Test it",href="../applications/%s.ks" %db)

def layout(db):
    path = os.path.join(os.getcwd(),"applications",db)+".pdl"
    pydb = PyDbLite.Base(path).open()
    db_name = os.path.splitext(os.path.basename(pydb.name))[0]
    menu.menu(db_name,"index.ks/layout")
    print pydb.fields
    