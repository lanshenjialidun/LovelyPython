#!/bin/python
from threading import Thread
from threading import Event
import time
class myThread(Thread):
    def __init__(self, threadname):
        Thread.__init__(self, name = threadname)
    def run(self):
        global event
        global share_var
        if event.isSet():
            event.clear()
            event.wait()
            #time.sleep(2)
            share_var += 1
            print '%s ==> %d' % (self.getName(), share_var)
        else:
            share_var += 1
            print '%s ==> %d' % (self.getName(), share_var)
            #time.sleep(1)
            event.set()
        
if __name__ == "__main__":
    share_var = 0
    event = Event()
    event.set()
    threadlist = []

    for i in range(10):
        my = myThread('Thread%d' % i)
        threadlist.append(my)
    for i in threadlist:
        i.start()
