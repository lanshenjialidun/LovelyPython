# authentication script

import md5

def displayAuthentError(message):
    Include("header.hip")
    "<center><p><b>%s : %s</b>" %(_("Authentication error"),message)
    raise SCRIPT_END

so=Session()
from portalDb import db

users = [ user for user in db['users'] if user["login"]==_login ]
if not len(users):
    displayAuthentError(_("unknown user"))
else:
    user = users[0]

pw=md5.new(_password).digest()
if pw==user["password"]:
    so.user=user["__id__"]
    so.login=user["login"]
    raise HTTP_REDIRECTION,"index.pih"
else:
    displayAuthentError(_("incorrect password"))
