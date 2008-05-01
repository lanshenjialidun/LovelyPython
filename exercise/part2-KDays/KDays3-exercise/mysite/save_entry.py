#!/bin/python
# coding:utf-8

#print QUERY
#获得文章id
id = int(QUERY['entry_id'])

#获得文章title, 若为空, 则出错, 转入出错链接
title = QUERY['entry_title'].strip()
if not title or not len(title):
    print "Please input entry's title"
    raise HTTP_REDIRECTION,"error"

#获得文章content, 若为空, 则出错, 转入出错链接
content = QUERY['entry_content']
if not content or not len(content):
    print "Please input entry's content"
    raise HTTP_REDIRECTION,"error"

#获得文章tag, 以空格为分割
tag = QUERY['entry_tag'].split()

#导入
import pickle
#自定义的文章类
from entry import Entry

#尝试load原有的文章列表对象, 若不存在则为空
try:
    entrylist = pickle.load(open("entry.dump"))
except Exception, e:
    entrylist = []

#id为0表示是新建的文章
if id == 0:
    newentry = Entry(len(entrylist)+1, title, tag, content)
    entrylist.append(newentry)
else:
    #print id
    #已存文章, 则对其修改, 注意因为列表是从0开始编号的, 而Entry的id是从1开始的, 所以这边需要调整id
    entrylist[id-1].title = title
    entrylist[id-1].tag = tag
    entrylist[id-1].content = content
    #for en in entrylist:
    #    if en.id == id:
    #        en.title = title
    #        en.tag = tag
    #        en.content = content

#保存更改后的新对象
pickle.dump(entrylist, open("entry.dump", "w"))

#最后页面跳转至首页
print 'Save Successfully'
raise HTTP_REDIRECTION,"index"