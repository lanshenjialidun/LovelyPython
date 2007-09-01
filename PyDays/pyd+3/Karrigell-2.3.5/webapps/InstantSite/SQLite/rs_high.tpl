import os
from HTMLTags import *
import md5

import k_config

%(inits)s
field_names = [ f[0] for f in fields ]

%(open_)s

#header
header=HEAD(LINK(rel="stylesheet",href="../default.css") +
    TITLE(name))

user_test = hasattr(Session(),'%(name)s_user')

def index():
    print '<html>\n'
    print header
    print H1(name)
    if not user_test:
        print '<p><a href="login">Login</p>'
    	raise SCRIPT_END
    # select all the items and return a list of dictionaries, one
    # for each record, indexed by the field names
    %(all_records)s

    if records:
        print '<table class="main" cellpadding="3" cellspacing="0">'
        print '<tr>'
        print Sum([TH(f,Class="main") for f in field_names])
        print TH('&nbsp;',Class="main")*2
        print '</tr>\n'
        counter = 0
        for record in records:
            counter+=1
            if counter %% 2:
                print '<tr class="even">'
            else:
                print '<tr class="odd">'
            for f in field_names:
                print TD(record[f],Class="main")
            print TD(A('Remove',
                href="removeRecord?record_id=%%s" %%record[__id__]),
                Class="main")
            print TD(A('Edit',
                href="editRecord?record_id=%%s" %%record[__id__]),
                Class="main")
            print '</tr>'
        print '</table>'
    else:
        print "Empty base"

	print '<p><a href="editRecord?record_id=-1">New record</a>'
	print '<p><a href="logout">Logout</a>'

    print '</body>\n</html>'

def editRecord(record_id):
    if not user_test:
        raise HTTP_REDIRECTION,"index"
    record_id=int(record_id)
    print header
    print '<body>'
    print SCRIPT(Type='text/JavaScript',src='../scw.js')
    print '<script>scwDateOutputFormat  = "YYYY-MM-DD"'
    print 'scwDateInputSequence = "YMD"'
    print '</script>'

    if record_id>-1:
        %(select_by_id)s
        print H1("Editing a record")
    else:
        print H1("New record")
        record=dict([(f,'') for f in field_names])
    
    print '<form action="insertRecord" method="post">'

    print INPUT(type="hidden",name="record_id",value=record_id)
    print '<table>'
%(ask_fields)s
    print '</table>'
    print INPUT(type="submit",value="Ok")
    print '</form>'
    print '</body>\n</html>'

def insertRecord(record_id,**untyped_fields):
    """Insert a record
    record_id : record identifier
    untyped_fields : field values as strings"""
    if not user_test:
        raise HTTP_REDIRECTION,"index"
    record_id=int(record_id)
    %(insert_or_update)s
    raise HTTP_REDIRECTION,"index"

def removeRecord(record_id):
    """Remove the record with identifier record_id"""
    if not user_test:
        raise HTTP_REDIRECTION,"index"
    %(remove)s
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
    digest=open("%(name)s.ini","rb").read()
    userDigest=digest[:16]
    passwordDigest=digest[16:]

    if (md5.new(user_data['login']).digest()==userDigest \
            and md5.new(user_data['password']).digest()==passwordDigest):
        setattr(Session(),'%%s_user' %%name, user_data['login'])
        raise HTTP_REDIRECTION,'index'
    else:    
        print "Authentication failed"
        print P(A("Back",href="index"))

def logout():
    Session().close()
    raise HTTP_REDIRECTION,'index'
