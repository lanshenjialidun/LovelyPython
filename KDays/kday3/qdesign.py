# $Id: obpKwd2.leo 325 2005-12-30 04:23:49Z  $
# qdesign.py 快捷问卷设计,,

#!/usr/bin/env python
# coding:utf-8

import time,datetime
import sys,os,string,re
from Cheetah.Template import Template as ctTpl


#sys.path.append("/usr/local/www/data/karriweb/src/plugin")
# /usr/local/www/data/warder/questionnaire
#from karriweb import *

#from agentweb import *
#from agentsys import *
from dict4ini import DictIni


#初始化参数集中维护！
qpath = "q/"
pubq = qpath+"easy051201.cfg"


page = open("questionnaire.tmpl","r").read()
vPool = {}
vPool['cfgtxt'] = open(pubq,"r").read()
txp = ctTpl(page, searchList=[vPool])
print txp

#print dir()
qcfg = DictIni(pubq)
#print len(qcfg)
#print qcfg.desc.learn
