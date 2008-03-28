import cgi
import os

print "Content-type: text/html"
print
print cgi.FieldStorage()
raise SCRIPT_END
print '<p>query string ',os.environ['QUERY_STRING']
