# -*- coding: utf-8 -*-
#实现每隔2秒钟向test中写入一个随机数。
import random
import time

def write_f():
    file = open("test", "a")
    while 1:
        afloat = random.random()
        print afloat
        file.write('%s\n' % afloat)
        file.flush()
        time.sleep(2)
    file.close()

if __name__ == '__main__':
    write_f()