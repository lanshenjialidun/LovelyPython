import os

import PyDbLite
import k_config
import ask

def _login_test(login,passwd):
    f = os.path.join(os.path.join(k_config.serverDir,'users',
        or_url.replace('/','_'))
    db = PyDbLite.Base(f).create('login','password',mode='open')
    db.create_index('login')
    r = db._login[login]
    if r and r[0]['password'] == passwd:
        return True

def login(or_url):
    ask.ask('Login','check_login',
        ('Login','login'),('Password','passwd','password'),
        ('or_url','hidden',or_url))

def check_login(login,passwd,or_url):
    if _login_test(login,passwd,or_url):
        SET_COOKIE['logged_user'] = login
        SET_COOKIE['logged_user']['path'] = or_url
        raise HTTP_REDIRECTION,or_url
    else:
        print 'Authentication failed.<a href="%s">Back</a>' %or_url

def logout(or_url):
    SET_COOKIE['logged_user'] = ""
    SET_COOKIE['logged_user']['path'] = or_url
    SET_COOKIE['logged_user']['max-age']=0
    raise HTTP_REDIRECTION,or_url