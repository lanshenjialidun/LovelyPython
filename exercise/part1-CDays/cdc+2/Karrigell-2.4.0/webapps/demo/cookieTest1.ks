def index():
    print """<form action = "set_cookie">
        What is your name ? <input name="login">
        <input type="submit" value="Ok">
        </form>"""

def set_cookie(login):
    SET_COOKIE['mylogin'] = login
    SET_COOKIE['mylogin']['path']='/'
    print '<a href="../cookieApp.ks">Test me</a>'
