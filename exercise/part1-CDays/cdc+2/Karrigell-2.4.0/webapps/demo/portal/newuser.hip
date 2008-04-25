from portalDb import db

if not _password==_password2:
    Include("header.hip")
    print "<center><p>%s" %_("You must enter the same password twice")
    raise SCRIPT_END

so=Session()

if len([ user for user in db['users'] if user["login"]==_login]):
    Include("header.hip")
    print "<center><p>%s <b>%s</b>"  %(_(" Login"),_login)
    print _("is already used, please choose another one")
    raise SCRIPT_END

import md5
pw = md5.new(_password).digest()
recno = db['users'].insert(_login,pw,"#AAA866","times")
db['users'].commit()

so.user=recno
so.login=_login

raise HTTP_REDIRECTION,"index.pih"
    