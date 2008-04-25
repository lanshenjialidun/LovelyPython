def index():
    print "<h1>My record collection</h1>"
    print '<a href="login">Login</a><br>'
    Include('../counter.py',counter_file='counter1.txt')

def login():
    print '<h1>Login</h1>'
    print '<form action="check_login" method="post">'
    print 'Login <input name="login"><br>'
    print 'Password <input type="password" name="passwd"><br>'
    print '<input type="submit" value="Ok">'
    print '</form>'

def check_login(login,passwd):
    if login=="john" and passwd=="doe":
        Session().user = login
    raise HTTP_REDIRECTION,"index"