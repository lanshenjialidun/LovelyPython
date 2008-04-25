#!/bin/python
from threading import Thread
from threading import RLock
import time

class myThread(Thread):
    def __init__(self, threadname):
        Thread.__init__(self, name = threadname)
    def run(self):
        global share_var
        lock.acquire()
        share_var += 1
        #time.sleep(2)
        print share_var
        lock.release()
        
if __name__ == "__main__":
    share_var = 0
    lock = RLock()
    threadlist = []

    for i in range(10):
        my = myThread('Thread%d' % i)
        threadlist.append(my)
    for i in threadlist:
        i.start()
