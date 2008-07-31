def iniCDinfo(cdrom,cdcfile):
    '''光盘信息.ini格式化函式
    @note: 直接利用 os.walk() 函式的输出信息由ConfigParser.RawConfigParser进行重组处理成 .ini 格式文本输出并记录
    @param cdrom: 光盘访问路径
    @param cdcfile: 输出的光盘信息记录文件(包含路径,绝对,相对都可以)
    @return: 无,直接输出成组织好的类.ini 的*.cdc 文件
    '''
    walker = {}
    for root, dirs, files in os.walk(cdrom):
        walker[root]=(dirs,files)          # 使用字典保存目录结构信息，以根目录作为key，对应子目录及文件作为value，以便下面的cfg组织信息

    cfg = rcp()
    cfg.add_section("Info")
    cfg.add_section("Comment")
    cfg.set("Info", 'ImagePath', cdrom)
    cfg.set("Info", 'Volume', cdcfile)
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


