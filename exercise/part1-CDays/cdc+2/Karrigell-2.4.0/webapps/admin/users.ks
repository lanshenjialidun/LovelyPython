import os

from HTMLTags import *
import k_config
import PyDbLite

db = PyDbLite.Base(os.path.join(CONFIG.serverDir,"data","users.pdl"))
db.create("host","login","password","role","session_key","nb_visits",
    "last_visit",
    mode="open")

db_roles = PyDbLite.Base(os.path.join(CONFIG.serverDir,"data","roles.pdl")).open()
roles = [r["role"] for r in db_roles()]

def _header(title,src):
    return HEAD(TITLE("title")+
        LINK(rel="stylesheet",href=src))

def index():

    Login(role=["admin"])

    print _header(_("Users management"),src="../users.css")

    t = A(_("Home"),href="../index.ks")+H2(_("Users for host %s") %HOST)

    lines = TR(TH("Login")+TH("Password")+TH("Role")+
        TH("Session key")+TH("Nb visits")+TH("Last visit")+TD("&nbsp;"))

    for r in db(host=HOST):
        lines += TR(Sum([TD(r.get(k)) for k in db.fields[1:]]) +
            TD(A("Edit",href="edit?recid=%s" %r["__id__"]))
            )

    print BODY(A(_("Admin"),href="/admin")+
        t+TABLE(lines)+P()+A(_("New user"),href="edit")+
        P()+A(_("Manage users roles"),href="../roles.ks"))

def edit(recid=-1):
    recid = int(recid)
    if recid>=0:
        r = db[int(recid)]
        print _header("Edition",src="../users.css")
        print H2("Edition")
    else:
        r = {"role":"visit"}
        print _header("New user",src="../users.css")
        print H2("New user")
    print "<table>"
    print '<form action="insert" method="post">'
    print INPUT(name="recid",Type="hidden",value=recid)
    print TR(TD("Login")+
        TD(INPUT(name="login",value=r.get("login",""))))
    print TR(TD("Password")+
        TD(INPUT(name="password",Type="password",value=r.get("passwd",""))))

    print TD("Role")
    croles = Sum([INPUT(name="role",Type="radio",value=role,
            checked = r.get("role","")==role)+TEXT(role) for role in roles])
    print TD(croles)

    print TR(TD(INPUT(Type="submit",value="Ok"),colspan="2"))
    print '</form></table>'
    if recid>=0:
        print P()+A("Delete",href="delete?recid=%s" %r["__id__"])

def delete(recid):
    print _header("Delete",src="../users.css")
    print "Delete %s ?" %db[int(recid)]["login"]
    print A("Yes",href="confirm_delete?recid=%s" %recid)
    print A("No",href="index")

def confirm_delete(recid):
    del db[int(recid)]
    db.commit()
    raise HTTP_REDIRECTION,"index"

def insert(**kw):
    for field in ["login","password"]:
        if not kw.get(field,""):
            print _("Error - field %s empty" %field)
            print BR(A(_("Back"),href="javascript:window.history.back()"))
            raise SCRIPT_END
    recid = int(kw["recid"])
    del kw["recid"]
    if recid >= 0:
        r = db[recid]
        db.update(r,**kw)
    else:
        kw["nb_visits"] = 0
        kw["host"] = HOST
        db.insert(**kw)
    db.commit()
    raise HTTP_REDIRECTION,"index"
    