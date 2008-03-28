#! /usr/bin/python 

"""Karrigell HTTP Server

Written by Pierre Quentel quentel.pierre@wanadoo.fr

Published under the BSD licence. See the file LICENCE.txt

This script launches Karrigell with webservers.SimpleAsyncHTTPServer.Server as 
web server
It is an asynchronous server (uses non-blocking sockets and the select() 
function)

Requests are handled by class RequestHandler (one instance per request)
"""

import os
import traceback
import sys

import KarrigellRequestHandler
from core import k_config, k_utils
import webservers.SimpleAsyncHTTPServer as Server

class asyncRequestHandler(KarrigellRequestHandler.KarrigellRequestHandler, 
        Server.DialogManager):
    
    def handle_data(self):
        KarrigellRequestHandler.KarrigellRequestHandler.handle_data(self)
    
    def send_error(self, code, message=None):
        KarrigellRequestHandler.KarrigellRequestHandler.send_error(self,code,message)

    def handle_error(self):
        traceback.print_exc(file=sys.stderr)

if k_config.silent:
    sys.stdout = k_utils.silent()
    sys.stderr = k_utils.silent()
    
# Launch the server
s = Server.Server(('',k_config.port),asyncRequestHandler)
print "Karrigell %s running on port %s" %(KarrigellRequestHandler.__version__,k_config.port)
if k_config.debug:
    print "Debug level %s" %k_config.debug
print "Press Ctrl+C to stop"

try:
    s.loop()
except KeyboardInterrupt:
    s.close_all()
    k_utils.trace("Ctrl+C pressed. Shutting down.")
