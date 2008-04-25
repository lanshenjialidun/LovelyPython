
import os

from HTMLTags import *
import k_config
import PyDbLite

db = PyDbLite.Base(os.path.join(k_config.serverDir,"admin","users.pdl"))
db.create("login","passwd","role",mode="open")

roles = ["admin","edit","visit"]

def header(title,src='../default.css'):
    h = TITLE(title)
    if src:
        h += LINK(rel="stylesheet",href=src)
    return HEAD(h)

def admin_login():
    print HEAD(TITLE("Administrator authentication"))
    lines = TR(TD("Login")+TD(INPUT(name="login")))
    lines += TR(TD("Password")+TD(INPUT(name="passwd",Type="password")))
    lines += TR(TD(INPUT(Type="submit",value="Ok"),colspan="2"))
    print BODY(FORM(TABLE(lines),action="check_login",method="post"))

def check_login(login,passwd):
    import md5
    digest=open("admin.ini","rb").read()
    userDigest=digest[:16]
    passwordDigest=digest[16:]

    if (md5.new(login).digest()==userDigest \
            and md5.new(passwd).digest()==passwordDigest):
        SET_COOKIE["admin"] = passwordDigest
        raise HTTP_REDIRECTION,"index"
    else:
        print "Authentication failed"

def index():

    # check if user is the administrator
    if not COOKIE.has_key("admin"):
        raise HTTP_REDIRECTION,"admin_login"
    else:
        adm_digest=open("admin.ini","rb").read()[16:]
        if not COOKIE["admin"].value == adm_digest:
            raise HTTP_REDIRECTION,"admin_login"

    print header("Utilisateurs")
    print H2("Liste des utilisateurs")
    print "<table>"
    print TR(Sum([TH(f) for f in db.fields])+TD("&nbsp;"))
    for r in db:
        print TR(Sum([TD(r.get(k)) for k in db.fields]) +
            TD(A("Editer",href="edit?recid=%s" %r["__id__"]))
            )
    print "</table>"
    print P()+A("Nouveau",href="edit")

def edit(recid=-1):
    recid = int(recid)
    if recid>=0:
        r = db[int(recid)]
        print header("Edition")
    else:
        r = {}
        print header("Nouveau")
    print "<table>"
    print '<form action="insert" method="post">'
    print INPUT(name="recid",Type="hidden",value=recid)
    print TR(TD("Identifiant")+
        TD(INPUT(name="login",value=r.get("login",""))))
    print TR(TD("Mot de passe")+
        TD(INPUT(name="passwd",Type="password",value=r.get("passwd",""))))

    print TD("Rôle")
    croles = Sum([INPUT(name="role",Type="radio",value=role,
            checked = r.get("role","")==role)+TEXT(role)+BR() for role in roles])
    print TD(croles)

    print TR(TD(INPUT(Type="submit",value="Ok"),colspan="2"))
    print '</form></table>'
    if recid>=0:
        print P()+A("Supprimer",href="delete?recid=%s" %r["__id__"])

def delete(recid):
    print header("Suppression")
    print "Suppression de %s ?" %db[int(recid)]
    print A("Oui",href="confirm_delete?recid=%s" %recid)
    print A("Non",href="index")

def confirm_delete(recid):
    del db[int(recid)]
    db.commit()
    raise HTTP_REDIRECTION,"index"

def insert(**kw):
    recid = int(kw["recid"])
    del kw["recid"]
    if recid >= 0:
        r = db[recid]
        db.update(r,**kw)
    else:
        db.insert(**kw)
    db.commit()
    raise HTTP_REDIRECTION,"index"
    