#!/usr/bin/env python
# encoding: utf-8
"""
syncwiki.py

Created by QingFeng on 2008-09-05.
Copyright (c) 2008 woodpecker. All rights reserved.
"""

from twill.commands import *
from time import sleep
import os

USERNAME = ''
PASSWORD = ''

def login():
    go("http://wiki.woodpecker.org.cn/moin/ObpLovelyPython?action=login")
    showforms()

    fv(3,"name", USERNAME)
    fv(3,"password", PASSWORD)
    showforms()
    submit(0)

def execute_cmd(data):
    go("http://wiki.woodpecker.org.cn/moin/ObpLovelyPython/%(pcs)s?action=edit"%data)
    showforms()
    fv(1,"savetext","%(body)s"%data)
    submit()
    
def main(fname,pagename):
    text=open(fname).read()
    data = {'pcs':pagename,
        'body':text,
        'username':USERNAME,'password':PASSWORD,
    }
    cmd=execute_cmd(data)
    # print execute_string(cmd)

if __name__ == '__main__':
    errpages,winpages=[],[]
    cmd='find . -name "*.moin"'
    login()
    for r in os.popen(cmd):
        r = r.strip()
        fname,ext = os.path.splitext(r)
        pagename = os.path.basename(fname)
        pagename = "".join(pagename.upper().split("-"))
        print "pagename:",pagename
        try:
            main(fname=r,pagename=pagename)
            winpages.append(pagename)
        except:
            errpages.append(pagename)
        sleep(5)
    print "error pages:%s"%" ".join(errpages)
    print "win pages:%s"%" ".join(winpages)
