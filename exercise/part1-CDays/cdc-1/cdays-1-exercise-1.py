#!/bin/python
#coding:utf-8
'''cdays-1-exercise-1.py using chardet and urllib2
    @author: U{shengyan<mailto:shengyan1985@gmail.com>}
    @version:$Id$
'''

import sys
import urllib2
import chardet

def blog_detect(blogurl):
	'''
	detect the coding of blog
	@param blogurl: some url string
	'''
	try:
		fp = urllib2.urlopen(blogurl)							#尝试打开给定url
	except Exception, e:										#若产生异常，则给出相关提示并返回
		print e
		print 'download exception %s' % blogurl
		return 0
	blog = fp.read()											#读取内容
	codedetect = chardet.detect(blog)["encoding"]				#检测得到编码方式
	print '%s\t<-\t%s' % (blogurl, codedetect)
	fp.close()												#关闭
	return 1
    
if __name__ == "__main__":
	if len(sys.argv) == 1:
		print 'usage:\n\tpython cdays-1-exercise-1.py http://xxxx.com'
	else:
		blog_detect(sys.argv[1])
