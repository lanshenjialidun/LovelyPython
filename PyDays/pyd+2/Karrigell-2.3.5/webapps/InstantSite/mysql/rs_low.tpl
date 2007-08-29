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

def index():
    print '<html>\n'
    print header
    print H1(name)
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

    print '</body>\n</html>'

def editRecord(record_id):
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

    record_id=int(record_id)
    %(insert_or_update)s
    raise HTTP_REDIRECTION,"index"

def removeRecord(record_id):
    %(remove)s
    raise HTTP_REDIRECTION,"index"
