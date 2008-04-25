import k_utils
print COOKIE
print "<br>",k_utils.is_logged(COOKIE)

import PyDbLite
db = PyDbLite.Base(os.path.join(CONFIG.serverDir,"data","users.pdl"))
db.open()
for k in "skey","login":
    if not k in COOKIE.keys():
        print "%s not in cookie keys" %k
        raise SCRIPT_END
user = db(login=COOKIE["login"].value)
if not user:
    print "no user"
    raise SCRIPT_END
if user[0]["session_key"] != COOKIE["skey"].value:
    print "session key mismatch"
    print user[0]
    print "<br>PyDbLite",PyDbLite.__file__
    print "<br>Fields",db.fields
    print "<br><b>users</b><br>"
    for r in db():
        print '<br>',r
    raise SCRIPT_END
# authenticated user : update number of visits and last visit time
print "ok"