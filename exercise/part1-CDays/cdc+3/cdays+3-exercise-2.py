#!/bin/python
#coding:utf-8
'''cdays+3-exercise-2.py 使用Thread和Queue保持多线程间同步
    @author: U{shengyan<mailto:shengyan1985@gmail.com>}
    @version:$Id$
'''
from threading import Thread
import Queue
import time

class Input(Thread):
	'''输入线程： 从标准输入中读一个string，然后把该string加入到queue
	'''
	def __init__(self, threadname):
		Thread.__init__(self, name = threadname)
	def run(self):
		some_string = raw_input('please input something for thread %s:' % self.getName())	#输入一个字符串
		global queue
		queue.put((self.getName(), some_string))											#加入到队列
		#time.sleep(5)																#延时一段时间
        
class Output(Thread):
	'''输出线程：从queue中得到一个string，并将它输出到屏幕
	'''
	def __init__(self, threadname):
		Thread.__init__(self, name = threadname)
	def run(self):
		global queue
		(iThread, something) = queue.get()												#从queue中读取
		print 'Thread %s get "%s" from Thread %s' % (self.getName(), something, iThread)		#输出

if __name__ == "__main__":
    queue = Queue.Queue()																#创建Queue对象
    inputlist = []
    outputlist = []
    for i in range(10):
        il = Input('InputThread%d' % i)														#输入线程列表
        inputlist.append(il)
        ol = Output('outputThread%d' % i)													#输出线程列表
        outputlist.append(ol)
    for i in inputlist:
        i.start()																			#依次开始输入线程	
        i.join()																			#等待
    for i in outputlist:
        i.start()																			#依次开始输出线程
        #i.join()
