import psycopg2 as pgdb

conn = pgdb.connect(host='localhost',databse='qingfeng',user='qingfeng',password='123')

cur = conn.cursor()

cur.execute("select * from dream")

print cur.rowcount
