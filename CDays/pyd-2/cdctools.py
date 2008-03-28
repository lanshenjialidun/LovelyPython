# coding : utf-8
''''cdctools.py'
Lovely Python -2 PyDay 
'''
import os
def cdWalker(cdrom,cdcfile):
    export = ""
    for root, dirs, files in os.walk(cdrom):
        export+="\n %s;%s;%s" % (root,dirs,files)
    open(cdcfile, 'w').write(export)

def cdcGrep(cdcpath,keyword):
    filelist = os.listdir(cdcpath)          # 搜索目录中的文件
    for cdc in filelist:                    # 循环文件列表
        cdcfile = open(cdcpath+cdc)         # 拼合文件路径，并打开文件
        for line in cdcfile.readlines():    # 读取文件每一行，并循环
            if keyword in line:             # 判定是否有关键词在行中
                print line                  # 打印输出

if __name__ == '__main__':      # this way the module can be
    CDROM = '/media/cdrom0'
    #cdWalker(CDROM,"cdc/cdctools.cdc")
    cdcGrep("cdc/","EVA")
