import os
from urllib import quote_plus,unquote_plus
from HTMLTags import *

import menu

def index(folder=None):

    menu.menu(THIS.basename)
    
    print H2("Select root directory")
    print I("Current root directory is %s" %CONFIG.rootDir)+P()
    if folder is None:
        folder = os.path.dirname(CONFIG.rootDir)
    else:
        folder = unquote_plus(folder)

    drive,rest = os.path.splitdrive(folder)
    folder_parts = rest.split(os.sep)
    print drive
    for i,f in enumerate(folder_parts):
        if not f:
            continue
        parent = drive+os.sep.join(folder_parts[:i+1])+os.sep
        print A(f+os.sep,href="index?folder=%s" %quote_plus(parent))
    print P()

    options = []
    if not os.path.dirname(folder) == folder:
        v = quote_plus(os.path.dirname(folder))
        options.append(TD(A("..",href="index?folder=%s" %v))+
            TD("&nbsp;")*2)
    for f in os.listdir(folder):
        path = os.path.join(folder,f)
        if os.path.isdir(path):   
            v=quote_plus(path)
            line = TD(A("+",href="index?folder=%s" %v))
            line += TD(f)
            line += TD(INPUT(Type="radio",name="root",value=v,
                checked=path==CONFIG.rootDir))
            options.append(line)

    t = TABLE(Sum([TR(option) for option in options]))

    lines = [TR(TD(INPUT(Type="submit",value="Set as root directory")))]
    print FORM(TABLE(TR(TD(t)+TD(TABLE(Sum(lines))))),
        action="set_root",method="post")
    
def set_root(**kw):
    if "root" in kw:
        path = unquote_plus(kw["root"])
        import PyDbLite
        init_db = os.path.splitext(CONFIG.initFile)[0]+".pdl"
        db_name = os.path.join(CONFIG.serverDir,"conf",init_db)
        settings_db = PyDbLite.Base(db_name).open()
        rec = settings_db(setting="rootDir")[0]
        settings_db.update(rec,value=path)
        settings_db.commit()

        # reload k_config
        import KarrigellRequestHandler
        KarrigellRequestHandler.reset_config()

        parent = os.path.dirname(path)
        raise HTTP_REDIRECTION,"index?folder=%s" %quote_plus(parent)        