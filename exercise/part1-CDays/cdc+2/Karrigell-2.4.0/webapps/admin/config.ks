Login(role='admin')

from HTMLTags import *
import menu

def index():
    print HEAD(TITLE("Select root directory")+
        LINK(rel="stylesheet",href="../admin.css"))
    body = A("Admin",href="../index.ks")
    body += H2("Editing configuration file")
    body += TEXT("Current config file is %s" %CONFIG.initFile)
    content = open(CONFIG.initFile).read()
    body += FORM(TEXTAREA(content,name="content",rows=25,cols=80)+BR()+
        INPUT(Type="submit",name="subm",value="Save changes")+
        INPUT(Type="submit",name="subm",value="Cancel"),
        action="save_changes",method="post")
    print BODY(body)
    
def save_changes(content,subm):
    if subm=="Cancel":
        raise HTTP_REDIRECTION,"../index.ks"
    out = open(CONFIG.initFile,"wb")
    out.write(content)
    out.close()
    print "Changes in configuration file %s saved" %CONFIG.initFile
    print BR("Apply them immediately ? ")
    print A("Yes",href="apply")
    print "&nbsp;"
    print B(A("No",href="/admin"))

def apply():
    import KarrigellRequestHandler
    KarrigellRequestHandler.reset_config()
    print "New configuration applied"
    print BR()+A("Admin",href="/admin")