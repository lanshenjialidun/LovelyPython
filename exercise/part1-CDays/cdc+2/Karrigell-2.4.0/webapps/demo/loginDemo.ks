Login()

def index():
    print 'This is a login demo'
    if LOGGED_USER:
        print 'User is <b>%s</b>' %LOGGED_USER