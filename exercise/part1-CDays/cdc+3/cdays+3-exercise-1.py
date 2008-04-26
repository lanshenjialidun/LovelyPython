#!/bin/python
#coding:utf-8
'''cdays+3-exercise-1.py using Thread and RLock
    @author: U{shengyan<mailto:shengyan1985@gmail.com>}
    @version:$Id$
'''
from threading import Thread
from threading import RLock
import time

class myThread(Thread):
	'''myThread
		user-defined thread
	'''
	def __init__(self, threadname):
		Thread.__init__(self, name = threadname)

	def run(self):
		global share_var				#共享一全局变量
		lock.acquire()				#调用lock的acquire，获得锁
		share_var += 1				#修改共享变量
		#time.sleep(2)
		print share_var
		lock.release()				#释放
        
if __name__ == "__main__":
	share_var = 0
	lock = RLock()
	threadlist = []

	for i in range(10):					#产生10个线程
		my = myThread('Thread%d' % i)
		threadlist.append(my)
	for i in threadlist:				#开始10个线程
		i.start()
