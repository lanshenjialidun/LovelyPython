Login(role='admin')

import os
import cPickle
import urllib

from HTMLTags import *
import k_config

comments = {
    "serverDir":"Server folder : the one where Karrigell.py stands",
    "rootDir":"Root folder : a script foo.py in this folder will be served for the url "\
        "http://host/foo.py",
    "cgi_directories":"Folders holding CGI scripts",
    "protectedDirs":"Folders with access restricted to the site administrator",
    "allow_directory_listing":"If a url matches a folder name, " \
        "set who can see the list of files in it",
    "hide_extensions":"List of the file extensions that must not be served when the" \
        " matching URL is called"
}

choices = {
    "allow_directory_listing":["all","none"],
    "reloadModules":[True,False]
}

def index():
    print H2("Configuration")
    for conf in os.listdir("conf"):
        print A(conf,href="show?conf=%s" %conf)

def show(conf):
    info = cPickle.load(open(os.path.join("conf",conf)))
    # folders
    print H3("Folders")
    for k in ["serverDir","rootDir"]:
        print B(comments.get(k,k))," "
        print SMALL(A("[edit]",href="edit/%s/%s" %(conf,k)))
        print info[k] or "(None)"
        print BR()
    for k in ["cgi_directories","protectedDirs"]:
        print B(comments.get(k,k))," "
        print SMALL(A("[edit]",href="edit/%s/%s" %(conf,k)))
        if info[k]:
            for folder in info[k]:
                print BR(folder)
        else:
            print BR("(None)")
        print BR()

    # files and extensions
    print H3("Files and extensions")
    for k in ["hide_extensions"]:
        print B(comments.get(k,k))," "
        print SMALL(A("[edit]",href="edit/%s/%s" %(conf,k)))
        print info[k] or "(None)"
        print BR()

    for k in ["allow_directory_listing"]:
        print B(comments.get(k,k))," "
        print FORM(SELECT(Sum([OPTION(v,value=v) for v in choices[k]])))
        print BR()
    
    for k,v in info.iteritems():
        print B(comments.get(k,k))," ",v,A("edit",href="edit/%s/%s" %(conf,k)),BR()
    
def test(**kw):
    print THIS.subpath
    print BR("kw"),kw

def edit():
    conf,key=THIS.subpath
    info = cPickle.load(open(os.path.join("conf",conf)))
    v = info[key]
    if key in ["cgi_directories","protectedDirs"]:
        print FRAMESET(
            FRAME(src=THIS.rel("selected_folders/%s/%s"%(conf,key)))+
            FRAME(src=THIS.rel("folder_browser/%s/%s/%s" 
                %(conf,key,urllib.quote_plus(info["serverDir"])))),
            cols="50%,*"
            )
    elif key in ["rootDir","serverDir"]:
        print FRAMESET(
            FRAME(src=THIS.rel("selected_folder/%s/%s"%(conf,key)))+
            FRAME(src=THIS.rel("folder_browser/%s/%s/%s" 
                %(conf,key,urllib.quote_plus(info[key])))),
            cols="50%,*"
            )
    else:
        print key,v

def modif(conf,key,subm,folder):
    info = cPickle.load(open(os.path.join("conf",conf)))
    v = info[key]
    folder = urllib.unquote_plus(folder)
    if subm == "Remove":
        v.remove(folder)
        info[key] = v
        out = open(os.path.join("conf",conf),"wb")
        cPickle.dump(info,out)
        out.close()
        raise HTTP_REDIRECTION,"selected_folders/%s/%s" %(conf,key)

def selected_folders():
    conf,key = THIS.subpath
    info = cPickle.load(open(os.path.join("conf",conf)))
    v = info[key]
    print H2(comments.get(key,key))
    data = INPUT(Type="hidden",name="conf",value=conf)
    data += INPUT(Type="hidden",name="key",value=key)
    s = SELECT(Sum([OPTION(folder,value=urllib.quote_plus(folder))
        for folder in v]),name="folder",size=10)
    remove_button = INPUT(Type="submit",name="subm",value="Remove")
    print FORM(data+s+remove_button,action=THIS.rel("modif"),
        method="post")
    print FORM(INPUT(Type="hidden",value=conf,name="conf")+
        INPUT(Type="submit",value="Exit"),
        action=THIS.rel("show"),target="_top")

def selected_folder():
    conf,key = THIS.subpath
    info = cPickle.load(open(os.path.join("conf",conf)))
    folder = info[key]
    print H2(comments.get(key,key))
    data = INPUT(Type="hidden",name="conf",value=conf)
    data += INPUT(Type="hidden",name="key",value=key)
    s = INPUT(name="folder",value=folder,size=40)
    print FORM(data+s,action=THIS.rel("modif"),
        method="post")
    print FORM(INPUT(Type="hidden",value=conf,name="conf")+
        INPUT(Type="submit",value="Exit"),
        action=THIS.rel("show"),target="_top")

def folder_browser():
    conf,key,folder = THIS.subpath
    folder = urllib.unquote_plus(folder)
    print H2(folder)
    if os.path.dirname(folder) != folder:
        print BR(A("..",href="%s"
            %urllib.quote_plus(os.path.dirname(folder))))
    for f in [ d for d in os.listdir(folder)
        if os.path.isdir(os.path.join(folder,d)) ]:
        dest = urllib.quote_plus(os.path.join(folder,f))
        print BR(A("+",href="%s" %dest)+
            TEXT(" ")+
            A(f,href=THIS.rel("update/%s/%s/%s" %(conf,key,dest)),
                target="_top"))

def update():
    conf,key,folder = THIS.subpath
    folder = urllib.unquote_plus(folder)
    info = cPickle.load(open(os.path.join("conf",conf)))
    v = info[key]
    if isinstance(v,list):
        if not folder in v:
           info[key].append(folder)
    else:
        info[key] = folder
    out = open(os.path.join("conf",conf),"wb")
    cPickle.dump(info,out)
    out.close()
    raise HTTP_REDIRECTION,THIS.rel("edit/%s/%s" %(conf,key))
    