#coding:utf-8
#实现每隔1秒钟读取test中的内容。
import time

def read_f():
    file = open("test", "r")
    while 1:
        content = file.readline()
        if not content:
            time.sleep(1)
        else:
            print content
    file.close()

if __name__ == '__main__':
    read_f()