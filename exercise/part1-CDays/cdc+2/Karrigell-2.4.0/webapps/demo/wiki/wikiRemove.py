""" Removes the pages whose names are the keys of QUERY """

# check authentication
Include("wikiAuthent.py")

if not QUERY.keys():
    print 'No page to remove<p><a href="index.pih">Back</a>'
    raise SCRIPT_END
    
# get records to remove using their recno
from wikiBase import db

recs_to_remove = []
for r in _remove:
    recs_to_remove.append(db[int(r)])

if len(_remove) == 1:
    print "Deleting 1 page<p>\n"
else:
    print "Deleting %s pages<p>\n" %len(_remove)

# actually remove the records
for r in _remove:
    del db[int(r)]

print '<a href="index.pih">Back</a>'
