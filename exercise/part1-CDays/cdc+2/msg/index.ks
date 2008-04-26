# -*- coding: utf-8 -*-

import os,sys
import pickle   # 神奇的序列化模块
from HTMLTags import * # Karrigell 提供页面输出支持模块
from Karrigell_QuickForm import Karrigell_QuickForm as KQF

def _htmhead(title):
    '''默认页面头声明
    @note: 为了复用，特别的组织成独立函式,根据Karrigell 非页面访问约定，函式名称前加"_"
    @param title: 页面标题信息
    @return: 标准的HTML代码
    '''
    htm = """<html><HEAD>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
<title>%s</title></HEAD>
<body>"""%title
    return htm
## 默认页面尾声明
htmfoot="""
<h5>design by:<a href="mailto:shengyan1985@gmail.com">lizzie</a>
    powered by : <a href="http://python.org">Python</a> +
 <a href="http://karrigell.sourceforge.net"> KARRIGELL 2.4.0</a>
</h5>
</body></html>"""

def index(**args):
    '''默认主
    @note: 使用简单的表单／链接操作来完成原有功能的界面化
    @param args: 数组化的不定参数
    @return: 标准的HTML页面
    '''
    print _htmhead("Leave Messages")
    p = KQF('fm_message','POST',"index","Message")
    p.addHtmNode('text','yname','Name',{'size':20,'maxlength':20})
    p.addTextArea('Words','10','90')
    p.addGroup(["submit","btn_submit","Submit","btn"])
    p.display()
    
    if 0 == len(QUERY):
        pass
    else:
        if "Submit" in QUERY['btn_submit']:
            yname = QUERY['yname']
            ywords = QUERY['Words']
            if 0 == len(ywords):
                print H3("please say something!")
            else:
                if 0 == len(yname):
                    yname = 'somebody'
                try:
                    msg = pickle.load(open("message.dump"))
                except:
                    msg = []
                msg.append((yname, ywords))
                index = len(msg)-1
                while index >= 0:
                    print H5(msg[index][0]+' says: ')
                    print P('------ '+msg[index][1])
                    index -= 1
                pickle.dump(msg,open("message.dump","w"))
        else:
            pass
    print htmfoot


