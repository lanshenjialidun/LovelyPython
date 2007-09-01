import os
import sys
import socket
import urllib

class Response:

    def __init__(self,s):
        res = ''
        while True:
            buff = s.recv(1024)
            if not buff:
                break
            res += buff
        self.resp_line,self.headers,self.body = self.parse_response(res)

    def parse_response(self,resp):
        lines = resp.split('\n')
        resp_line = lines[0].rstrip()
        if len(lines)==1:
            return resp_line,None,None
        headers = []
        for i,line in enumerate(lines[1:]):
            if line.strip():
                headers.append(line.rstrip())
            else:
                break
        body = '\n'.join(lines[i+2:])
        return resp_line,headers,body

PORT = 80

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
while True:
    try:
        s.connect(('localhost',PORT))
        break
    except:
        pass
s.close()

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',PORT))

s.send('HEAD / HTTP/1.1\r\n')
s.send('\r\n')
res = Response(s) 

print 'HEAD /',res.resp_line

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',PORT))
s.send('GET /index.html HTTP/1.1\r\n')
s.send('\r\n')
res = Response(s)
print res.body == file(os.path.normpath('../webapps/index.html'),'rb').read()
print 'GET /index.html',res.resp_line

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',PORT))
s.send('GET /demo/calendar/delete.gif HTTP/1.1\r\n')
s.send('\r\n')
res = Response(s)
print res.headers
print 'GET /demo/calendar/delete.gif',res.resp_line

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',PORT))
s.send('HEAD /demo/calendar/delete.gif HTTP/1.1\r\n')
s.send('\r\n')
res = Response(s)
print 'HEAD /demo/calendar/delete.gif',res.resp_line
print 'headers',res.headers

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',PORT))
s.send('HEAD /index.html HTTP/1.1\r\n')
s.send('\r\n')
res = Response(s)
print 'HEAD /index.html',res.resp_line

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',PORT))
s.send('HEAD /index1.html HTTP/1.1\r\n')
s.send('\r\n')
res = Response(s)
print 'HEAD /index1.html',res.resp_line

res = urllib.urlopen('http://localhost:%s/index.html' %PORT)
print len(res.read())

body = urllib.urlencode({'spam':'lqhglg'})
res = urllib.urlopen('http://localhost:%s/demo/myScript.py' %PORT,body)
print res.info()

s.send('HEAD /index.html HTTP/1.1\r\n')
s.send('\r\n')
res = Response(s) 
print 'HEAD /'
print res.resp_line
