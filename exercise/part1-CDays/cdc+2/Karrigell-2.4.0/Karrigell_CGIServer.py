#! /usr/bin/python 
"""Karrigell HTTP Server

Written by Pierre Quentel quentel.pierre@wanadoo.fr

Published under the BSD licence. See the file LICENCE.txt

This script launches Karrigell with SocketServer.TCPServer as web server

Requests are handled by class RequestHandler (one instance per request)
"""

import os
import CGIHTTPServer
import KarrigellRequestHandler
import k_config
import k_utils

CGIHTTPServer.executable = lambda x:True

class RequestHandler(CGIHTTPServer.CGIHTTPRequestHandler):
    
    def send_head(self):
        """Version of send_head that support CGI scripts"""
        self.cgi_info = "cgi-bin","start.py"
        os.chdir(os.path.join(k_config.rootDir,"cgi-bin"))
        os.environ["REMOTE_PORT"] = str(self.client_address[1])
        os.environ["REQUEST_URI"] = self.path
        return self.run_cgi()

    def translate_path(self,path):
        parts = path.split("/")
        k_utils.trace(os.path.join(k_config.rootDir,*parts))
        return os.path.join(k_config.rootDir,*parts)

if k_config.silent:
    import sys
    sys.stdout = k_utils.silent()
    sys.stderr = k_utils.silent()

if k_config.debug:
    print "Debug level %s" %k_config.debug

# Launch the server
import SocketServer
server=SocketServer.TCPServer(('', k_config.port), RequestHandler)
server.server_name = "Karrigell_CGIServer"
server.server_port = k_config.port
print "Karrigell %s running on port %s" \
    %(KarrigellRequestHandler.__version__,k_config.port)
print "Press Ctrl+C to stop"

try:
    server.serve_forever()
except KeyboardInterrupt:
    k_utils.trace("Ctrl+C pressed. Shutting down.")
