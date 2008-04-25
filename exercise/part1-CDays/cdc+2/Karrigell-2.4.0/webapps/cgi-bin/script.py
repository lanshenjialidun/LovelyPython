import cgi

print "content-type: text/html"
print
print cgi.FieldStorage()
print cgi.parse_qs(os.environ["QUERY_STRING"])