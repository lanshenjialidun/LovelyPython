print "<p>QUERY %s" %QUERY
import os
print os.environ
#print "<br>Spam is",_spam,"unicode",isinstance(_spam,unicode)
if QUERY.has_key("animal"):
    print "<br>Animal is",str(QUERY["animal"])
