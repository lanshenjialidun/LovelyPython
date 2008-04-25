header="""HEAD(LINK(rel="stylesheet",href="%(stylesheet)s") +
    TITLE(pageTitle))"""

hdr1="""Karrigell script for managing the database %s
Generated %s
"""

imports ="""
import os
from HTMLTags import *
import md5

"""

hdr2="""
def index():
    user_test = %(default_user_test)s # default
    print '<html>\\n'
    print header
    print H1(pageTitle)
"""
index_if_users1="""
    user_id = None
    so = Session()
    if hasattr(so,'%s_user' %name):
        user_id = getattr(so,'%s_user' %name)
"""
index_if_users2="""
        print user['login']
        print BR(A("Logout",href="logout"))
        user_test = True
    else:
        print A("Login",href="login")
    print P()
"""
index_security_high="""
    print "You are not allowed to see the base"
"""
index_security_not_high="""
    if records:
        print '<table class="main" cellpadding="3" cellspacing="0">'
        print '<tr>'
        print Sum([TH(f,Class="main") for f in field_names])
        if user_test:
            print TH('&nbsp;',Class="main")*2
        print '</tr>\\n'
        counter = 0
        for record in records:
            counter+=1
            if counter % 2:
                print '<tr class="even">'
            else:
                print '<tr class="odd">'
            """
index_security_not_high_2="""
            if user_test:
                print TD(A('Remove',
                    href="removeRecord?recordId=%s" %record['recno']),
                    Class="main")
                print TD(A('Edit',
                    href="editRecord?recordId=%s" %record['recno']),
                    Class="main")
            print '</tr>'
        print '</table>'
    else:
        print "Empty base"
"""
index_end="""
    if user_test:
        print '<p><a href="editRecord?recordId=-1">New record</a>'
    print '</body>\\n</html>'
"""

edit_1="""
def editRecord(recordId):
    recordId=int(recordId)
    if recordId>-1:
%s
        print header
        print H1("Editing a record")
    else:
        print header
        print H1("New record")
        record=dict([(f,'') for f in %s])
    
    print '<form action="insertRecord" method="post">'

    print INPUT(type="hidden",name="recordId",value=recordId)
    print '<table>'
    """
# input records
edit_2="""
    print '</table>'
    print INPUT(type="submit",value="Ok")
    print '</form>'
    print '</body>\\n</html>'
"""

rest="""
def insertRecord(recordId,**untyped_fields):
%s
    raise HTTP_REDIRECTION,"index"

def removeRecord(recordId):
%s
    raise HTTP_REDIRECTION,"index"

def login():
    print H1("Login")
    print '<form action="check_login" method="post">'
    print TABLE(
        TR(TD("Login")+TD(INPUT(name="login"))) +
        TR(TD("Password")+
            TD(INPUT(name="password", Type="password"))) +
        TR(TD(INPUT(Type="submit",value="Ok"))+
            TD("&nbsp;"))
        )
    print '</form>'

def check_login(**user_data):
%s
    if not user_record:
        print "Unknown user"
        print P(A("Back",href="index"))
    else:
        setattr(Session(),'%%s_user' %%name, user_record['recno'])
        raise HTTP_REDIRECTION,'index'

def logout():
    Session().close()
    raise HTTP_REDIRECTION,'index'
    
def error(msg):
    print header
    print H1(pageTitle)
    print msg
    print P(A('Back',href='index'))
"""

admin_method="""
def admin():
    raise HTTP_REDIRECTION, '../%s.ks/index'
"""
admin="""
info = open(r'%(admin_file)s').readlines()
admin_login = info[0].strip()
admin_password = info[1].strip()
def authTest():
    return (AUTH_USER==admin_login
        and md5.new(AUTH_PASSWORD).digest()==admin_password)

Authentication(authTest,
    realm=_("Administration"),
    errorMessage=_("Authentication error"))
"""