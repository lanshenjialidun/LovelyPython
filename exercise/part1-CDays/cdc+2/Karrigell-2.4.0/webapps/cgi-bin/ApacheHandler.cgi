#!/usr/bin/python

import os
import sys
import CGIHTTPServer
import cgi

import cStringIO

# set the current directory to the one where Karrigell.py stands
# if this script is in /cgi-bin and Karrigell is in /www/karrigell

root = os.path.dirname(os.getcwd())
os.chdir(os.path.join(root,"www","karrigell"))

initFile = os.path.join(root,"www","karrigell","Karrigell_Apache.ini")
sys.argv = [ os.path.join(root,"www","karrigell","ApacheHandler.cgi"),
    "-R",os.path.join(root,"www"),initFile]

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

import KarrigellRequestHandler

class RequestHandler(KarrigellRequestHandler.KarrigellRequestHandler,
    CGIHTTPServer.CGIHTTPRequestHandler):

    def __init__(self, server, request, client_address):
        env = os.environ
        self.server = server
        self.server_version = os.environ["SERVER_SOFTWARE"]
        self.sys_version = sys.version
        self.request, self.client_address = request, client_address
        self.wfile = sys.stdout
        self.headers = {}
        for k in os.environ:
            if k.startswith("HTTP_"):
                header = k[5:].replace('_','-')
                self.headers[header] = os.environ[k]
        self.path = os.environ["REQUEST_URI"]
        self.request_version = env["SERVER_PROTOCOL"]
        self.protocol_version = env["SERVER_PROTOCOL"]
        self.command = env["REQUEST_METHOD"]
        self.requestline = "%s %s %s" %(env["REQUEST_METHOD"],
            env["REQUEST_URI"],env["SERVER_PROTOCOL"])
        if self.command == "POST":
            self.body = cgi.FieldStorage(keep_blank_values = 1)

    def send_response(self, code, message=None):
        """Don't send response code : Apache sends 200 Ok, 
        except if a Status header is sent
        """
        if code==304:
            self.send_header('Status','304 Not modified')
        elif code==302:
            self.send_header('Status','302 Found')
        elif code==401:
            self.send_header('Status','401 Unauthorized')
    
request = sys.stdin
client_address = (os.environ["REMOTE_ADDR"],int(os.environ["REMOTE_PORT"]))
handler = RequestHandler("Apache",request,client_address)

# on windows all \n are converted to \r\n if stdout is a terminal 
# and is not set to binary mode
# this will then cause an incorrect Content-length.
if sys.platform == "win32":
    import  msvcrt
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

handler.handle_data()
