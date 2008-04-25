def index():
    print """<form action = "set_cookie">
        What is your name ? <input name="login">
        <input type="submit" value="Ok">
        </form>"""

def set_cookie(login):
    if _is_valid(login):
        SET_COOKIE['mylogin'] = login
        print '<a href="cookie_test">Test me</a>'
    else:
        print "Unknown user"

def cookie_test():
    print "Hello",COOKIE['mylogin'].value

def _is_valid(login):
    # replace this by the test you like
    return login in ['one','two','three']