#!/bin/python
from threading import Thread
import Queue
import time

class Input(Thread):
    def __init__(self, threadname):
        Thread.__init__(self, name = threadname)
    def run(self):
        some_string = raw_input('please input something for thread %s:' % self.getName())
        global queue
        queue.put((self.getName(), some_string))
        #time.sleep(5)
        
class Output(Thread):
    def __init__(self, threadname):
        Thread.__init__(self, name = threadname)
    def run(self):
        global queue
        (iThread, something) = queue.get()
        print 'Thread %s get "%s" from Thread %s' % (self.getName(), something, iThread)

if __name__ == "__main__":
    queue = Queue.Queue()
    inputlist = []
    outputlist = []
    for i in range(10):
        il = Input('InputThread%d' % i)
        inputlist.append(il)
        ol = Output('outputThread%d' % i)
        outputlist.append(ol)
    for i in inputlist:
        i.start()
        i.join()
    for i in outputlist:
        i.start()
        #i.join()
