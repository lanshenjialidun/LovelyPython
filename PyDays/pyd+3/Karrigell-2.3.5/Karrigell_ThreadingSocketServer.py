#! /usr/bin/python 
"""Karrigell HTTP Server

Written by Pierre Quentel quentel.pierre@wanadoo.fr

Published under the BSD licence. See the file LICENCE.txt

This script launches Karrigell with SocketServer.TCPServer as web server

Requests are handled by class RequestHandler (one instance per request)
"""

import os
import webservers.CustomHTTPServer
import KarrigellRequestHandler
import k_config

class RequestHandler(KarrigellRequestHandler.KarrigellRequestHandler,
    webservers.CustomHTTPServer.RequestHandler):
        pass

if k_config.silent:
    import sys
    import k_utils
    sys.stdout = k_utils.silent()
    sys.stderr = k_utils.silent()

if k_config.debug:
    print "Debug level %s" %k_config.debug

# Launch the server
import SocketServer
server=SocketServer.ThreadingTCPServer(('', k_config.port), RequestHandler)
print "Karrigell %s running on port %s" \
    %(KarrigellRequestHandler.__version__,k_config.port)
print "Press Ctrl+C to stop"

try:
    server.serve_forever()
except KeyboardInterrupt:
    print "Ctrl+C pressed. Shutting down."
