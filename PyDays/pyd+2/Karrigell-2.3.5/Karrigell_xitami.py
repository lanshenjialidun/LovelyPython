"""Launches Karrigell for use with the Xitami web server

Xitami is a small, fast, and powerful multiplatform Open Source web server.
See http://www.xitami.com

The link between xitami and Karrigell uses the "long running web process"
(LRWP), a sort of FastCGI. It uses the lrwplib module, Copyright (c) 1997 
by Total Control Software

Published under the BSD licence. See the file LICENCE.txt

"""

import SimpleHTTPServer, KarrigellRequestHandler, k_config, URLResolution
import urlparse

class RequestHandler(KarrigellRequestHandler.KarrigellRequestHandler,
    SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    def __init__(self, request):
        self.request = request
        fs=request.getFieldStorage()
        self.headers={}
        for item in request.env.keys():
            if item.startswith("HTTP_"):
                hd=item[5:]
                self.headers[hd.lower()]=request.env[item]
        self.command = request.env['REQUEST_METHOD']
        self.body = {}
        if self.command == 'POST':
            self.body=fs
            """for item in fs.keys():
                if isinstance(fs[item],list):
                    self.body[item]=[ x.value for x in fs[item] ]
                else:
                    if fs[item].filename:
                        # file upload
                        self.body[item]= [ fs[item] ]                    
                    else:
                        self.body[item]= [ fs[item].value ]"""

        self.wfile = request.out
        self.client_address=(request.env["REMOTE_ADDR"],0)
        self.path=self.path_without_qs=request.env["SCRIPT_PATH"]+\
            request.env["PATH_INFO"]
        if request.env.has_key("QUERY_STRING"):
            self.path+="?"+request.env["QUERY_STRING"]
        self.request_version=request.env["SERVER_PROTOCOL"]
        self.requestline="%s %s %s" %(request.env["SERVER_PROTOCOL"],
            request.env["REQUEST_METHOD"],self.path)
        try:
            self.handle_data()
        finally:
            sys.exc_traceback = None    # Help garbage collection

# xitami will serve requests to http://host/karrigell/... through Karrigell
karrigellUrl="karrigell"    # this url can be changed at user's preferences
k_config.base='/'+karrigellUrl

print "Karrigell %s running on port %s" %(KarrigellRequestHandler.__version__,k_config.port)
if k_config.debug:
    print "Debug level %s" %k_config.debug
if k_config.silent:
    print "Silent mode"

# Launch the server
import sys, cgi
import webservers.lrwplib

#
# One-time LRWP startup logic: connect to local Xitami
# to serve a the request at location defined in karrigellUrl
#
try:
  lrwp = webservers.lrwplib.LRWP(karrigellUrl, '127.0.0.1', 81, '')
  lrwp.connect()
  print "Connected to Xitami, serves requests at url http://host/%s" %karrigellUrl
  sys.stdout.flush()
except:
  raise # comment this out when connection works
  sys.exit("Could not start long-running web process.")

while 1:
  #
  # Per-request code
  #
  request = lrwp.acceptRequest()   # blocks until server has work
  RequestHandler(request)

#
# LRWP Process termination
#
lrwp.close()