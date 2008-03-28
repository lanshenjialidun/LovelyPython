from MySQLdb.constants import FIELD_TYPE
types = [ f for f in dir(FIELD_TYPE) if not f.startswith('__') ]

inits = """import MySQLdb

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
connection = MySQLdb.connect(host=host,user=user,passwd=passwd,db=base_name)
cursor = connection.cursor()"""

all_records = """cursor.execute('SELECT %s FROM %s' %(','.join([__id__]+field_names),name))
    records = makeDict(cursor.fetchall())"""

select_by_id = """field_string = ','.join(field_names)
        sql = 'SELECT %s,%s FROM %s WHERE %s = %s' \\
            %(__id__,field_string,name,__id__,record_id)
        cursor.execute(sql)
        record = makeDict(cursor.fetchall())[0]
        connection.close()"""

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
    cursor.execute(sql)
    connection.commit()
    connection.close()""" 

remove = """
    sql = 'DELETE FROM %s WHERE %s = %s' %(name,__id__,record_id)
    cursor.execute(sql)
    connection.commit()
    connection.close()
"""
