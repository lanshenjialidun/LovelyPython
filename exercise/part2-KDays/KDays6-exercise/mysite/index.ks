# -*- coding: utf-8 -*-

import pickle
from Karrigell_QuickForm import Karrigell_QuickForm as KQF
from entry import Entry
from HTMLTags import *
from ConfigParser import RawConfigParser
import os

#使用 Session来记忆成员信息
sess = Session()
if not hasattr(sess, 'usr'):
    sess.usr = {'name':None, 'entry_path':'default_entry.dump'}

#尝试load原有的文章列表对象, 若不存在则为空
try:
    entrylist = pickle.load(open(sess.usr["entry_path"]))
except Exception, e:
    entrylist = list()

def print_head(type='Entry'):
    #页面首部
    print '''
    <head>
        <title>Mysite</title>
    </head>
    <body>
        <h1>%s</h1>
    ''' % type
    
    ##########
    #print H1(type)
    
def print_foot():
    #页面底部
    print '''
    </body>
    '''

def error(errmsg='ERROR'):
    '''显示错误
    '''
    print_head(errmsg)
    print '<a href= "http://localhost:8081/mysite/">Return</a>'
    
    ##########
    #print SPAN(A('Return', href="http://localhost:8081/mysite/"), id='return')
    
    print_foot()
    
def index(**args):
    '''显示首页
    '''
    #首先判断是否已经登录, 若未登录, 转入登录页面
    if not sess.usr['name']:
        raise HTTP_REDIRECTION,"login"
    
    #输出头部
    print_head()
    
    print 'login : ', sess.usr['name']
    print '|'
    print '<a href="logout">logout</a>'
    
    ##########
    #print SPAN(A('logout', href="logout"),id="logout")
    
    print '|'
    ##########
    print SPAN(A('New', href="edit"),id="edit") 
    
    print '|'
    ##########
    print SPAN(A('Search', href="search"),id="search") 
    
    #依次输出各个文章
    entrylist.reverse()
    for e in entrylist:
        print '<h3>%s</h3><p>Title: %s</p><p>Tags: %s</p><p>%s</p>' % (e.id, e.title, ' '.join(e.tag), e.content)
        print '<a href="edit?id=%s">Edit</a>' % e.id
        print '|'
        print '<a href="delete?id=%s">Delete</a>' % e.id
        print '<hr/>'
        
        ##########
        #print H3(e.id)
        #print H4('Title: %s' % e.title)
        #print '<p>Tags: %s</p><p>%s</p>' % (' '.join(e.tag), e.content)
        #print '<a href="edit?id=%s">Edit</a>' % e.id
        #print '<hr/>'

    #输出页面尾部
    print_foot()

def search(**args):
    '''搜索功能
    '''
    print_head('Search')
    if not len(QUERY):
        #增加搜索框
        s = KQF('fm_search','POST',"search", '')
        s.addHtmNode('text','keywords','KeyWords',{'size':20, 'maxlength':'40', "value":""})
        s.addElement("submit", 'submit', {'value':"submit"})
        s.display()
    else:
        #获取keywords, 若为空, 则跳转到之前搜索页面
        keywords = QUERY['keywords'].strip()
        if not len(keywords):
            raise HTTP_REDIRECTION,"search"
        
        print H4('Result-->')
        #依次遍历所有entry, 查找符合条件的entry并输出
        for e in entrylist:
            if e.has_keywords(keywords):
                print '<h4>%s</h4><p>Title: %s</p><p>Tags: %s</p><p>%s</p>' % (e.id, e.title, ' '.join(e.tag), e.content)
                print '<hr/>'
    
    print SPAN(A('Next Search', href="search"), id="search") 
    print SPAN(A('Return', href="index"), id="index") 
    print_foot()
    
def save(**args):
    '''保存修改
    '''
    #获得文章id
    id = int(QUERY['entry_id'])

    #获得文章title, 若为空, 则出错, 转入出错链接
    title = QUERY['entry_title'].strip()
    if not title or not len(title):
        raise HTTP_REDIRECTION,"error?errmsg=%s" % 'Title is Empty'

    #获得文章content, 若为空, 则出错, 转入出错链接
    content = QUERY['entry_content']
    if not content or not len(content):
        raise HTTP_REDIRECTION,"error?errmsg=%s" % 'Content is Empty'

    #获得文章tag, 以空格为分割
    tag = QUERY['entry_tag'].split()

    #id为0表示是新建的文章
    if id == 0:
        newentry = Entry(len(entrylist)+1, title, tag, content)
        entrylist.append(newentry)
    else:
        #已存文章, 则对其修改, 注意因为列表是从0开始编号的, 而Entry的id是从1开始的, 所以这边需要调整id
        entrylist[id-1].title = title
        entrylist[id-1].tag = tag
        entrylist[id-1].content = content
    #保存更改后的新对象
    pickle.dump(entrylist, open(sess.usr["entry_path"], "w"))

    #最后页面跳转至首页
    raise HTTP_REDIRECTION,"index"

def delete(id=0):
    '''删除某个文章
    '''
    id = int(id)-1
    #验证id
    if id < 0 or id >= len(entrylist):
        raise HTTP_REDIRECTION,"error?errmsg=%s" % 'Delete Id Error'
    
    #调整删除项后面项的id, 依次减1
    for dentry in entrylist[id+1:]:
        dentry.id -= 1
    #删除第id个文章
    del entrylist[id]
    #保存更改后的新对象
    pickle.dump(entrylist, open(sess.usr["entry_path"], "w"))
    #最后页面跳转至首页
    raise HTTP_REDIRECTION,"index"
    
def edit(id=0):
    '''编辑
    '''
    print_head('Edit')
    
    #初始化, 新建文章id为0, 已存文章为非0
    entry_title = ''
    entry_content = ''
    entry_tag = ''
    entry_id = 0
    if id:
        #获取已存文章id, 应该减1
        id = int(id)-1
        #获取对应id的文章
        try:
            entry_title = entrylist[id].title
            entry_content = entrylist[id].content
            entry_tag = ' '.join(entrylist[id].tag)
            entry_id = entrylist[id].id
        except:
            raise HTTP_REDIRECTION,"error?errmsg=%s" % 'Get Entry Error'
        
    #使用Karrigell_QuickForm修改
    p = KQF('fm_edit','POST',"save", '')
    p.addHtmNode('text','entry_title','Title',{'size':20, 'maxlength':'40', "value":"%s" % entry_title})
    p.addHtmNode('text','entry_tag','Tags',{'size':20, 'maxlength':'40', "value":"%s" % entry_tag})
    p.addCntTextArea('entry_content', 'Content', '%s' % entry_content, '20','50')
    p.addElement("reset", 'reset', {'value':"Reset"})
    p.addGroup(["submit","btn_submit","Submit","btn"])
    p.addElement("hidden", "entry_id", {"value":"%s" % entry_id})
    p.display()
    
    print_foot()

def login():
    """登录页面
    """
    print_head("Login") 
    string = '''
    <form action="chkusr" method="post">
        <table>
            <tr>
                <td>Name</td><td><input name="name" value=""></td>
            </tr>
            <tr>
                <td>Password</td><td><input name="passwd" type="password" value=""></td>
            </tr>
            <tr>
                <td><input type="submit" value="Ok"></td><td>&nbsp;</td>
            </tr>
        </table>
    </form>
    '''
    print string
    print_foot()

def chkusr(**args):
    """从login 自然引发的页面
        检查用户登录情况
    """
    #先判断user_info.txt是否存在, 不存在则新建一个空文件
    if not os.path.isfile('user_info.txt'):
            open('user_info.txt', 'w').close()
    
    cfg = RawConfigParser()
    try:
        user_file = open('user_info.txt', 'r')

        cfg.readfp(user_file)
        #先检测user_info.txt中是否已经存在此用户信息, 有则把该用户的数据路径加入session中, 若不存在, 还要保存该用户信息, 并新建该用户数据文件
        username = QUERY["name"]
        userpath = ''
        if cfg.has_section(username):
            userpath = cfg.get(username, 'path')
            #可能还有用户其他信息
        else:
            #增加新用户信息
            cfg.add_section(username)
            #新的用户数据路径
            if not os.path.isdir('data'):
                os.mkdir('data')
            userpath = os.getcwd()+os.sep+ 'data'+os.sep+username+'_entry.txt'
            cfg.set(username, 'path', userpath)
            cfg.write(open('user_info.txt', 'w'))

        #加入会话中
        sess.usr["name"] = username
        sess.usr["entry_path"] = userpath

    except Exception, e:
        raise HTTP_REDIRECTION,"error?errmsg=11%s" % e

    raise HTTP_REDIRECTION,"index"

def logout():
    """登出
    """
    sess.close()    
    raise HTTP_REDIRECTION,"index"
