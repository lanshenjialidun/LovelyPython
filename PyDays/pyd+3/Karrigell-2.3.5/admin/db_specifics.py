import os

# equivalences in types
Integer = ['int','integer']
String = ['str','string','varchar','text']
Date = ['datetime.date']
DateTime = ['datetime.date']
Float = ['float','real']

Types = {}
Types['kirbybase'] = {
    'int' : 'int',
    'integer':'int',
    'str' : 'str',
    'string' : 'str',
    'varchar' : 'str',
    'text':'str',
    'float' : 'float',
    'real':'float',
    'bool' : 'bool',
    'boolean' : 'bool',
    'datetime.datetime' : 'datetime.datetime',
    'datetime.date' : 'datetime.date'
    }

Types['gadfly'] = {
    'int' : 'integer',
    'integer':'integer',
    'str' : 'varchar',
    'string' : 'varchar',
    'varchar' : 'varchar',
    'text':'varchar',
    'float' : 'float',
    'real':'float',
    'bool' : 'varchar',
    'boolean' : 'varchar',
    'datetime.datetime' : 'varchar',
    'datetime.date' : 'varchar'
    }

Types['sqlite'] = {
    'int' : 'integer',
    'integer':'integer',
    'str' : 'text',
    'string' : 'text',
    'varchar' : 'text',
    'text':'text',
    'float' : 'real',
    'real':'real',
    'bool' : 'text',
    'boolean' : 'text',
    'datetime.datetime' : 'text',
    'datetime.date' : 'text'
    } 
    
modulesToImport = {}
createCode = {}
selectAllAsDict = {}
selectByUserId = {}
selectByRecordId = {}
insert = {}
remove = {}
selectUserByLogin = {}

field_list = []
field_names = ""
field_types = ""
field_string = ""
base_name = ""
table = ""
table_base = ""
table_dir = ""
users_base = ""
users_dir = ""

def fieldDefs(dbmod_name,data_directory,name,fields,users_name):
    global field_names, field_types, field_string, field_list
    global table_name, table_base, table_dir, users_base, users_table
    global users_dir, base_name, table
    base_name = name
    abspath = os.path.join(os.path.normpath(data_directory),name)
    users_abspath = os.path.join(os.path.normpath(data_directory),users_name)
    field_list = fields
    field_names = [ f.split(':')[0] for f in fields ]
    field_types = [ f.split(':')[1] for f in fields ]
    field_types = [ Types[dbmod_name][t.lower()] for t in field_types ]    
    table = abspath
    if dbmod_name == 'kirbybase':
        table_name = abspath
        users_base = users_abspath
        table_name = table_name.replace('\\','\\\\')
        users_base = users_base.replace('\\','\\\\')
    elif dbmod_name == 'gadfly':
        table_base = os.path.basename(table)
        table_dir = os.path.dirname(table)
        users_base = os.path.basename(users_abspath)
        users_dir = os.path.dirname(users_abspath)
        field_string = "','".join(['recno']+field_names)
    elif dbmod_name == 'sqlite':
        users_table = users_abspath
        users_base = users_name

# -------------------------------------------
# code to import modules and create utilities
# -------------------------------------------

def modulesToImport(dbmod_name):
    if dbmod_name == 'kirbybase':
        return "import kirbybase\nimport kb_utils\n"
    elif dbmod_name == 'gadfly':
        return "import gadfly\n\n" + makeDict(dbmod_name)
    elif dbmod_name == 'sqlite':
        return \
            "from pysqlite2 import dbapi2 as sqlite\n\n" + makeDict(dbmod_name)

def makeDict(dbmod_name):
    if dbmod_name=='gadfly':
        return \
            "def makeDict(res):\n" \
            "    # convert the result of a cursor.fetchall() to a list\n" \
            "    # of dictionaries\n" \
            "    records = []\n" \
            "    for item in res:\n" \
            "        records.append(dict([(fname,item[i])\n" \
            "            for (i,fname) in enumerate(%(field_names)s)]))\n" \
            "    return records\n" \
                %{'field_names':['recno']+field_names}
    elif dbmod_name == 'sqlite':
        return \
            "def makeDict(res):\n" \
            "    # convert the result of a cursor.fetchall() to a list\n" \
            "    # of dictionaries\n" \
            "    records = []\n" \
            "    for item in res:\n" \
            "        records.append(dict([(fname,item[i])\n" \
            "            for (i,fname) in enumerate(%(field_names)s)]))\n" \
            "        for (fn,ft) in zip(field_names,field_types):\n" \
            "            if ft == 'text':\n" \
            "                records[-1][fn] = records[-1][fn].encode('latin-1')\n" \
            "    return records\n" \
                %{'field_names':['recno']+field_names}
    

# -------------------------
# code to create a database
# -------------------------

def createCode(dbmod_name):
    if dbmod_name == 'kirbybase': 
        return \
        "table = r'%(table)s'\n" \
        "# create an instance of kirbybase\n" \
        "db=kirbybase.KirbyBase()\n\n" \
        "# create the database if it doesn't already exist\n" \
        "if not os.path.exists(table):\n" \
        "    db.create(table,%(fields)s)\n" \
            %{'table':table_name,'fields':str(field_list)}
    elif dbmod_name == 'gadfly':
        sql = ', '.join(['recno integer'] + \
            ['%s %s' %(n,t) for (n,t) in zip(field_names, field_types)])
        sql = 'CREATE TABLE %s (%s)' %(base_name,sql)
        return \
            "try:\n" \
            "    connection = gadfly.gadfly('%(table_base)s',r'%(table_dir)s')\n" \
            "    cursor = connection.cursor()\n" \
            "except IOError:\n" \
            "    connection = gadfly.gadfly()\n" \
            "    connection.startup('%(table_base)s',r'%(table_dir)s')\n" \
            "    cursor = connection.cursor()\n" \
            "    cursor.execute('%(sql)s')\n" \
            %{'sql':sql,'table_base':table_base,'table_dir':table_dir}
    elif dbmod_name == 'sqlite':
        sql = ', '.join(['recno INTEGER PRIMARY KEY'] + \
            ['%s %s' %(n,t) for (n,t) in zip(field_names, field_types)])
        sql = 'CREATE TABLE %s (%s)' %(base_name,sql)
        return \
            "connection = sqlite.connect(r'%(table)s')\n" \
            "cursor = connection.cursor()\n" \
            """cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")\n""" \
            "if not len(cursor.fetchall()):\n" \
            "    cursor.execute('%(sql)s')\n" \
            %{'sql':sql,'table':table}

# -------------------------------
# code to open the users database
# -------------------------------

def openUsersCode(dbmod_name):
    if dbmod_name == 'gadfly':
        return \
        "try:\n" \
        "    users_connection = gadfly.gadfly('%(users_base)s',r'%(users_dir)s')\n" \
        "    users_cursor = users_connection.cursor()\n" \
        "except IOError:\n" \
        "    users_cursor = None\n" \
            %{'users_base':users_base,'users_dir':users_dir}
    elif dbmod_name == 'sqlite':
        return \
        "users_connection = sqlite.connect(r'%(users_table)s')\n" \
        "users_cursor = users_connection.cursor()\n" \
            %{'users_table':users_table}
    else:
        return ""

# -----------------------------------------------------------
# code to return all elements of the database as a dictionary
# -----------------------------------------------------------

def selectAllAsDict(dbmod_name,name):
    if dbmod_name== 'kirbybase':
        return \
        "    # select all the items and return a list of dictionaries, one\n" \
        "    # for each record, indexed by the field names\n" \
        "    records=db.select(table,['recno'],['*'],returnType='dict')\n"
    elif dbmod_name in ['gadfly','sqlite']:
        return \
        "    cursor.execute('SELECT %s FROM %s')\n" \
        "    records = makeDict(cursor.fetchall())\n" \
            %(','.join(['recno']+field_names),name)

# --------------------------------------
# code to select a user from his user id
# --------------------------------------

def selectByUserId(dbmod_name):
    if dbmod_name == 'kirbybase':
        return """        user = db.select(users,['recno'],[user_id],returnType='dict')[0]"""
    elif dbmod_name in ['gadfly','sqlite']:
        return """
        users_cursor.execute('SELECT recno,login,password FROM %(name)s WHERE recno=%%s'
               %%user_id)
        user = dict(zip(['recno','login','password'],users_cursor.fetchall()[0]))\n""" \
            %{'name':users_base}

# -----------------------------------
# code to select a record from its id
# -----------------------------------

def selectByRecordId(dbmod_name):
    if dbmod_name == 'kirbybase':
        return """        record=db.select(table,["recno"],[recordId],returnType='dict')[0]"""
    elif dbmod_name in ['gadfly','sqlite']:
        return """        cursor.execute('SELECT recno,%(field_string)s FROM %(name)s WHERE recno = %%s'
               %%recordId)
        record = makeDict(cursor.fetchall())[0]\n""" \
            %{'field_string':','.join(field_names),'name':base_name}

# ---------------------------------------
# code to insert a record in the database
# ---------------------------------------

def insert(dbmod_name):
    if dbmod_name == 'kirbybase':
        return """    try:
        typed_fields = kb_utils.conv_rec(field_names,field_types,**untyped_fields)
    except ValueError,msg:
        error(msg)
        raise SCRIPT_END
    recordId=int(recordId)
    if recordId==-1:
        db.insert(table,typed_fields)
    else:
        db.update(table,["recno"],[recordId],typed_fields)
    db.pack(table)"""
    elif dbmod_name == 'gadfly':
        return """
    sql="SELECT MAX(recno) FROM %(name)s"
    try:
        cursor.execute(sql)
        res=cursor.fetchall()
        next_id = res[0][0]+1
    except ValueError: # empty base
        next_id = 0

    recordId=int(recordId)
    # replace single quotes by double quotes
    for (k,v) in untyped_fields.items():
        untyped_fields[k]=v.replace("'","''")
    if recordId==-1:
        sql = 'INSERT INTO %(name)s (%(field_string)s) VALUES (%%s)' \\
            %%','.join([str(next_id)]+["'%%s'" %%untyped_fields[n] for n in field_names])
        cursor.execute(sql)
    else:
        vals = ','.join(["%%s = '%%s'" %%(k,v) for (k,v) in untyped_fields.items()])
        sql = 'UPDATE %(name)s SET %%s WHERE recno = %%s' %%(vals,recordId)
        cursor.execute(sql)
    connection.commit()
    """ %{'field_string':'recno,'+','.join(field_names),
            'name':base_name}
    elif dbmod_name == 'sqlite':
        return """
    recordId=int(recordId)
    for (fn,ft) in zip(field_names,field_types):
        if ft == 'text':
            untyped_fields[fn] = unicode(untyped_fields[fn],'latin-1')
    # replace single quotes by double quotes
    for (k,v) in untyped_fields.items():
        untyped_fields[k]=v.replace("'","''")
    if recordId==-1:
        sql = 'INSERT INTO %(name)s (%(field_string)s) VALUES (%%s)' \\
            %%','.join(['NULL']+["'%%s'" %%untyped_fields[f] for f in field_names])
        cursor.execute(sql)
    else:
        vals = ','.join(["%%s = '%%s'" %%(k,v) for (k,v) in untyped_fields.items()])
        sql = 'UPDATE %(name)s SET %%s WHERE recno = %%s' %%(vals,recordId)
        cursor.execute(sql)
    connection.commit()
    """ %{'field_string':'recno,'+','.join(field_names),
            'name':base_name}

# -----------------------
# code to remove a record
# -----------------------

def remove(dbmod_name):
    if dbmod_name == 'kirbybase':
        return """    db.delete(table,["recno"],[int(recordId)])
    db.pack(table)"""
    elif dbmod_name in ['gadfly','sqlite']:
        return """
    sql = 'DELETE FROM %(name)s WHERE recno = %%s' %%recordId
    cursor.execute(sql)
    connection.commit()""" %{'name':base_name}

# ---------------------------------------------
# code to select a user from his login/password
# ---------------------------------------------

def selectUserByLogin(dbmod_name):
    if dbmod_name == 'kirbybase':
        return """    try:
        user_record = db.select(users,['login','password'],
            [user_data['login'],user_data['password']],
            returnType = 'dict')[0]
    except IndexError:
        print "Unknown user"
        print P(A("Back",href="index"))
        return
    except kirbybase.KBError,msg:
        print "An error occured when checking login info"
        print P(msg)
        print P(A("Back",href="index"))
        return"""
    elif dbmod_name in ['gadfly','sqlite']:
        return """
    if users_cursor is not None:
        sql = "SELECT recno,login,password FROM %(name)s"
        sql += " WHERE login = '%%s' AND password = '%%s'" \\
            %%(user_data['login'],user_data['password'])
        users_cursor.execute(sql)
        user_record = users_cursor.fetchall()
        if user_record:
            user_record = dict(zip(['recno','login','password'],user_record[0]))
    else:
        user_record = None\n""" \
        %{'name':users_base}
