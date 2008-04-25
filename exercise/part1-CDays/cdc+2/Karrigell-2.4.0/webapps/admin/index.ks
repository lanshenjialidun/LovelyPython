import os

from HTMLTags import *
import k_utils
import PyDbLite

db = PyDbLite.Base(os.path.join(CONFIG.serverDir,"data","users.pdl"))
db.create("login","password","role","session_key","nb_visits",
    "last_visit",mode="open")

def index():
    # if admin not set, initialize it
    if not k_utils.has_admin(HOST):
        raise HTTP_REDIRECTION,"create_admin"
    # check if user is the administrator
    Login(role=["admin"])

    # menu
    print HEAD(TITLE(_("Administration"))+
        LINK(rel="stylesheet",href="../admin.css"))
    print BODY(A(_("Home"),href="/")+
        H2(_("Administration"))+
        A(_("Configure"),href="../config.ks")+
        BR()+A(_("Translations"),href="../localize/internat.pih")+
        BR()+A(_("Users management"),href="../users.ks")+
        BR()+A(_("Database management"),href="../InstantSite")+
        BR()+TEXT(Logout(_("Logout")))
        )

def create_admin():
    # no access if admin file exists
    if k_utils.has_admin(HOST):
        raise HTTP_REDIRECTION,"index"
    # form
    print H2(_("Enter administrator login and password"))
    print FORM(TABLE(
        TR(TD(_("Login"))+TD(INPUT(name="login")))
        + TR(TD(_("Password"))+TD(INPUT(Type="password",name="passwd")))
        + TR(TD(INPUT(Type="submit",value="Ok")))),
        action="check_admin",method="post")

def check_admin(login,passwd):
    # no access if admin file exists
    if k_utils.has_admin(HOST):
        raise HTTP_REDIRECTION,"index"
    if len(login)<6:
        print _("Error - Login must have at least 6 characters")
        raise SCRIPT_END
    elif len(passwd)<6:
        print _("Error - Password must have at least 6 characters")
        raise SCRIPT_END
    elif login == passwd:
        print _("Error - Login and password must be different")
        raise SCRIPT_END
    # remove previous admin info if any
    db.remove(db(host=HOST,role="admin"))
    # insert admin info
    db.insert(login=login,password=password,role="admin",
        nb_visits=1)
    db.commit()
    raise HTTP_REDIRECTION,"index"
