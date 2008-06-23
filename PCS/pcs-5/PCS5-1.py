#!/bin/python
# coding: utf-8

""" Html To Txt
@author: lizzie
@contract: shengyan1985@gmail.com
@see: ...
@version:0.1
"""
import os
from html2txt import *
import chardet
import sys

reload(sys)
sys.setdefaultencoding('utf8')

YAHOO_DIR = 'J:\\yahoo_data\\'
YAHOO_TXT = yahoo_dir + 'txt\\all.txt'

def html_to_txt():
    """将多个html文件合并为一个txt文件，统一编码为utf-8 or ascii
    """
    ft = open(YAHOO_TXT, 'w')
    start = 1
    while 1:
        filename = YAHOO_DIR+ str(start) + '.html'
        if os.path.isfile(filename):
            fp = open(filename, 'r')
            htmltxt = ''.join(fp.readlines())
            if not htmltxt or not len(htmltxt):
                continue
            fp.close()
            
            codedetect = chardet.detect(htmltxt)["encoding"]				#检测得到修改之前的编码方式
            print codedetect
	    if not codedetect in ['utf-8', 'ascii']:
	        htmltxt = unicode(htmltxt, codedetect).encode('utf-8')
	        codedetect = chardet.detect(htmltxt)["encoding"]			#检测得到修改之后的编码方式
                print 'change', codedetect
            
            ft.write(html2txt(htmltxt))
            print 'Success change html to txt %s' % start
            start += 1
        else:
            break
    ft.close()

if __name__ == '__main__':
    html_to_txt()