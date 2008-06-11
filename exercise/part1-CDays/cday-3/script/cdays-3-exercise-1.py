# coding=utf-8
'''Lovely Python -3 PyDay 
    PyCDC v0.3
    @see：http://www.woodpecker.org.cn/diveintopython/scripts_and_streams/command_line_arguments.html 
'''
import os,sys
import getopt       #导入getopt模块

CDROM = '/media/cdrom0'
def cdWalker(cdrom,cdcfile):
    export = ""
    for root, dirs, files in os.walk(cdrom):
        export+="\n %s;%s;%s" % (root,dirs,files)
    open(cdcfile, 'w').write(export)

def usage():
    print '''PyCDC 使用方式:
    python cdays-3-exercise-1.py -d cdc -k 中国火
    #搜索 cdc 目录中的光盘信息，寻找有“中国火”字样的文件或是目录，在哪张光盘中
        '''

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hd:e:k:')
except getopt.GetoptError:
    usage()
    sys.exit()

if len(opts) == 0:
    usage()
    sys.exit()

c_path = ''
for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit()
    elif opt == '-e':
        #判别sys.argv[2]中是否有目录，以便进行自动创建
        #cdWalker(CDROM, arg)
        print "记录光盘信息到 %s" % arg
    elif opt == '-d':
        c_path = arg
    elif opt == '-k':
        if not c_path:
            usage()
            sys.exit()
        #进行文件搜索
