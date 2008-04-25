def index():
    # check if user is the administrator
    Login(role=["admin","edit"])

    # only shows is Login successful
    print "Logged in as ",Role()
    print "<br>",Logout()
