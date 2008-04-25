import time
print """<table>
<tr>
<td>%s</td>
<td>""" %info
print time.strftime("%d.%m.%y %H:%M",time.localtime(time.time()))
print "</td></tr></table>"
print quote+"<p>"
print "In query string : "+what+"<p>"
print "Value of THIS.name in footer script : %s" %THIS.name
print "<p>"
Include("includedFooter.py")
