# -*- coding: utf-8 -*-
''''cdctools.py' is part of PyCDC.
    @author: U{Zoom.Quiet<mailto:Zoom.Quiet@gmail.com>}
    @license:GPL v3 U{http://www.gnu.org/licenses/}
    @version:0.9
    @note: 作为主程序调用的常用处理函式集合,没有类定义
    @todo: 更加智能的中文编码判定或是提示
'''
import os                                       # 导入操作系统支持模块
from ConfigParser import RawConfigParser as rcp  # 导入基础配置处理机为 rcp
import time                                     # 导入时间处理支持模块
from threading import Thread                    # 导入线程支持模块

def iniCDinfo(cdrom,cdcfile):
    '''光盘信息.ini格式化函式
    @note: 直接利用 os.walk() 函式的输出信息由ConfigParser.RawConfigParser进行重组处理成 .ini 格式文本输出并记录
    @param cdrom: 光盘访问路径
    @param cdcfile: 输出的光盘信息记录文件(包含路径,绝对,相对都可以)
    @return: 无,直接输出成组织好的类.ini 的*.cdc 文件
    '''
    walker = {}
    for root, dirs, files in os.walk(cdrom):
        walker[root]=(dirs,files)
    cfg = rcp()
    cfg.add_section("Info")
    cfg.add_section("Comment")
    cfg.set("Info", 'ImagePath', cdrom)
    cfg.set("Info", 'Volume', cdcfile)
    cfg.set("Info", 'FAT', 'CDFS')
    dirs = walker.keys()
    i = 0
    for d in dirs:
        i+=1
        cfg.set("Comment", str(i),d)
        
    for p in walker:
        cfg.add_section(p)
        for f in walker[p][1]:
            cfg.set(p, f, os.stat("%s/%s"%(p,f)).st_size)    
    cfg.write(open(cdcfile,"w"))
    
def cdWalker(cdrom,cdcfile):
    '''光盘扫描主函式
    @param cdrom: 光盘访问路径
    @param cdcfile: 输出的光盘信息记录文件(包含路径,绝对,相对都可以)
    @return: 无,直接输出成*.cdc 文件
    @attention: 从v0.7 开始不使用此扫描函式,使用 iniCDinfo()
    '''
    export = ""
    for root, dirs, files in os.walk(cdrom):
        print formatCDinfo(root,dirs,files)
        export+= formatCDinfo(root,dirs,files)
    open(cdcfile, 'w').write(export)

def formatCDinfo(root,dirs,files):
    '''光盘信息记录格式化函式
    @note: 直接利用 os.walk() 函式的输出信息进行重组
    @param root: 当前根
    @param dirs: 当前根中的所有目录
    @param files: 当前根中的所有文件
    @return: 字串,组织好的当前目录信息
    '''
    export = "\n"+root+"\n"
    for d in dirs:
        export+= "-d "+root+_smartcode(d)+"\n"
    for f in files:
        export+= "-f %s %s \n" % (root,_smartcode(f))
    export+= "="*70
    return export

import chardet
def _smartcode(ustring):
    '''智能字串编码转换函式
    @note: 利用chardet.detect() 猜测字串的编码值,然后统一转换为utf8
    @param ustring: 有正确编码的中文字串
    @todo: 更加精确的猜测处理
    '''
    codename = chardet.detect(ustring)["encoding"]
    print codename
    try:
        print ustring
        ustring = unicode(ustring, codename)
        print ustring
        return "%s %s"%("",ustring.encode('utf8'))
    except:
        return u"bad unicode encode try!"

def cdcGrep(cdcpath,keyword):
    '''光盘信息文本关键词搜索函式
    @note: 使用最简单的内置字串匹配处理来判定是否有关键词包含
    @param cdcpath: 包含*.cdc 文件的目录
    @param keyword: 搜索的关键词
    @todo: 可结合搜索引擎进行模糊搜索!
    '''
    filelist = os.listdir(cdcpath)          # 搜索目录中的文件
    for cdc in filelist:                    # 循环文件列表
        if ".cdc" in cdc:
            cdcfile = open(cdcpath+cdc)         # 拼合文件路径，并打开文件
            for line in cdcfile.readlines():    # 读取文件每一行，并循环
                if keyword in line:             # 判定是否有关键词在行中
                    print line                  # 打印输出

class grepIt(Thread):
    '''继承自threading.Thread 的线程对象类
    '''
    def __init__ (self,cdcfile,keyword):
        '''类初始化函式:
        @param cdcfile: *.cdc文件名，含路径
        @param keyword: 搜索关键词，应该是utf-8 编码
        '''
        Thread.__init__(self)
        self.cdcf = cdcfile
        self.keyw = keyword.upper()
        self.report = ""
    def run(self):
        '''线程行为声明函式:
        @note: 各个线程的实际动作的定义
        '''
        if ".cdc" in self.cdcf:
            self.report = markIni(self.cdcf,self.keyw)
            #self.report = markLine(self.cdcf,self.keyw)
        '''重构前的当地匹配处置::
            for line in open(self.cdcf).readlines():    # 打开文件,读取文件每一行，并循环
                if self.keyw in line.upper():             # 判定是否有关键词在行中
                    #print line                  # 打印输出
                    self.report += line
        '''
        
def markLine(cdcfile,keyword):
    '''搜索匹配函式:
    @param cdcfile: *.cdc文件名，含路径
    @param keyword: 搜索关键词，应该是utf-8 编码
    @return:将所有匹配的行组织成 report 返回
    @note: 粗略的在摘要文件行中匹配，并直接输出该行;为了E文的通用匹配，预先将关键词和行文字都变成大写的
    '''
    report = ""
    for line in open(cdcfile).readlines():    # 打开文件,读取文件每一行，并循环
        if keyword in line.upper():             # 判定是否有关键词在行中
            report += line
    return report

def markIni(cdcfile,keyword):
    '''配置文件模式匹配函式:
    @param cdcfile: *.cdc文件名，含路径
    @param keyword: 搜索关键词，应该是utf-8 编码
    @return:将所有匹配的行组织成 report 返回
    @note: 将文件解析成配置对象树,然后进行匹配;为了E文的通用匹配，预先将关键词和行文字都变成大写的:
        - 如果在目录名上有匹配就记录目录,并停止挖掘
        - 如果在文件名上有匹配,则前缀目录名记录
    '''
    report = ""
    keyw = keyword.upper()
    cfg = rcp()
    cfg.read(cdcfile)
    nodelist = cfg.sections()
    nodelist.remove("Comment")
    nodelist.remove("Info")
    
    for node in nodelist:
        #print type(node)
        if keyw in node.upper():
            report += node
            continue
        else:
            for item in cfg.items(node):
                #print item[0].upper()
                if keyw in item[0].upper():
                    report += "%s/%s"%(node,item)
    #print keyw
    return report
    
def grpSearch(cdcpath,keyword):
    '''多线程群体搜索函式:
        @param cdcpath: *.cdc文件所在 路径
        @param keyword: 搜索关键词，应该是utf-8 编码
    '''
    print time.ctime()
    filelist = os.listdir(cdcpath)          # 搜索目录中的文件
    searchlist = []                         # 记录发起的搜索编程
    for cdcf in filelist:
        pathcdcf = "%s/%s"%(cdcpath,cdcf)
        current = grepIt(pathcdcf,keyword)  # 初始化线程对象
        searchlist.append(current)          # 追加记录线程队列
        current.start()                     # 发动线程处理
    for searcher in searchlist:
        searcher.join()
        print "Search from ",searcher.cdcf," out ",searcher.report     
    print time.ctime()

if __name__ == '__main__':      # this way the module can be
    '''cdctools 自测响应处理
    '''
    CDROM = '/media/cdrom0'
    #iniCDinfo(CDROM,"cdctools-utf8-beautify.cdc")
    #cdWalker(CDROM,"cdctools-utf8-beautify.cdc")
    #cdcGrep("cdc/","EVA")
    grpSearch("cdc/","忆莲")
    #markLine("cdc/z.MFC.pop.02.cdc","忆莲")
    #markIni("cdc/z.MFC.pop.02.cdc","忆莲")

'''
自动时: /dev/scd0 /media/cdrom0 iso9660 ro,noexec,nosuid,nodev,user=zoomq 0 0
GBK$ sudo mount -o ro,norock,iocharset=cp936 /dev/scd0 /media/cdrom0
UTF8$ sudo mount -o ro,norock,iocharset=utf8 /dev/scd0 /media/cdrom0
'''
