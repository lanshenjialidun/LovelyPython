"""Karrigell HTTP Server

Written by Pierre Quentel quentel.pierre@wanadoo.fr

Published under the BSD licence. See the file LICENCE.txt

This script launches Karrigell with webservers.SimpleAsyncHTTPServer.Server as web server.
It is built on the asyncore/asynchat framework (non-blocking sockets, use of
the select() function) and partly copied from the medusa web server

References :
- medusa : http://www.amk.ca/python/code/medusa.html for medusa
- Sockets HOWTO on www.python.org

Requests are handled by class RequestHandler (one instance per request)
"""

import webservers.SimpleAsyncHTTPServer
import KarrigellRequestHandler
import k_config
import traceback
import sys

class asyncRequestHandler(webservers.SimpleAsyncHTTPServer.DialogManager,
    KarrigellRequestHandler.KarrigellRequestHandler):
    
    def handle_data(self):
        KarrigellRequestHandler.KarrigellRequestHandler.handle_data(self)
    
    def send_error(self, code, message=None):
        KarrigellRequestHandler.KarrigellRequestHandler.send_error(self,code,message)

    def handle_error(self):
        traceback.print_exc(file=sys.stderr)

# Launch the server

s=webservers.SimpleAsyncHTTPServer.Server(('',k_config.port),asyncRequestHandler)
print "Karrigell %s running on port %s" %(KarrigellRequestHandler.__version__,k_config.port)
if k_config.debug:
    print "Debug level %s" %k_config.debug
if k_config.silent:
    print "Silent mode"

import thread
# start the server in a different thread
thread.start_new_thread(s.loop, ())

# GUI to stop the server and log
from Tkinter import *
from ScrolledText import ScrolledText
import tkFont

class Output:

    maxlines = 100

    def __init__(self,textWidget):
        self.textWidget = textWidget
    
    def write(self,data):
        self.textWidget.insert(END,data)
        l = int(self.textWidget.index(END).split('.')[0])
        if l > self.maxlines:
            self.textWidget.delete(1.0,'%s.0' %(l-self.maxlines))
        self.textWidget.see(END)        

def stop_server():
    s.close_all()
    sys.exit()

root = Tk()
Button(root,text="Stop server",command = stop_server).pack()
tw = ScrolledText(root,width=80,height=40,bg="black",foreground="white",
    font=tkFont.Font(family="courier",size=10,weight="bold"))
tw.pack()

sys.stderr = Output(tw)

root.mainloop()