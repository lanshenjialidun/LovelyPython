inits = """import sys
import traceback

try:
    from sqlite3 import dbapi2 as sqlite
except ImportError:
    from pysqlite2 import dbapi2 as sqlite
except ImportError:
    print "SQLite is not installed"
    raise SCRIPT_END

def makeDict(res):
    # convert the result of a cursor.fetchall() to a list
    # of dictionaries
    records = []
    for item in res:
        records.append(dict([(fname,item[i])
            for (i,fname) in enumerate([__id__]+field_names)]))
    return records
"""

open_ = """# open connection
connection = sqlite.connect(base_name)
cursor = connection.cursor()"""

all_records = """cursor.execute('SELECT %s FROM %s' %(','.join(["_ROWID_"]+field_names),name))
    records = makeDict(cursor.fetchall())"""

select_by_id = """field_string = ','.join(field_names)
        sql = 'SELECT _ROWID_,%s FROM %s WHERE %s = %s' \\
            %(field_string,name,__id__,record_id)
        cursor.execute(sql)
        record = makeDict(cursor.fetchall())[0]"""

insert_or_update = """
    # field names except the record identifier (auto increment)
    f_names = [ f for f in field_names if not f == __id__ ]
    field_string = ','.join(f_names)
    # replace single quotes by double quotes
    for (k,v) in untyped_fields.items():
        untyped_fields[k]=v.replace("'","''")
    if record_id == -1:
        vals = ','.join(["'%s'" %untyped_fields[f] for f in f_names])
        sql = 'INSERT INTO %s (%s) VALUES (%s)' \\
            %(name,field_string,vals)
    else:
        vals = ','.join(["%s = '%s'" %(k,v) for (k,v) in untyped_fields.iteritems()])
        sql = 'UPDATE %s SET %s WHERE %s = %s' %(name,vals,__id__,record_id)
    sql = unicode(sql,k_config.outputEncoding)
    try:
        cursor.execute(sql)
        connection.commit()
        raise HTTP_REDIRECTION,"index"
    except sqlite.OperationalError:
        print 'Operational error - try again'
        traceback.print_exc(file=sys.stdout)
        cursor.close()
        connection.close()""" 

remove = """
    sql = 'DELETE FROM %s WHERE %s = %s' %(name,__id__,record_id)
    cursor.execute(sql)
    connection.commit()
"""
