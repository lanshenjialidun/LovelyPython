#!/usr/bin/python

import os
import sys
import CGIHTTPServer
import cgi

import cStringIO

# set the current directory to the one where Karrigell.py stands
# if this script is in /cgi-bin and Karrigell is in /www/karrigell

root = os.path.dirname(os.path.dirname(os.getcwd()))
os.chdir(root)

initFile = os.path.join(root,"Karrigell_Apache.ini")
sys.argv = [ os.path.join(root,"ApacheHandler.cgi"),
    "-R",root,initFile]

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

import KarrigellRequestHandler

