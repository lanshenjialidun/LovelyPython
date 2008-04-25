import os
import k_utils
from HTMLTags import *
import k_config
import PyDbLite

def index():

    if k_utils.has_admin(HOST):
        print "Administrator login / password already set"
        raise SCRIPT_END

    print H3(_("Create a login/password for administrator"))
    print FORM(TABLE(
        TR(TD(_("Login"))+TD(INPUT(name="login")))+
        TR(TD(_("Password"))+TD(INPUT(name="passwd1",Type="password")))+
        TR(TD(_("Confirm password"))+TD(INPUT(name="passwd2",Type="password")))+
        TR(TD(INPUT(Type="submit",value="Ok"),colspan=2))
        ),action="set_admin_info",method="post")

def _error(msg):
    print msg
    print BR(A(_("Back"),href="javascript:history.back()"))

def set_admin_info(login,passwd1,passwd2):

    if k_utils.has_admin(HOST):
        print _("Administrator login / password already set")
        raise SCRIPT_END
    
    if passwd1 != passwd2:
        _error(_("Password mismatch"))
    elif len(login)<6:
        _error(_("Login must have at least 6 characters"))
    elif len(passwd1)<6:
        _error(_("Password must have at least 6 characters"))
    else:
        # create users database
        db_path = os.path.join(k_config.serverDir,"data","users.pdl")
        db = PyDbLite.Base(db_path)
        db.create("host","login","password","role","session_key","nb_visits",
            "last_visit",mode="open")

        # remove existing admin if any
        db.delete(db(host=HOST,role="admin"))
        # insert new admin
        db.insert(host=HOST,login=login,password=passwd1,role="admin",nb_visits=0)
        db.commit()
        print _("Administrator info set")
        print BR(A("Home",href="/"))
