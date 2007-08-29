"""Custom HTTP server based on SimpleHTTPServer
Handles POST request
Subclasses of RequestHandler only have to override the handle_data() method
"""

import cgi
import select
import SimpleHTTPServer

class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        """Begin serving a GET request"""
        # nothing more to do before handle_data()
        self.body = {}
        self.handle_data()
        
    def do_POST(self):
        """Begin serving a POST request. The request data must be readable
        on a file-like object called self.rfile"""
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        self.body = cgi.FieldStorage(fp=self.rfile,
            headers=self.headers, environ = {'REQUEST_METHOD':'POST'},
            keep_blank_values = 1, strict_parsing = 1)
        # throw away additional data [see bug #427345]
        while select.select([self.rfile._sock], [], [], 0)[0]:
            if not self.rfile._sock.recv(1):
                break
        self.handle_data()

    def handle_data(self):
        """Class to override"""
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)

if __name__=="__main__":
    # launch the server on port 80
    import SocketServer
    s=SocketServer.TCPServer(('',80),RequestHandler)
    print "CustomHTTPServer running on port 80"
    s.serve_forever()