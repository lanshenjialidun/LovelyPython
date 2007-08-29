"""Default script executed by the Login() function in scripts"""

if COOKIE.has_key('logged_user'):
    print COOKIE['logged_user'].value
    print '<br><a href="/utils/login.ks/logout?or_url=%s>Logout</a>'\
        %PATH
else:
    print '<a href="/utils/login.ks/login?or_url=%s">Login</a>'\
        %PATH
