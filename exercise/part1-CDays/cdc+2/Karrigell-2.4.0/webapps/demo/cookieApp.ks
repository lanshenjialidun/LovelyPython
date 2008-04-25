if not SET_COOKIE.has_key('mylogin') or \
    not SET_COOKIE['mylogin'].value in ['one','two','three']:
        raise SCRIPT_ERROR,'Unknown user'

def index():
    print "Your application starts here"#, SET_COOKIE['mylogin'].value
    