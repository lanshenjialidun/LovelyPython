#!/bin/python
#coding:utf-8
'''cdays-1-exercise-1.py 
    @author: U{shengyan<mailto:shengyan1985@gmail.com>}
    @version:$Id$
    @note: 使用chardet和 urllib2
    @see: chardet使用文档: http://chardet.feedparser.org/docs/, urllib2使用参考: http://docs.python.org/lib/module-urllib2.html
'''

import sys
import urllib2
import chardet

def blog_detect(blogurl):
    '''
    检测blog的编码方式
    @param blogurl: 要检测blog的url
    '''
    try:
        fp = urllib2.urlopen(blogurl)                       #尝试打开给定url
    except Exception, e:                                    #若产生异常，则给出相关提示并返回
        print e
        print 'download exception %s' % blogurl
        return 0
    blog = fp.read()                                        #读取内容
    codedetect = chardet.detect(blog)["encoding"]           #检测得到编码方式
    print '%s\t<-\t%s' % (blogurl, codedetect)
    fp.close()                                              #关闭
    return 1
    
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'usage:\n\tpython cdays-1-exercise-1.py http://xxxx.com'
    else:
        blog_detect(sys.argv[1])
