# -*- coding: utf-8 -*-
''''cdctools.py'
Lovely Python -1 PyDay 
自动时: /dev/scd0 /media/cdrom0 iso9660 ro,noexec,nosuid,nodev,user=zoomq 0 0
GBK$ sudo mount -o ro,norock,iocharset=cp936 /dev/scd0 /media/cdrom0
UTF8$ sudo mount -o ro,norock,iocharset=utf8 /dev/scd0 /media/cdrom0
'''
import os

def cdWalker(cdrom,cdcfile):
    export = ""
    for root, dirs, files in os.walk(cdrom):
        #export+="\n %s;%s;%s" % (root,dirs,files)
        #export+=_smartcode("\n %s;%s;%s" % (root,"+d"+"\n ".join(["%s"%d for d in dirs]),files))
        print formatCDinfo(root,dirs,files)
        export+= formatCDinfo(root,dirs,files)
        #print "\n %s;%s;%s" % (root,dirs,files)
        #print unicode(root, 'gb2312').encode('utf8')
    open(cdcfile, 'w').write(export)

def formatCDinfo(root,dirs,files):
    export = "\n"+root+"\n"
    for d in dirs:
        export+= "-d "+root+_smartcode(d)+"\n"
    for f in files:
        export+= "-f %s %s \n" % (root,_smartcode(f))
    export+= "="*70
    return export

def cdcGrep(cdcpath,keyword):
    filelist = os.listdir(cdcpath)          # 搜索目录中的文件
    for cdc in filelist:                    # 循环文件列表
        if ".cdc" in cdc:
            cdcfile = open(cdcpath+cdc)         # 拼合文件路径，并打开文件
            for line in cdcfile.readlines():    # 读取文件每一行，并循环
                if keyword in line:             # 判定是否有关键词在行中
                    print line                  # 打印输出

import chardet
def _smartcode(stream):
    """smart recove stream into UTF-8
    """
    ustring = stream
    codedetect = chardet.detect(ustring)["encoding"]
    print codedetect
    try:
        print ustring
        ustring = unicode(ustring, codedetect)
        print ustring
        return "%s %s"%("",ustring.encode('utf8'))
    except:
        return u"bad unicode encode try!"

if __name__ == '__main__':      # this way the module can be
    CDROM = '/media/cdrom0'
    cdWalker(CDROM,"cdctools-utf8-beautify.cdc")
    #cdcGrep("cdc/","EVA")

'''无法截取错误处理?!
...
GB2312
���¾��� ����.htm
Traceback (most recent call last):
  File "cdctools.py", line 101, in ?
    cdWalker(CDROM,"cdctools.cdc")
  File "cdctools.py", line 13, in cdWalker
    print formatCDinfo(root,dirs,files)
  File "cdctools.py", line 26, in formatCDinfo
    export+= "-f %s \n" % _smartcode(f)
UnicodeDecodeError: 'ascii' codec can't decode byte 0xd3 in position 14: ordinal not in range(128)


#try scan code
try:
    ustring = unicode(ustring, 'gbk')
except UnicodeDecodeError:
    try:
        ustring = unicode(ustring, 'big5')
    except UnicodeDecodeError:
        try:
            ustring = unicode(ustring, 'shift_jis')
        except UnicodeDecodeError:
            try:
                ustring = unicode(ustring, 'iso2022_kr')
            except UnicodeDecodeError:
                try:
                    ustring = unicode(ustring, 'ascii')
                except:
                    #print " [unknow decode[["+ustring                    
                    print LI(" [unknow decode[["+ustring)
                    print LI(chardet.detect(ustring)["encoding"])
                    return u"bad unicode encode!"

tryuni = ("gbk"
        ,"gb2312"
        ,"gb18030"
        ,"big5"
        ,"shift_jis"
        ,"iso2022_kr"
        ,"iso2022_jp"
        ,"ascii")

try:
    for type in tryuni:
        try:
            ustring = unicode("%s}"%type+ustring, type)
            #try decode by list
        except:            
            continue
            #break
            #continue try decode guess
except:
    return u"bad unicode encode!"
'''

