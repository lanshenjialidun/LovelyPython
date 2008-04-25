print "<html>\n"
Include("header.htm")
print "<h2>This is a demo for the Include() function</h2>"
info="A footer demo"
Include("footer.py?what=this_is_a_query_string",quote="my quote")
print "Value of THIS.name in includer script : %s" %THIS.name
print "\n</body>\n"
print "</html>"