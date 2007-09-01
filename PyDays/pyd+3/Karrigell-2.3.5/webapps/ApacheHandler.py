"""Handler for mod_python
Original version by Andrew Nelis
"""

import os
import sys
root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root)
os.chdir(root)

import KarrigellRequestHandler, webservers.CustomHTTPServer
import cgi
from mod_python import apache

class RequestHandler(KarrigellRequestHandler.KarrigellRequestHandler, 
    webservers.CustomHTTPServer.RequestHandler):

    def __init__(self,req):
        self.req = req
        self.headers = req.headers_in
        self.client_address = req.connection.remote_addr
        self.command = req.method
        environ = {'REQUEST_METHOD': req.method}
        self.body = cgi.FieldStorage(fp = self.req,
            headers = self.headers, environ = environ)
        self.path = req.unparsed_uri
        self.wfile = req

    def log_error(self, *args):
        """ Not used for now. stderror = Apache error log. """
        pass

    def send_response(self, code, message):
        """ Set mod_python status to whatever HTTP code we need """
        self.req.status = code

    def send_header(self, key, value):
        """ Set mod_python headers to be sent """
        if key.lower() == "content-type":
            self.req.content_type = value
        else:
            self.req.headers_out[key] = str(value)

    def end_headers(self):
        """ Don't need to explicitly end headers in mod_python """
        pass


def handler(req):
    handler = RequestHandler(req)
    req.content_type = 'text/html' # default
    handler.handle_data()
    return apache.OK