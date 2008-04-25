import os
from HTMLTags import *
import PyDbLite
import k_utils

db_path = os.path.join(CONFIG.serverDir,"data","users.pdl")

def login(baseurl,path,role="admin"):
    # check if users database initialized
    if not k_utils.has_admin(HOST):
        print "Users database doesn't exist for this host. You must "
        print A("set admin login and password",href="../set_admin.ks")
        raise SCRIPT_END
    # check if user session valid
    print HEAD(TITLE("Authentication"))
    print H2("Authentication")
    f = INPUT(Type="hidden",name="baseurl",value=baseurl)
    f += INPUT(Type="hidden",name="path",value=path)
    f += INPUT(Type="hidden",name="role",value=role)
    lines = TR(TD("Login")+TD(INPUT(name="login")))
    lines += TR(TD("Password")+TD(INPUT(name="passwd",Type="password")))
    lines += TR(TD(INPUT(Type="submit",value="Ok"),colspan="2"))
    print BODY(FORM(f+TABLE(lines),action="check_login",method="post"))

def check_login(baseurl,path,login,passwd,role="admin"):

    db = PyDbLite.Base(db_path).open()
    admin = db(host=HOST,login=login,password=passwd)
    if admin and admin[0]["role"] in role.split(","):
        # make session key
        import k_utils
        key = k_utils.generateRandom(16)
        r = admin[0]
        db.update(r,session_key=key)
        db.commit()
        SET_COOKIE["role"] = r["role"]
        SET_COOKIE["role"]["path"] = '/'+ baseurl.rstrip('/')
        SET_COOKIE["login"] = r["login"]
        SET_COOKIE["login"]["path"] = '/'+ baseurl.rstrip('/')
        SET_COOKIE["skey"] = key
        SET_COOKIE["skey"]["path"] = '/'+ baseurl.rstrip('/')
        raise HTTP_REDIRECTION,path
    else:
        print "Authentication failed"

def logout(baseurl,path):
    for cookie_name in "role","login","skey":
        SET_COOKIE[cookie_name] = ""
        SET_COOKIE[cookie_name]["path"] = '/'+baseurl.rstrip('/')
        SET_COOKIE[cookie_name]["expires"] = 0
    raise HTTP_REDIRECTION,path

def change_pw():
    db = PyDbLite.Base(db_path).open()
    if not "role" in COOKIE.keys():
        raise HTTP_REDIRECTION,"../"
    print header(_("Change password"))
    print H3(_("Change password"))
    user = db(host=HOST,login=COOKIE["login"].value)
    if not user:
        print _("Unknown user"),COOKIE["login"].value
        raise SCRIPT_END
    user = user[0]
    print B(_("User")),user["login"]
    f = TR(TD(_("Old password"))+TD(INPUT(Type="password",name="old_pw")))
    f += TR(TD(_("New password"))+TD(INPUT(Type="password",name="new_pw1")))
    f += TR(TD(_("Confirm"))+TD(INPUT(Type="password",name="new_pw2")))
    f += TR(TD(INPUT(Type="submit",value="Ok"),colspan="2"))
    print FORM(TABLE(f),action="check_new_pw",method="post")
    print FORM(INPUT(Type="submit",value=_("Cancel")),action="../")

def check_new_pw(old_pw,new_pw1,new_pw2):
    db = PyDbLite.Base(db_path).open()
    if not "role" in COOKIE.keys():
        raise HTTP_REDIRECTION,"../"
    user = db(host=HOST,login=COOKIE["login"].value)
    if not user:
        print _("Unknown user"),COOKIE["login"].value
        raise SCRIPT_END
    user = user[0]
    if not user["passwd"] == old_pw:
        print _("Wrong password")
        print A(_("Back"),href="change_pw")
        raise SCRIPT_END
    if not new_pw1 == new_pw2:
        print _("You didn't enter twice the same password")
        print A(_("Back"),href="change_pw")
        raise SCRIPT_END
    db.update(user,passwd=new_pw1)
    db.commit()
    raise HTTP_REDIRECTION,"../index2.html"
        