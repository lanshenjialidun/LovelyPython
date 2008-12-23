# $Id: obpKwd5.leo 325 2005-12-30 04:23:49Z  $
# qpage.py 快捷问卷模拟展示
#!/usr/bin/env python
# coding:utf-8

import time,shutil
import sys,os,string,re

#sys.path.append("../../karriweb/src/core")
#from agentweb import *
#from agentsys import *

from dict4ini import DictIni
from Karrigell_QuickForm import Karrigell_QuickForm

#初始化参数集中维护！
## 又一个，看来要重构！
qpath = "q/"
pubq = qpath+"easy051201.cfg"

cfgf = pubq

tcode = time.strftime("%y%m%d%H%M%S", time.localtime())
tcode = time.strftime("%y%m%d%H%M%S", time.localtime())

# 先复制一下子
#shutil.copy2(cfgf,cfgf+".%s"%tcode)
def qpublish(dict):
    """将dict 内容输出为回答问卷
    """
    exp = ""
    p = Karrigell_QuickForm('fm_kq','POST','#',dict.desc.desc)
    exp += "<h1>%s<sup>学习资料::%s</sup></h1>"%(dict.desc.pname
                                       ,dict.desc.learn)    

    #exp += "<H6>返回%s</H6>"%dict.desc.learn
    p.addElement('node','<ul>','')
    # 深入数据
    """
    p.addRadioList('cr_ask1'
                   ,"问题之一"
                   ,{'a':'Letter A'
                     ,'b':'Letter B'
                     ,'c':'Letter C'})
    """
    qli = {}
    k = [int(i) for i in dict.ask.keys()]
    k.sort()
    for i in k:
        ask = dict.ask[str(i)]
        qk = [j for j in ask.keys()]
        qk.sort()
        for q in qk:
            if 1==len(q):
                #exp +="<li>%s"%ask[q]
                qli[q] = ask[q]
            else:
                pass

        p.addRadioList("cr_ask%s"%i
                   ,ask["question"]
                   ,qli)
        p.addJSRule("cr_ask%s"%i,"问题%s "%i)

    p.addElement('node','</ul>','')

    # 无良的迁就……
    p.addJSValidation()
    p.saveJSRule("../js/validation-config.xml")

    p.addGroup(["submit","btn_submit","提交","btn"]
               ,["reset","btn_reset","重写","btn"])
    exp += p.export()

    return exp




#open(qpath+pubq,"w").write(QUERY["cfgfile"])
#print dir()
#print QUERY
qcfg = DictIni(cfgf)
print "<div id='qpage'>"
#print p.export()
print "<div id='errorDiv'></div>"

print qpublish(qcfg)
print "</div>"

"""
p = Karrigell_QuickForm('fm_kq','POST','#',qcfg.desc.pname)
p.addRadioList('cr_ask1'
               ,"问题之一"
               ,{'a':'Letter A'
                 ,'b':'Letter B'
                 ,'c':'Letter C'})

p.addGroup(["submit","btn_submit","提交"]
           ,["reset","btn_reset","重写"])
#p.display()
"""
