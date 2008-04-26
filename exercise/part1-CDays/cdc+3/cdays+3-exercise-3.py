#!/bin/python
#coding:utf-8
'''cdays+3-exercise-3.py using Thread and Event
    @author: U{shengyan<mailto:shengyan1985@gmail.com>}
    @version:$Id$
'''
from threading import Thread
from threading import Event
import time

class myThread(Thread):
	'''myThread
		user-defined thread
	'''
	def __init__(self, threadname):
		Thread.__init__(self, name = threadname)

	def run(self):
		global event
		global share_var
		if event.isSet():				#判断event的信号标志
			event.clear()				#若设置了，则清除
			event.wait()				#并调用wait方法
			#time.sleep(2)
			share_var += 1			#修改共享变量
			print '%s ==> %d' % (self.getName(), share_var)
		else:
			share_var += 1			#未设置，则直接修改
			print '%s ==> %d' % (self.getName(), share_var)
			#time.sleep(1)
			event.set()				#设置信号标志
        
if __name__ == "__main__":
	share_var = 0
	event = Event()					#创建Event对象
	event.set()						#设置内部信号标志为真
	threadlist = []

	for i in range(10):					#创建10个线程
		my = myThread('Thread%d' % i)
		threadlist.append(my)
	for i in threadlist:				#开启10个线程
		i.start()
