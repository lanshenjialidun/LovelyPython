#!/bin/python
# -*- coding: utf-8 -*-

'''cdays+2-exercise-2.py
    @author: U{shengyan<mailto:shengyan1985@gmail.com>}
    @version:$Id$
'''
import sys
import pickle

def add(n, w):
    '''增加并保存一条信息
    @param n: 名字
    @param w: 信息内容
    '''
    myMessage.append((n, w))                        #增加一条消息
    pickle.dump(myMessage,open("message.dump","w")) #将myMessage对象保存

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'usage:\n\tpython cdays+2-exercise-2.py name words'
    else:
        n = sys.argv[1].strip()
        w = sys.argv[2].strip()
        
        global myMessage
        myMessage = []
        try:
            myMessage = pickle.load(open("message.dump"))   #从message.dump读取对象为全局变量myMessage
            print myMessage
        except:
            pass
        add(n, w)
        print 'Done'
