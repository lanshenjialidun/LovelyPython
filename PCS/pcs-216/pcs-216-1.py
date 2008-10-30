# coding:utf-8
import socket
# 监听本机5678端口，当有客户端请求时，回复指定字符串

host = '127.0.0.1 '
port = 5678

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#创建采用TCP协议的socket对象
s.bind((host, port))
#绑定socket
s.listen(1)
#服务器监听连接

while 1:
#这里的whil循环，可以使程序多地响应多客户端的请求
    clientSocket,clientAddr = s.accept()
    #接受客户端连接
    print 'Client connected!'
    clientSocket.sendall('Welcome to Python World!')
    #向客户端发送字符串
    clientSocket.close()
    #关闭与客户端的连接
