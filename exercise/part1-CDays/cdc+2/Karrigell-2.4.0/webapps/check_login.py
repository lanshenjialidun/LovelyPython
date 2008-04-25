"""Script called by the form in login.pih
Checks if login and password are those of the site admin
If so, redirect to the original script where login was required
(the one with the built-in function Login() )

Override if necessary"""

import os
import md5
import k_config

digest=open(os.path.join(k_config.serverDir,"admin","admin.ini"),"rb").read()
userDigest=digest[:16]
passwordDigest=digest[16:]

test = (md5.new(_login).digest()==userDigest \
        and md5.new(_passwd).digest()==passwordDigest)

if test:
    SET_COOKIE['LOGGED'] = "logged"
    SET_COOKIE['LOGGED']['path'] = _baseurl
    
    raise HTTP_REDIRECTION,_path
else:
    print "Authentication failed"