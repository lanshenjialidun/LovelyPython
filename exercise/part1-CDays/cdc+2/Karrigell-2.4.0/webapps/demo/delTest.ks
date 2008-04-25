import sys

class myclass:
    def __init__(self):
        print >>sys.stderr, 'class created'
    def __del__(self):
        print >>sys.stderr, 'del called'

m = myclass()

def index():
    print "test" 