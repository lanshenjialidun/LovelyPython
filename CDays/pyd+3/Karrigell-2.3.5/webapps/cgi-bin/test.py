import sys

res = """hmqskld
mqsd
lgfmlq
1234"""


print "Content-type:text/html"
print "Content-length:%s" %(len(res)+res.count('\n'))
print
sys.stdout.write(res.replace('\r\n','\n'))
