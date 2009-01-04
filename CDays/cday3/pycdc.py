# -*- coding: utf-8 -*-
''''pycdc.py' is part of PyCDC.
    @author: U{Zoom.Quiet<mailto:Zoom.Quiet@gmail.com>}
    @license:GPL v3 U{http://www.gnu.org/licenses/}
    @version:0.7
    @note: 作为主响应交互环境使用cmd 模块实现
    @todo: 进一步美化交互提示
'''
import sys, cmd
from cdctools import *

class PyCDC(cmd.Cmd):
    '''PyCDC 主程序
    @author: U{Zoom.Quiet<mailto:Zoom.Quiet@gmail.com>}
    @todo: 更加丰富的表现？
    '''
    def __init__(self):
        '''class PyCDC 初始化函式
        - 设定默认光盘位置
        - 设定命令交互提示字串
        - 设定使用说明
        '''
        cmd.Cmd.__init__(self)                # initialize the base class
        self.CDROM = '/media/cdrom0'
        self.CDDIR = 'cdc/'
        self.prompt="(PyCDC)>"
        self.intro = '''PyCDC0.5 使用说明:
    dir 目录名     #指定保存和搜索目录，默认是 "cdc"
    walk 文件名    #指定光盘信息文件名，使用 "*.cdc"
    find 关键词    #遍历搜索目录中所有.cdc文件，输出含有关键词的行
    ?           # 查询
    EOF         # 退出系统，也可以使用Crtl+D(Unix)|Ctrl+Z(Dos/Windows)
        '''

    def help_EOF(self):
        '''PyCDC 退出帮助信息输出函式
        '''
        print "退出程序 Quits the program"
    def do_EOF(self, line):
        '''PyCDC 退出执行函式
        '''
        sys.exit()

    def help_walk(self):
        '''PyCDC 扫描光盘帮助信息输出函式
        '''
        print "扫描光盘内容 walk cd and export into *.cdc"
    def do_walk(self, filename):
        '''PyCDC 扫描光盘执行函式
        '''
        if filename == "":filename = raw_input("输入cdc文件名:: ")
        print "扫描光盘内容保存到:'%s'" % filename
        iniCDinfo(self.CDROM,"%s/%s"%(self.CDDIR,filename))
        #cdWalker(self.CDROM,"%s/%s"%(self.CDDIR,filename))

    def help_dir(self):
        '''PyCDC 指定目录执行函式
        '''
        print "指定保存/搜索目录"
    def do_dir(self, pathname):
        '''PyCDC 指定目录帮助信息输出函式
        '''
        if pathname == "": pathname = raw_input("输入指定保存/搜索目录: ")
        self.CDDIR = pathname
        print "指定保存/搜索目录:'%s' ;默认是:'%s'" % (pathname,self.CDDIR)

    def help_find(self):
        '''PyCDC 关键词搜索执行函式
        '''
        print "搜索关键词"
    def do_find(self, keyword):
        '''PyCDC 关键词搜索帮助信息输出函式
        '''
        if keyword == "": keyword = raw_input("输入搜索关键字: ")
        print "搜索关键词:'%s'" % keyword
        cdcGrep(self.CDDIR,keyword)

if __name__ == '__main__':      # this way the module can be
    '''PyCDC 自测,及调用主响应处理
    '''
    cdc = PyCDC()            # imported by other programs as well
    cdc.cmdloop()


