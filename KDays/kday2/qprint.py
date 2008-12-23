# qpage.py 快捷问卷模拟展示;

#!/usr/bin/env python
# coding:utf-8

import time,shutil
import sys,os,string,re

#sys.path.append("../../karriweb/src/core")
#from agentweb import *
#from agentsys import *

from dict4ini import DictIni
from Karrigell_QuickForm import Karrigell_QuickForm

## 元模板对象 使用 Cheetah 系统
#t = MetaTpl()
#t.actAs("Cheetah")
qpath = "q/"
pubq = "scmatrixQ41109.cfg"
#tryq = "scmatrixQ4%s.cfg"
cfgf = qpath+pubq

#m_CFG = "不是合法的问卷配置文件！！别玩了！"
tcode = time.strftime("%y%m%d%H%M%S", time.localtime())

# 先复制一下子
#shutil.copy2(cfgf,cfgf+".%s"%tcode)
def qpublish(dict):
    """将dict 内容输出为回答问卷
    """
    exp = ""
    p = Karrigell_QuickForm('fm_kq','POST','#',dict.desc.desc)
    exp += "<h1>%s<sup>%s</sup></h1>"%(dict.desc.pname
                                       ,dict.desc.learn)    

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


    p.addElement('node','</ul>','')

    p.addGroup(["submit","btn_submit","提交"]
               ,["reset","btn_reset","重写"])
    exp += p.export()
    exp += "<p>返回%s</p>"%dict.desc.learn
    return exp






#open(qpath+pubq,"w").write(QUERY["cfgfile"])
#print dir()
#print QUERY["cfgfile"]
#p.addRule('cr_ask1','required','问题? is required!')
#p.addElement('text','telephone',{'size':100,'maxlength':40})
#p.addRule('telephone','required','telephone is required!')
#p.addCheckBox('fuda',{'a':'Letra A','b':'Letra B'})
print QUERY
qcfg = DictIni(cfgf)
print "<div id='qpage'>"
#print p.export()
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
