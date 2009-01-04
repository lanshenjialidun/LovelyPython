# -*- coding: utf-8 -*-
''''pycdc.py' is part of PyCDC.

    PyCDC is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    PyCDC is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
        cdWalker(self.CDROM,self.CDDIR+filename)

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


