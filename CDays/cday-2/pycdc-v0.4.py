# coding : utf-8
'''pycdc-v0.4.py
Lovely Python -2 PyDay 
'''
import sys, cmd
class PyCDC(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)                # initialize the base class
        self.CDROM = '/media/cdrom0'
        self.CDDIR = 'cdc/'

    def help_EOF(self):
        print "退出程序 Quits the program"
    def do_EOF(self, line):
        sys.exit()

    def help_walk(self):
        print "扫描光盘内容 walk cd and export into *.cdc"
    def do_walk(self, filename):
        if filename == "":filename = raw_input("输入cdc文件名:: ")
        print "扫描光盘内容保存到:'%s'" % filename

    def help_dir(self):
        print "指定保存/搜索目录"
    def do_dir(self, pathname):
        if pathname == "": pathname = raw_input("输入指定保存/搜索目录: ")
        print "指定保存/搜索目录:'%s' ;默认是:'%s'" % (pathname,self.CDDIR)

    def help_find(self):
        print "搜索关键词"
    def do_find(self, keyword):
        if keyword == "": keyword = raw_input("输入搜索关键字: ")
        print "搜索关键词:'%s'" % keyword

if __name__ == '__main__':      # this way the module can be
    cdc = PyCDC()            # imported by other programs as well
    cdc.cmdloop()


