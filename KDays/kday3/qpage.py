# $Id: qpage.py 325 2005-12-30 04:23:49Z  $
# qpage.py 快捷问卷模拟展示

#!/usr/bin/env python
# coding:utf-8

import time,shutil
import sys,os,string,re

from dict4ini import DictIni
#初始化参数集中维护！
## 又一个，看来要重构！
qpath = "q/"
pubq = qpath+"easy051201.cfg"

cfgf = pubq

tcode = time.strftime("%y%m%d%H%M%S", time.localtime())

# 先复制一下子
shutil.copy2(cfgf,cfgf+".%s"%tcode)
def expage(dict):
    """将dict 内容输出为问卷
    """
    exp = ""
    exp += "<div id='qpage'>"
    exp += """<h3>%s —— 
        <sup>%s</sup>
        <sub>%s</sub></h3>"""%(dict.desc.pname
                                ,dict.desc.desc
                                ,dict.desc.learn)
    
    
    #print dict.ask["1"]
    exp +="<ul>"
    # 将字串的字典键值依照数字方式排序
    k = [int(i) for i in dict.ask.keys()]
    k.sort()
    for i in k:
        ask = dict.ask[str(i)]
        exp +="<li>%s"%ask["question"]
        exp +="<SUP>正确答案::%s</SUP>"%ask["key"]
        #unicode(str(dict.ask[i]["question"]), "utf8").encode("utf8")
        exp +="<ul>"
        qk = [j for j in ask.keys()]
        qk.sort()
        #name="animal[]"
        for q in qk:
            if 1==len(q):
                exp +="<li>%s"%ask[q]
            else:
                pass
        exp +="</ul>"
        exp +="</li>"
    exp +="</ul>"
    
    exp += "</div>" # id=qpage
    return exp
    
    
    
    
    
    
    

open(pubq,"w").write(QUERY["cfgfile"])
qcfg = DictIni(cfgf)
print expage(qcfg)
print "<hr/>"

# 测试...
#print dir()
#print QUERY["cfgfile"]
#print qcfg.desc
