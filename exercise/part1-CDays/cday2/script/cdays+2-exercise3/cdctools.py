# -*- coding: utf-8 -*-
''''cdctools.py' is part of PyCDC.
    @author: U{Zoom.Quiet<mailto:Zoom.Quiet@gmail.com>}
    @license:GPL v3 U{http://www.gnu.org/licenses/}
    @version:0.7.1
    @note: 配合Karrigell 的版本，作为主程序调用的常用处理函式集合,没有类定义
    @todo: 更加智能的中文编码判定或是提示
'''
import os
from ConfigParser import RawConfigParser as rcp
import pickle

def iniCDinfo(cdrom,cdcfile):
    '''光盘信息.ini格式化函式
    @note: 直接利用 os.walk() 函式的输出信息由ConfigParser.RawConfigParser进行重组处理成 .ini 格式文本输出并记录
    @param cdrom: 光盘访问路径
    @param cdcfile: 输出的光盘信息记录文件(包含路径,绝对,相对都可以)
    @return: 无,直接输出成组织好的类.ini 的*.cdc 文件
    '''
    walker = {}
    for root, dirs, files in os.walk(cdrom):
        walker[root]=(dirs,files)          # 这里是个需要理解的地方
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

HISTORY_SEARCH = './history_search.dump'
def cdcGrep(cdcpath,keyword):
    '''光盘信息文本关键词搜索函式
    @note: 使用最简单的内置字串匹配处理来判定是否有关键词包含
    @param cdcpath: 包含*.cdc 文件的目录;运行前得在 __main__ 中修订成你当前的 cdc 数据存放点
    @param keyword: 搜索的关键词
    @return: 组织匹配好的信息到字典中导出成 searched.dump 文件
    @todo: 可结合搜索引擎进行模糊搜索!
    '''
    expDict = {}
    print cdcpath
    try:
        h_search = pickle.load(open(HISTORY_SEARCH))
        
        if h_search.has_key(keyword):  # 如果已有该关键字，则直接使用历史记录中的，导出格式不变。
            for (c, l) in h_search[keyword]:
                if expDict.has_key(c):
                    expDict[c].append(l)
                else:
                    expDict[c] = [l]
            pickle.dump(expDict,open("searched.dump","w"))
            return
    except:
        h_search = {}
    
    filelist = os.listdir(cdcpath)          # 搜索目录中的文件
    for cdc in filelist:                    # 循环文件列表
        if ".cdc" in cdc:
            cdcfile = open(cdcpath+cdc)         # 拼合文件路径，并打开文件
            expDict[cdc]=[]
            for line in cdcfile.readlines():    # 读取文件每一行，并循环
                if keyword in line:             # 判定是否有关键词在行中
                    #print line                  # 打印输出
                    expDict[cdc].append(line)
                    if h_search.has_key(keyword):  # 保存keyword对应的结果，格式为{keyword:[(cdc, line)]}
                        h_search[keyword].append((cdc, line))
                    else:
                        h_search[keyword] = [(cdc, line)]
    #print expDict
    pickle.dump(expDict,open("searched.dump","w"))
    pickle.dump(h_search, open(HISTORY_SEARCH, 'w'))
    
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

if __name__ == '__main__':      # this way the module can be
    '''cdctools 自测响应处理
    '''
    CDROM = '/media/cdrom0'
    CDCPATH = "/home/shengyan/obp/Karrigell-2.3.5/webapps/cdc/cdc/"   # 测试时需修改该路径
    ## 以上目录要在运行时,修订成你当前的 cdc 数据存放点
    ##"/home/zoomq/workspace/obp/trunk/LovelyPython/PyDays/pyd+2/cdc/"
    #iniCDinfo(CDROM,"cdctools-utf8-beautify.cdc")
    #cdWalker(CDROM,"cdctools-utf8-beautify.cdc")
    cdcGrep(CDCPATH,"EVA")
    print pickle.load(open("searched.dump"))

'''
自动时: /dev/scd0 /media/cdrom0 iso9660 ro,noexec,nosuid,nodev,user=zoomq 0 0
GBK$ sudo mount -o ro,norock,iocharset=cp936 /dev/scd0 /media/cdrom0
UTF8$ sudo mount -o ro,norock,iocharset=utf8 /dev/scd0 /media/cdrom0
'''
