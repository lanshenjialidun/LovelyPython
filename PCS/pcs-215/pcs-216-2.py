# coding:utf-8
import socket
# 连接本机5678端口，并读取socket，将结果打印屏幕

host = '127.0.0.1'
port = 5678

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#创建采用TCP协议的socket对象
s.connect((host, port))
#连接指定的服务器端

while 1:
#从socket读取数据，并输出到屏幕，读完后退出程序
    buf = s.recv(2048)
    if not len(buf):
	break
    print buf
