import os
import urllib

import PyDbLite
from HTMLTags import *

import menu

db_name = os.path.splitext(CONFIG.initFile)[0]+".pdl"
settings_db = PyDbLite.Base(os.path.join(CONFIG.rootDir,"conf",db_name)).open()
levels = ["all","visit","edit","admin"]

def _options(sel_level):
    return Sum([OPTION(level,value=level,selected=level==sel_level) 
        for level in levels])

def index(folder=None):
    menu.menu(selected=THIS.basename)

    if folder is None:
        folder = CONFIG.rootDir
    else:
        folder = urllib.unquote_plus(folder)
    drive,rest = os.path.splitdrive(folder)
    folder_parts = rest.split(os.sep)

    for i,f in enumerate(folder_parts):
        if not f:
            continue
        parent = drive+os.sep.join(folder_parts[:i+1])+os.sep
        print A(f+os.sep,href="index?folder=%s" %urllib.quote_plus(parent))
    print P()
    t = [TR(TH("&nbsp;")+TH("Folder")+TH("Access")+TH("CGI")+
        TH("Alias")+TH("&nbsp;"))]
    if not os.path.dirname(folder)==folder:
        t.append(TR(TD("&nbsp;")+
                TD(A("..",href="index?folder=%s" 
                    %urllib.quote_plus(os.path.dirname(folder))))+
                    TD("&nbsp")*4))
    for f in os.listdir(folder):
        path = os.path.join(folder,f)
        if os.path.isdir(path):
            alias = ""
            if path in CONFIG.alias.values():
                alias = [ k for k in CONFIG.alias if CONFIG.alias[k]==path][0]
            level = CONFIG.protectedDirs.get(path,"all")
            is_cgi = path in CONFIG.cgi_directories

            qpath = urllib.quote_plus(path)
            line = TD(A("+",href="index?folder=%s" %qpath))
            line += TD(f)
            line += TD(SELECT(_options(level),name="level"))
            line += TD(INPUT(Type="checkbox",name="cgi",checked=is_cgi))
            line += TD(INPUT(name="alias",value=alias or ""))
            line += TD(INPUT(Type="submit",value="Update"))
            t.append(FORM(TR(line)+INPUT(Type="hidden",name="path",value=qpath),
                action="update",method="post"))
    print TABLE(Sum(t),border=1)

def update(**kw):
    path = urllib.unquote_plus(kw["path"])
    alias = settings_db(setting="alias")[0]
    al_dict = alias["value"]

    if "level" in kw:
        if path == al_dict["admin"]:
            print "Can't change security level for path admin"
            raise SCRIPT_END
        protected = settings_db(setting="protectedDirs")[0]
        protected["value"][path] = kw["level"]
        settings_db.update(protected,value=protected["value"])

    if "alias" in kw:

        # forbid changing admin alias
        if path == al_dict["admin"] and kw["alias"] != "admin":
            print "Can't change alias for the admin folder"
            raise SCRIPT_END

        # forbid duplicate aliases
        if kw["alias"] in al_dict \
            and not al_dict[kw["alias"]]==path:
            print "Alias %s already exists for folder %s" %(kw["alias"],
                    al_dict[kw["alias"]])
            raise SCRIPT_END
        al_dict.update({kw["alias"]:path})
        settings_db.update(alias,value=al_dict)

    settings_db.commit()
    
    # reload k_config
    import KarrigellRequestHandler
    KarrigellRequestHandler.reset_config()
    
    parent = os.path.dirname(path)
    raise HTTP_REDIRECTION,"index?folder=%s" %urllib.quote_plus(parent)