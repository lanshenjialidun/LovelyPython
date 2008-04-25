import os
from urllib import quote_plus,unquote_plus
from HTMLTags import *

import menu

def index(folder=None):

    menu.menu(THIS.basename)
    
    print H2("Current configuration")
    ks = [ key for key in dir(CONFIG) if not key.startswith("_") and
        isinstance(getattr(CONFIG,key),(bool,str,list,dict)) ]
    ks.sort()

    lines = [TR(TD(k)+TD(getattr(CONFIG,k))) for k in ks]
    print TABLE(Sum(lines))