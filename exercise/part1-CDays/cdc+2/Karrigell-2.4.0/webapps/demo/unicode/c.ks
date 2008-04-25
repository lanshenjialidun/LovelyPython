#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding directive is needed only if you write non-ascii
# values directly in text

import cgi

def index(par='default'):
    print '''
<form action="index" method="post">
<input type="submit" value="OK">
<input name="par">
</form>
    <hr>

'''
    print "Escaped repr of the parameter: `par` ="
    print cgi.escape(`par`)
    print "<hr>"
    print "Escaped parameter par ="
    print cgi.escape(par)
    print "<hr>"
    print "Unescaped parameter:", par

    

