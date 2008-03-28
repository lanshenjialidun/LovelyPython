"""A small long-running web process for Xitami.

Takes a run-time argument and returns this plus a call count
each time it is called, terminating after ten calls.

Responds to http://localhost/test (line 19)

"""

import sys, cgi
myname = "test"
callcount = 0
import lrwplib
#
# One-time LRWP startup logic: connect to local Xitami
# to serve a fixed number of application "lrtest" requests
#
try:
  lrwp = lrwplib.LRWP("test", '127.0.0.1', 81, '')
  lrwp.connect()
  print "Connected to Xitami"
  sys.stdout.flush()
except:
  raise # comment this out when connection works
  sys.exit("Could not start long-running web process.")

while 1:
  #
  # Per-request code
  #
  request = lrwp.acceptRequest()   # blocks until server has work
  query = request.getFieldStorage()  # retrieve task as a CGI call
  callcount += 1
  #
  # Page generation logic
  #
  #request.out.write("""Content-Type: text/html\n\n""")
  request.out.write("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2     Final//EN">
  <html>
  <head>
  <title>LONG-RUNNING WEB PROCESS %s</title>
  </head>
  <body>
  """ % myname)
  request.out.write("""<H1>Process %s, call %d</H1>""" % (myname,     callcount))
  request.out.write("""<H1>request.env</H1>""")
  request.out.write("<table>")
  for item in request.env.keys():
      request.out.write("<tr><td>%s</td><td>%s</td>" %(item,cgi.escape(request.env[item])))
  request.out.write("</table>")
  request.out.write("""<H1>Query</H1>""")
  request.out.write("<table>")
  for item in query.keys():
      request.out.write("<tr><td>%s</td><td>%s</td>" %(item,cgi.escape(query[item].value)))
  request.out.write("</table>")
  request.out.write("""
</body>
</html>
""")
  request.finish()

#
# LRWP Process termination
#
lrwp.close()