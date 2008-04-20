#!/usr/bin/env python
print "Content-type: text/html"
print
import cgi
form=cgi.FieldStorage()
x,y = form.getvalue("val").split(',')
x,y = int(x),int(y)
print "<table>"
for i in range(y):
    print "<tr>"
    for j in range(x):
        print "<td>%dx%d</td>" % (j,i)
    print "</tr>"
print "</table>"

cgi.print_directory()
cgi.print_form(form)