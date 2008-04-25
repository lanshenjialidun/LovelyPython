import os
from datetime import date, datetime
from HTMLTags import *
import ask

import MySQLdb

Types = ['TINYINT','BIT','BOOL',
  'SMALLINT',
  'MEDIUMINT',
  'INT',
  'INTEGER',
  'BIGINT',
  'REAL',
  'DOUBLE',
  'FLOAT',
  'DECIMAL','DEC','FIXED',
  'NUMERIC',
  'DATE',
  'TIME',
  'TIMESTAMP',
  'DATETIME',
  'YEAR',
  'CHAR',
  'VARCHAR',
  'TINYBLOB',
  'BLOB',
  'MEDIUMBLOB',
  'LONGBLOB',
  'TINYTEXT',
  'TEXT',
  'MEDIUMTEXT',
  'LONGTEXT',
  'ENUM',
  'SET']
Types.sort()

class ConfigError(Exception):
    pass

def makeDict(res):
    # convert the result of a cursor.fetchall() to a list
    # of dictionaries
    records = []
    for item in res:
        records.append(dict([(fname,item[i])
            for (i,fname) in enumerate(['recno']+field_names)]))
    return records

# restrict access to administrator
RestrictToAdmin()

#header
script = SCRIPT(src="../mysql.js")+SCRIPT(src="../genScript.js")

header=HEAD(LINK(rel="stylesheet",href="../manage.css") +
    TITLE('MySQL management')+script)

print '<html>'
print header

def index():
    if hasattr(Session(),"connection"):
        Session().connection.close()
    print '<body>'
    print H1('Connection to MySQL server')
    ask.ask('Database info','open_connection',
        ('Host','host'),('User','user'),
        ('Password','passwd','password'))

def open_connection(host,user,passwd):
    connection = MySQLdb.connect(host=host,user=user,
        passwd=passwd)
    Session().connection = connection
    Session().cursor = connection.cursor()
    Session().conn_info = host,user,passwd
    Session().folded = {}
    if hasattr(Session(),'db'):
        del Session().db
    raise HTTP_REDIRECTION,"view"

def _show_databases():
    Session().cursor.execute("SHOW DATABASES")
    print '<ul>'
    for _db in Session().cursor.fetchall():
        db = _db[0]
        if db in ['information_schema','mysql']:
            continue
        lnk = A(db,href="view?db=%s&action=show_db" %db)
        if Session().folded.get(db,True):
            print LI(A(SPAN('+',Class="fold"),
                href="view?db=%s&action=unfold" %db)+
                TEXT('&nbsp;')+lnk)
        else:
            print LI(A(SPAN('-',Class="fold"),
                href="view?db=%s&action=fold" %db)+
                TEXT('&nbsp;')+lnk)
            print '<ul>'
            _show_tables(db)
            print '</ul>'
    print LI(A('[New]',href="view?action=create_db"))
    print '</ul>'

def create_new_db(new_db):
    Session().cursor.execute('CREATE DATABASE IF NOT EXISTS %s' %new_db)
    Session().cursor.execute('USE %s' %new_db)
    Session().db = new_db
    raise HTTP_REDIRECTION,'view'

def _create_new_table():
    print H3('New table in database %s' %Session().db)
    print '<form action="view">'
    print '<input type="hidden" name="new_table" value="1">'
    print '<input name="table">'
    print '<input type="submit" value="Ok">'
    print '</form>'

def _show_tables(db):
    Session().cursor.execute('USE %s' %db)
    Session().cursor.execute('SHOW TABLES')
    for table_info in Session().cursor.fetchall():
        tname = table_info[0]
        print LI(A(tname,href="view?db=%s&table=%s"
            %(db,tname)))
    print LI(A("[New]",href="view?action=new_table"))

def view(db=None,table=None,action="",new_db=0,new_table=0):
    print '<body onLoad="change_type()" onKeyUp="validate()">'
    print H2('MySQL management')
    if db is None and hasattr(Session(),"db"):
        db = Session().db
    else:
        Session().db = db
    if action=="create_db":
        db = 0
    if action=="unfold":
        Session().folded[db] = False
    elif action=="fold":
        Session().folded[db] = True
    print '<table cellpadding="10">'
    print '<tr><td valign="top" id="tblist">'
    _show_databases()
    print '</td>'
    if db:
        Session().cursor.execute('USE %s' %db)
    print '<td valign="top">'
    if action=="create_db":
        ask.ask('Create new database','create_new_db',
            ('Name','new_db'))
    elif action=="new_table":
        _create_new_table()
    elif action=="show_db":
        print "Database %s" %db
        print FORM(INPUT(Type="hidden",name="action",value="drop_db")+
            INPUT(Type="submit",value="Drop database"),
            action="view")
    elif action=="drop_db":
        _drop_db()
    elif action=="drop_table":
        _drop_table()
    else:
        view_table(table,new_table)
    print '</td></tr></table>'
    print A("Close session",href="index")
    print '</body></html>'
    
def view_db(db,new=0):
    Session().db = db

def view_table(table,new=0):
    if table is None:
        return
    print '<h4>'
    print 'Database %s' %Session().db
    print '&nbsp;Table %s</h4>' %table
    
    new = int(new)
    Session().table = table
    columns = []
    if new == 0:
        print TABLE(TR(
            TD(FORM(INPUT(Type="submit",value="Drop table")+
                INPUT(Type="hidden",name="action",value="drop_table"),
               action="view"))  +
            TD(FORM(INPUT(Type="submit",value="Generate management script"),
               action="generate_script"))
              ))
               
        Session().cursor.execute('DESCRIBE %s' %table)
        print '<form action="remove_fields" name="fields" method="post" target="_top">'
        print '<table border="1" width="100%">'
        print TR(TH('&nbsp')+TH('Field')+TH('Type')+TH('Null')+TH('Key')+
            TH('Default')+TH('Extra'))
        columns = []
        for field_info in Session().cursor.fetchall():
            s = INPUT(Type="checkbox",name="field[]",value=field_info[0],onClick="sel_field()")
            columns.append(field_info[:2])
            print TR(TD(s)+Sum([ TD(item or '&nbsp;') for item in field_info ]))
        print '</table>'
        print INPUT(Type="submit",value="Remove selected",id="sub",disabled=True)
        print '</form>'
        Session().columns = columns

    print '<form action = "insert_field" name="add" method="post" target="_top">'
    print INPUT(name="table",id="table",Type="hidden",value=table)
    print INPUT(name="new",id="new",Type="hidden",value=new)
    print H4('Insert new field')
    print '<p><div id="field_def">'
    print '<table>'
    print '<tr><td>'
    print '<table border="1">'
    print TR(TD(B('Field name'))+TD(INPUT(name="field")))
    if not new:
        pos = OPTION('FIRST',value="FIRST")
        for i,item in enumerate(columns):
            pos += OPTION('AFTER %s' %item[0],value='AFTER %s' %item[0],
                 selected = i==(len(columns)-1)) 
        print TR(TD('Position')
            +TD(SELECT(pos,name="position",onChange="validate()")))
    print '<tr>'
    print TD('Type')
    print TD(SELECT(Sum([ OPTION(t,value=t,selected=t=='TEXT') for t in Types ]),
            name="Type",id="Type",onChange="change_type()"))
    print '</tr>'
    print TR(TD('NULL')+TD(TEXT('NULL')+
             INPUT(name="null",Type="radio",
                   checked=True,onClick="ch_null(0)") +
             TEXT('NOT NULL')+
             INPUT(name="null",Type="radio",onClick="ch_null(1)")))
    print TR(TD('DEFAULT')+TD(INPUT(id="default",name="default",disabled=True)))
    print TR(TD('KEY')+TD(TEXT('no')+
             INPUT(name="key",Type="radio",
                   checked=True,onClick="ch_key(0)") +
             TEXT('KEY')+
             INPUT(name="key",Type="radio",onClick="ch_key(1)")+
             TEXT('PRIMARY KEY')+
             INPUT(name="key",Type="radio",onClick="ch_key(2)")
             ))
    print '</table>'
    print '</td>'
    print TD(DIV(id="f_opt",style="position:absolute"),valign="top")
    print '</tr></table>'
    print "<p>SQL statement"
    print BR()+TEXTAREA(name="sql",cols="40",rows="4")
    print INPUT(id="subm",Type="submit", value="Ok")
    print '</div>' # end of field_def
    print '</form>'
    print '</body></html>'

def remove_fields(field):
    for f in field:
        Session().cursor.execute('ALTER TABLE %s DROP %s' 
            %(Session().table,f))
    raise HTTP_REDIRECTION,"view?db=%s&table=%s" %(Session().db,
        Session().table)

def insert_field(**kw):
    sql = kw["sql"]
    Session().cursor.execute(sql)
    Session().connection.commit()
    raise HTTP_REDIRECTION,"view?db=%s&table=%s" %(Session().db,
        Session().table)

def _drop_db():
    db = Session().db
    Session().cursor.execute('USE %s' %db)
    Session().cursor.execute('SHOW TABLES')
    if len(Session().cursor.fetchall()):
        print "Can't drop database %s ; all tables must be dropped first" %db
        raise SCRIPT_END
    print "Are you sure you want to delete database %s ?" %db
    print P()+FORM(INPUT(Type="hidden",name="db",value=db)+
        INPUT(Type="submit",value="Drop database"),
        action="drop_db_confirm")
    print INPUT(Type="button",value="Cancel",onClick="javascript:back()")
    print "</body>"

def drop_db_confirm(db):
    Session().cursor.execute('DROP DATABASE %s' %db)
    del Session().db
    raise HTTP_REDIRECTION,'view'

def _drop_table():
    print "Are you sure you want to delete table %s" %Session().table
    print "? This will erase all data"
    print P()+FORM(INPUT(Type="submit",value="Drop table"),
        action="drop_table_confirm",target="_top")
    print INPUT(Type="button",value="Cancel",onClick="javascript:back()")

def drop_table_confirm():
    Session().cursor.execute('DROP TABLE %s' %Session().table)
    del Session().table
    raise HTTP_REDIRECTION,"view?db=%s" %Session().db

def generate_script():
    print H2("Generating script for table %s" %Session().table)
    print '<form action="generate_script_2" method="post">'
    sec = INPUT('low (anyone can see/edit records)',Type="radio",value="low",name="security",
            onClick="change_sec(this)")+BR()+\
        INPUT('standard (anyone can see records, edition restricted to administrator)',
            Type="radio",value="standard",name="security",
            onClick="change_sec(this)",checked=True)+BR()+\
        INPUT('high (only the admin can see and edit records)',
            Type="radio",value="high",name="security",onClick="change_sec(this)")
    e_security = TR(TD(B("Security level")+BR())+TD(sec))
    print e_security
    adm_info = TABLE(TR(TD('Login')+TD(INPUT(name="login")))+
        TR(TD('Password')+TD(INPUT(Type="password",name="passwd"))))
    print SPAN(adm_info,id="adm_info")
    print INPUT(Type="submit",value="Ok")
    print '</form>'

def generate_script_2(security,login=None,passwd=None):
    """Generate the management script"""
    table = Session().table
    name = table
    # initialize the variables
    Session().cursor.execute('DESCRIBE '+table)
    __id__ = None
    info = []
    for field in Session().cursor.fetchall():
        Field,Type,Null,Key,Default,Extra = field
        if Key == 'PRI' and Extra == 'auto_increment':
            __id__ = Field
        else:
            info.append((Field,Type,Null,Key,Default,Extra))
    if __id__ is None:
        print "Error - base %s has no integer primary key with auto_increment"\
            %table
        raise SCRIPT_END

    if security != 'low':
        admin_file = os.path.join('applications',table + '.ini')
        if not login or not passwd:
            if not os.path.exists(admin_file):
                raise ConfigError,'Administrator login or password missing'
        else:
            _save_admin_info(admin_file,login,passwd)

    from db_mysql import inits,open_,all_records,\
        select_by_id,insert_or_update,remove

    template = open('rs_%s.tpl' %security).read()

    # open the generated ks script
    out = open(os.path.join('applications','%s.ks' %table),'w')
    out.write('"""Database management\nGenerated %s"""\n\n'
        %(datetime.now().strftime('%x %X')))

    for k,v in zip(['host','user','passwd'],Session().conn_info):
        out.write('%s = "%s"\n' %(k,v))
    out.write('base_name = "%s"\n' %Session().db)
    out.write('name = "%s"\n' %table)
    out.write('fields = (')
    out.write(','.join(['("%s","%s","input")' %f for f in Session().columns]))
    out.write(')\n')
    out.write('__id__ = "%s"\n' %__id__)

    ask_fields = ""
    for field in Session().columns:
        fn = field[0]
        if fn == __id__:
            continue
        input_format = 'input' #field[2]
        if field[1].lower() == 'date':
            input_format = 'calendar'
        if input_format == 'textarea':
            ask_fields += '    print TR(TD("%s")+' %fn
            ask_fields += 'TD(TEXTAREA(record["%s"],name="%s",rows="10",cols="50")))\n' %(fn,fn)
        elif input_format == 'calendar':
            ask_fields += '    print TR(TD("%s")+' %fn
            ask_fields += 'TD(INPUT(name="%s",id="%s",size="20",value=record["%s"])+\n' %(fn,fn,fn)
            ask_fields += '        A(IMG(src="../Calandar.gif",border=0),\n'
            ask_fields += '        href= "javascript:scwShow(document.'
            ask_fields += 'getElementById(\'%s\'), this);" )))\n' %fn
        else:
            ask_fields += '    print TR(TD("%s")+' %fn
            ask_fields += 'TD(INPUT(name="%s",size="40",value=record["%s"])))\n' %(fn,fn)

    out.write(template %locals())
    out.close()

    print "Script <b>%s.ks</b> generated<br>" %table
    print '<a href="../applications/%s.ks" target="_new">Test it</a>' \
        %table
    print '<br><a href="view?table=%s">Back to configuration</a>' %table

def _save_admin_info(admin_file,login,password):
    # save md5 digest of the login and password
    import md5
    out = open(admin_file,'wb')
    out.write(md5.new(login).digest())
    out.write(md5.new(password).digest())
    out.close()
