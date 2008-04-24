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
    fp.close()
    codedetect = chardet.detect(blog)["encoding"]
    if codedetect <> 'utf-8':
        try:
            blog = unicode(blog, codedetect)                            #######problem
            print blog
            blog = blog.encode('utf8')
        except:
            print u"bad unicode encode try!"
            return 0
    filename = '%s_utf-8' % blogurl[7:]
    filename = filename.replace('/', '_')
    open(filename, 'w').write('%s' % blog)
    return 1
    
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'usage:\n\tpython CDays-1-2.py http://xxxx.com'
    else:
        blog_detect(sys.argv[1])
