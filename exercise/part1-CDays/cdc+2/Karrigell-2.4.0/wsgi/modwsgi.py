import os
import sys

here = os.path.dirname(__file__)
root = os.path.normpath(os.path.join(here, '..'))

os.chdir(root)

if not root in sys.path:
    sys.path.append(root)

import cgi
import CGIHTTPServer
import KarrigellRequestHandler

class RequestHandler(KarrigellRequestHandler.KarrigellRequestHandler,
    CGIHTTPServer.CGIHTTPRequestHandler):

    def __init__(self, environ, start_response):

        self.server = "wsgi"
        self.server_version = environ["SERVER_SOFTWARE"]
        self.sys_version = sys.version
        self.request = environ['wsgi.input']
        self.client_address = (environ["REMOTE_ADDR"],
            int(environ["REMOTE_PORT"]))

        self.headers = {}
        for k in environ:
            if k.startswith("HTTP_"):
                header = k[5:].replace('_', '-')
                self.headers[header] = environ[k]

        self.path = environ["REQUEST_URI"]
        self.request_version = environ["SERVER_PROTOCOL"]
        self.protocol_version = environ["SERVER_PROTOCOL"]
        self.command = environ["REQUEST_METHOD"]
        self.requestline = "%s %s %s" %(environ["REQUEST_METHOD"],
            environ["REQUEST_URI"],environ["SERVER_PROTOCOL"])
        if self.command == "POST":
            self.body = cgi.FieldStorage(fp=environ['wsgi.input'],
                environ=environ, keep_blank_values=1)

        self.__status = 0
        self.__message = None
        self.__headers = {}
        self.__output = None

        self.__start = start_response

        class output: pass
        self.wfile = output()
        self.wfile.write = self.write_content

    def send_response(self, code, message=None):
        self.__status = code
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = str(code)
        self.__message = message

    def send_header(self, key, value):
        self.__headers[key] = str(value)

    def end_headers(self):
        self.write_content(None)

    def write_content(self, data):
        if not self.__output:
            status_line = "%d %s" % (self.__status, self.__message)
            self.__output = self.__start(status_line, self.__headers.items())
        if data:
            self.__output(data)

    def flush_response(self):
        self.write_content(None)

warning = """
CONFIGURATION ERROR

Note: Karrigell is not safe to run in a multithread server process.

It is also not recommended that Karrigell be run within the actual Apache
child processes, as the fact that Karrigell keeps changing the current
working directory could interfere with other hosted Apache applications.
Correspondingly, other Apache applications could interfere with Karrigell
if they also change the current working directory. The safest way to run
Karrigell is with mod_wsgi in 'daemon' mode. This can be enabled using
the additional configuration:

  WSGIDaemonProcess karrigell processes=5 threads=1
  WSGIProcessGroup karrigell

The WSGIDaemonProcess directive should appear at global scope within the
Apache configuration, and the WSGIProcessGroup directive with the virtual
host or directory container pertaining to the Karrigell application.
"""

def application(environ, start_response):
    if environ['wsgi.multithread'] or not environ['mod_wsgi.process_group']:
        headers = [
            ('Content-Length', str(len(warning))),
            ('Content-Type', 'text/plain'),
        ]
        start_response('500 Internal Server Error', headers)
        return [warning] 

    handler = RequestHandler(environ, start_response)
    handler.handle_data()
    handler.flush_response()
    return []