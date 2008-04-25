#!/bin/python
import sys
import os
import pickle

def add(n, w):
    myMessage.append((n, w))
    pickle.dump(myMessage,open("message.dump","w"))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'usage:\n\tpython CDays2-1.py name words'
    else:
        n = sys.argv[1].strip()
        w = sys.argv[2].strip()
        
        global myMessage
        myMessage = []
        try:
            myMessage = pickle.load(open("message.dump"))
            print myMessage
        except:
            pass
        add(n, w)
        print 'Done'
