#!/bin/python
# coding:utf-8

#获得文章id
id = QUERY['entry_id']

#获得文章title, 若为空, 则出错, 转入出错链接
title = QUERY['entry_title'].strip()
if not title or not len(title):
    print "Please input entry's title"
    raise HTTP_REDIRECTION,"error1"

#获得文章content, 若为空, 则出错, 转入出错链接
content = QUERY['entry_content']
if not content or not len(content):
    print "Please input entry's content"
    raise HTTP_REDIRECTION,"error2"

#导入RawConfigParser模块
from ConfigParser import RawConfigParser
cfg = RawConfigParser()

#尝试打开文件, 同样, 该文件实现需存在
try:
    entry_file = open('entry.txt', 'r')
    cfg.readfp(entry_file)
    entry_file.close()
except Exception, e:
    print e
    raise HTTP_REDIRECTION,"error"

#id为0表示是新建的文章, 需增加一个section, 若不为0, 则表示修改已存在的文章
if id == '0':
    this_entry_id = str(len(cfg.sections()) +1)
    cfg.add_section("%s" % this_entry_id )
else:
    this_entry_id = id
cfg.set("%s" % this_entry_id, 'Entry Title', title)
cfg.set("%s" % this_entry_id, 'Entry Content', content)
cfg.write(open('entry.txt', 'w'))

#最后页面跳转至首页
print 'Save Successfully'
raise HTTP_REDIRECTION,"index"



