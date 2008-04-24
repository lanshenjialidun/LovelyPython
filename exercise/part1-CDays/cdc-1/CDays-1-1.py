#!/bin/python
import sys
import urllib2
import chardet

def blog_detect(blogurl):
    try:
        fp = urllib2.urlopen(blogurl)
    except Exception, e:
        print e
        print 'download exception %s' % blogurl
        return 0
    blog = fp.read()
    codedetect = chardet.detect(blog)["encoding"]
    print '%s\t<-\t%s' % (blogurl, codedetect)
    fp.close()
    return 1
    
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'usage:\n\tpython CDays-1-1.py http://xxxx.com'
    else:
        blog_detect(sys.argv[1])
