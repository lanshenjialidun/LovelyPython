#!/bin/python
#coding:utf-8
'''cdays-1-exercise-2.py 熟悉chardet和urllib2
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
        fp = urllib2.urlopen(blogurl)                           #尝试打开给定url
    except Exception, e:                                        #若产生异常，则给出相关提示并返回
        print e
        print 'download exception %s' % blogurl
        return 0
    blog = fp.read()                                            #读取内容
    fp.close()                                                  #关闭
    codedetect = chardet.detect(blog)["encoding"]               #检测得到编码方式
    if codedetect <> 'utf-8':                                   #是否是utf-8
        try:
            blog = unicode(blog, codedetect)                    #不是的话，则尝试转换
            #print blog
            blog = blog.encode('utf-8')
        except:
            print u"bad unicode encode try!"
            return 0
    filename = '%s_utf-8' % blogurl[7:]                         #保存入文件
    filename = filename.replace('/', '_')
    open(filename, 'w').write('%s' % blog)
    print 'save to file %s' % filename
    return 1
    
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'usage:\n\tpython cdays-1-exercise-2.py http://xxxx.com'
    else:
        blog_detect(sys.argv[1])
