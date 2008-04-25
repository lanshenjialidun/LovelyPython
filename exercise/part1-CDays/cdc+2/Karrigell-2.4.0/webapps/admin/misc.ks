import os

from HTMLTags import *

import menu

info = {"debug":'check if you want the "Debug" button to appear when '
        'an exception is caught by Karrigell. You might want to uncheck it to '
        'for security reasons',
        "reload":"check to reload all imports at every request ; better leave "
        "it checked, except if unchecking results in better performance, "
        "or if you import modules that must maintain a state",
        "encode":"check if form fields should be encoded",
        "output":"Unicode encoding used by the browser to print bytestrings",
        "allow":
        "If a url matches a directory with no index file in it, determine if "
        "a directory listing should be printed"}


def index():
    menu.menu(selected=THIS.basename)

    lines = [TR(TH("Setting")+TH("Value"))]
    
    lines.append(TR(TD("debug")+TD(INPUT(Type="checkbox",name="debug",
        checked = CONFIG.debug))+
        TD(info.get("debug","&nbsp;"))))
    lines.append(TR(TD("reload modules")+TD(INPUT(Type="checkbox",
        name="reload_modules",checked = CONFIG.reload_modules))+
        TD(info.get("reload","&nbsp;"))))
    lines.append(TR(TD("encode form data")+TD(INPUT(Type="checkbox",
        name="encode_form_data",checked = CONFIG.encode_form_data))+
        TD(info.get("encode","&nbsp;"))))
    lines.append(TR(TD("allow directory listing")+TD(INPUT(Type="checkbox",
        name="allow_directory_listing",
        checked = CONFIG.allow_directory_listing))+
        TD(info.get("allow","&nbsp;"))))
    lines.append(TR(TD("output encoding")+TD(INPUT(name="output_encoding",
        value = CONFIG.output_encoding))+
        TD(info.get("output","&nbsp;"))))

    lines.append(TR(TD(INPUT(Type="submit",value="Ok"),colspan=2)))
    
    print FORM(TABLE(Sum(lines)),action="update",method="post")

def update(**kw):

    import PyDbLite
    db_name = os.path.splitext(CONFIG.initFile)[0]+".pdl"
    settings_db = PyDbLite.Base(os.path.join(CONFIG.rootDir,"conf",db_name)).open()

    output_encoding = kw.get("output_encoding","")
    if output_encoding:
        try:
            unicode('a',output_encoding)
            rec = settings_db(setting="output_encoding")[0]
            settings_db.update(rec,value=output_encoding)
        except LookupError:
            print "Unknown output encoding : %s" %kw["output_encoding"]
            raise SCRIPT_END

    for key in ["debug","reload_modules","encode_form_data",
        "allow_directory_listing"]:

        rec = settings_db(setting=key)[0]
        settings_db.update(rec,value = key in kw)

    settings_db.commit()
    
    # reload k_config
    import KarrigellRequestHandler
    KarrigellRequestHandler.reset_config()
    
    raise HTTP_REDIRECTION,"index"
