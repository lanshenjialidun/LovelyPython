<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet ekr_stylesheet?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="799" clone_windows="0"/>
<globals body_outline_ratio="0.216796875">
	<global_window_position top="10" left="10" height="698" width="1024"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="Zoomq.20050615144554" a="E"><vh>KarrigellWebDev</vh>
<v t="ZoomQuiet.20051222104742" a="TV"><vh>Kday2:完成</vh></v>
<v t="ZoomQuiet.20051222105247" a="E"><vh>管理</vh>
<v t="ZoomQuiet.20051222105247.1" a="E"><vh>@thin __init__.py</vh></v>
<v t="ZoomQuiet.20051222105247.2" a="E" tnodeList="ZoomQuiet.20051222105247.2"><vh>@nosent  mana.pih</vh></v>
<v t="ZoomQuiet.20051222105247.3" a="E" tnodeList="ZoomQuiet.20051222105247.3"><vh>@nosent questionnaire.tmpl</vh></v>
<v t="ZoomQuiet.20051222105247.4" a="E" tnodeList="ZoomQuiet.20051222105247.4,ZoomQuiet.20051222105247.5,ZoomQuiet.20051222105247.6,ZoomQuiet.20051222105247.7"><vh>@nosent  qdesign.py</vh>
<v t="ZoomQuiet.20051222105247.5"><vh>&lt;&lt; page declarations &gt;&gt;</vh></v>
<v t="ZoomQuiet.20051222105247.6"><vh>init</vh></v>
<v t="ZoomQuiet.20051222105247.7"><vh>&lt;&lt; try &gt;&gt;</vh></v>
</v>
<v t="ZoomQuiet.20051222105247.8" a="E" tnodeList="ZoomQuiet.20051222105247.8,ZoomQuiet.20051222105247.15,ZoomQuiet.20051222105247.15"><vh>@nosent  qpage.pih</vh>
<v t="ZoomQuiet.20051222105247.15"><vh>&lt;&lt;导航&gt;&gt;</vh></v>
</v>
<v t="ZoomQuiet.20051222105247.16" a="E" tnodeList="ZoomQuiet.20051222105247.16,ZoomQuiet.20051222105247.17,ZoomQuiet.20051222105247.18,ZoomQuiet.20051222105247.19,ZoomQuiet.20051222105247.20,ZoomQuiet.20051222105247.21,ZoomQuiet.20051222105247.22"><vh>@nosent  qpage.py</vh>
<v t="ZoomQuiet.20051222105247.17"><vh>&lt;&lt; page declarations &gt;&gt;</vh></v>
<v t="ZoomQuiet.20051222105247.18"><vh>init</vh></v>
<v t="ZoomQuiet.20051222105247.19" a="E"><vh>expage</vh>
<v t="ZoomQuiet.20051222105247.20"><vh>desc</vh></v>
<v t="ZoomQuiet.20051222105247.21"><vh>askloop</vh></v>
</v>
<v t="ZoomQuiet.20051222105247.22" a="E"><vh>&lt;&lt; try &gt;&gt;</vh></v>
</v>
<v t="ZoomQuiet.20051222105247.23" tnodeList="ZoomQuiet.20051222105247.23,ZoomQuiet.20051222105247.24,ZoomQuiet.20051222105247.24"><vh>@nosent  qprint.pih</vh>
<v t="ZoomQuiet.20051222105247.24"><vh>&lt;&lt;backdesign&gt;&gt;</vh></v>
</v>
<v t="ZoomQuiet.20051222105247.25" tnodeList="ZoomQuiet.20051222105247.25,ZoomQuiet.20051222105247.26,ZoomQuiet.20051222105247.27,ZoomQuiet.20051222105247.28,ZoomQuiet.20051222105247.29,ZoomQuiet.20051222105247.30"><vh>@nosent  qprint.py</vh>
<v t="ZoomQuiet.20051222105247.26"><vh>&lt;&lt; page declarations &gt;&gt;</vh></v>
<v t="ZoomQuiet.20051222105247.27"><vh>init</vh></v>
<v t="ZoomQuiet.20051222105247.28" a="E"><vh>qpubish()</vh>
<v t="ZoomQuiet.20051222105247.29"><vh>askloop</vh></v>
</v>
<v t="ZoomQuiet.20051222105247.30"><vh>&lt;&lt; try &gt;&gt;</vh></v>
</v>
</v>
<v t="ZoomQuiet.20051201224226" a="E"><vh>问卷设计</vh>
<v t="ZoomQuiet.20051204223324" tnodeList="ZoomQuiet.20051204223324"><vh>@nosent easy051201.cfg</vh></v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="ZoomQuiet.20051201224226"># 使用标准
# 这个是Leo 的宏约定，让Leo 将以下的节点及时的保存到指定目录中
@path q

</t>
<t tx="ZoomQuiet.20051204223324">[desc]
pname		= 啄木鸟问卷 之 “基本知晓”
desc		= 自学问卷v0.7
learn   = &lt;a href='http://wiki.woodpecker.org.cn/moin/CPUG'&gt;CPyUG首页&lt;/a&gt;
# 问卷状态: 0 设计中|1 发布中|2 发布过
done		= 0

[ask/1]
question= 啄木鸟社区首页在哪里？
a		= woodpecker.org.cn
b		= python.cn
c		= 不知道……
key		= a # 正确答案

[ask/2]
question= 啄木鸟社区关注的是什么语言的开发推广？
a		= PHP
b		= Perl
c       = Python
d       = ASP
e       = Zope
f		= 不知道……
key		= c # 正确答案

[ask/3]
question= 啄木鸟和CPyUG的关系是？
a		= 联盟
b		= 下属
c		= 所有者
d		= 不知道……
key		= a # 正确答案

[ask/4]
question= 啄木鸟社区的项目组织原则是什么？
a		= 路见不平一声吼！
b		= 听从组织安排
c		= 不知道……
key		= a # 正确答案

[ask/5]
question= 啄木鸟社区提供了什么资源供大家使用？
a		= Wiki
b		= SVN
c       = 邮件列表
d       = 以上全有
key		= d # 正确答案</t>
<t tx="ZoomQuiet.20051222104742">## page was renamed from zhArticleTemplate
##language:zh
#pragma section-numbers on

::-- ZoomQuiet [[[DateTime(2005-12-11T04:45:50Z)]]]
[[TableOfContents]]
= K2日:直接完成功能！ =
'''不管37 21 直接完成心目中的功能先！'''
 * 计划是这样的，要可以直接读取原先的问卷设计 ini 文本，到页面的 TEXTAREA 中，然后可以提交并保存到指定目录中！

== 规划 ==
 * [wiki:self/RocketyKarrigell Rockety 对KarriGell 的设置有很好的介绍]
  * 为了统一组织好你功能站点的开发{{{
[Alias]
..
obp=%(base)s/karriweb/obp
}}} 在`Karrigell.ini` 有进行如此设置，这样一来，就可以通过
 http://localhost/obp/ 来访问了[[FootNote("当然没有在 obp 目录中安置index.htm/index.pih 之类的脚本是不会让你看的说……")]]
 
 * 简单点儿吧！{{{# 约定以下全局性变量
qpath = "q/"
pubq = qpath+"easy051201.cfg"
}}}
  * 使用这样的全局变量定义下来，使用 Leo 快速的将所有的文件控制起来

 * 计划就是这样的:
     http://localhost/obp/KwDay2/mana.pih 看到并可以编辑 ini 问卷设计文稿
     点击提交后 到
     http://localhost/obp/KwDay2/qpage.pih
     可以看到真正保存下来的问卷设计内容
== Cheetah ==
''' 道听途说 各种模板系统中 Cheetah 非常的好和稳定，就用它了！'''
 * 小小看一下子示例，知道 [wiki:self/CheetahTemplateOrg Cheetah] 的基本使用是这样的:
     1. 引入模板`from Cheetah.Template import Template`
     1. 加载模板`page = open("你的模板文件.tmpl","r").read()`
     1. 加载数据`vPool = {'cfgtxt':随便什么字串的值就成}`
     1. 渲染输出`print Template(page, searchList=[vPool])`
     * 则模板中有`$cfgtxt` 的地方就会替换为实际数据
== Leo 组织实现 ==
'''可以在一个统一界面中把握全部章节/元素哪！'''
 * 可以使用中文作章节名目:
     * `问卷`来组织设计文案
     * 就是`@nosent easy051201.cfg`
     * 当然要使用`@path q` 来配合，这样你对 easy051201.cfg 的修改可以立即输出为具体的文件
 * `Ctrl+Alt+c`和`Ctrl+Alt+v` 是 ["Leo"] 中的复制和粘贴操作:
     * 快速从原先的 `@nosent index.pih` 复制整个节点为
     * `@nosent  mana.pih` 管理页面入口
     * `@nosent  questionnaire.tmpl` 修改问卷模板，["Cheetah"]的
=== 干净的处理脚本 ===
'''MVC?尝试一下子'''
 * `@nosent  mana.pih` 是纯HTML页面了！ 算表现？
 * `&lt;%Include("qdesign.py")%&gt;` 来包含一个纯操作脚本，算模式了
 * `@nosent  questionnaire.tmpl` 模板，算数据控制？

=== 八股文样 ===
'''模式化的处理脚本'''
 * 从文学化编程角度看，web 应用的脚本，应该说都一个样儿！
 attachment:snap-KwDay10.png
 
 * 即:
     1. 脚本说明 `@...@c` 部分
     1. 脚本声明 `&lt;&lt; page declarations &gt;&gt;`  引用部分
     1. 行为定义 `@others` 包含的所有下级节点
     1. 实际尝试 `&lt;&lt;try&gt;&gt;` 引用的部分

== 编辑实现 ==
'''其实就是将指定的文件内容读出来发布到页面的TEXTARE 中'''
 * 模板中先准备{{{&lt;textarea NAME="cfgfile" rows="27" &gt;
$cfgtxt
&lt;/textarea&gt;}}}
 * 处理脚本中{{{#!python
#简化引用对象名
from Cheetah.Template import Template as ctTpl
vPool = {}
vPool['cfgtxt'] = open(pubq,"r").read()
page = open("questionnaire.tmpl","r").read()
txp = ctTpl(page, searchList=[vPool])
print txp
}}}
 * bingo! 完成！
 attachment:snap-KwDay21.png
 
== 实现展现 ==
'''就是将ini 的内容整理为HTML的页面展示'''
 * 同样的快速组织一下子:
     1. `@nosent  qpage.pih` 访问的页面
     http://localhost/obp/KwDay2/qpage.pih
     
     1. `@nosent  qpage.py` 实际的数据重组
=== 关键代码 ===
 * `from dict4ini import DictIni` 当然的要从 NewEdit 中扒出 dict4ini.py 安装到当前目录中
 * 创建`def expage(dict):` 问卷输出函式，来将ini 内容整理为相应的页面
 {{{#!python
exp +="&lt;ul&gt;"
# 将字串的字典键值依照数字方式排序
k = [int(i) for i in dict.ask.keys()]
k.sort() # 没有回传的数组重整处理
for i in k:
    ask = dict.ask[str(i)]
    exp +="&lt;li&gt;%s"%ask["question"]
    exp +="&lt;ul&gt;"
    qk = [j for j in ask.keys()]
    qk.sort()
    for q in qk:
        if 1==len(q):
            exp +="&lt;li&gt;%s"%ask[q]
        else:
            pass    
    exp +="&lt;p&gt;正确答案::%s&lt;/p&gt;"%ask["key"]
    exp +="&lt;/ul&gt;"
    exp +="&lt;/li&gt;"
exp +="&lt;/ul&gt;"
return exp
    }}} 双重循环就可以对应的将类似`[ask/1]` 一节中的所有
    类似`a = 赞！` 的选择项按照列表的形式输出了！
attachment:snap-KwDay22.png

== 串联页面 ==
'''将编辑页面和展现页面串联起来'''
 * 当然的要使用 FORM:
{{{&lt;FORM ENCTYPE="multipart/form-data" 
    ACTION="qpage.pih" 
    METHOD=POST&gt;
    }}} 在模板中声明一下子
 * 测试为先！！！在 qpage.py 中加入`print QUERY` 确认倒底传送了什么
 * OK！ 一切吻合想象`open(qpath+pubq,"w").write(QUERY["cfgfile"])`
  * 将传送来的编辑成果先写回文件，再整理展现！

== 明日目标 ==
'''实现了最基本的编辑到保守，还有问卷展示的脚本那未自然的：'''
 * 实现可以真实使用的问卷表单哪！


== 实例下载 ==
使用 [wiki:self/AllAboutSubversion SVN 下载]:
    [wiki:selfsvn/zqlib/trunk/zqlib/tangle/zoomq/Karrigell/obpKWD/KwDay2/ KwDay2实例]

今日成果：
attachment:snap-KwDay2Leo.png


== 讨论 ==
[[Include(/Discuss)]]

----
返回 KarrigellWebDev -- 快速体验K开发








</t>
<t tx="ZoomQuiet.20051222105247">#一步接一步自然的来
"""
1. 组织首页 mana.pih
2. 嵌入表单 使用模板 questionnaire.tmpl
3. 创建处理脚本 qdesign.py
... 然后就瀑布样的该作什么就作什么了(^_^)
"""
@path ./</t>
<t tx="ZoomQuiet.20051222105247.2">&lt;html&gt;
&lt;head&gt;
&lt;title&gt;
&lt;%
print "自由问卷 之 啄木鸟基本知晓 - Powered by Karrigell"
%&gt;
&lt;/title&gt;
&lt;meta content="text/html; charset=utf-8" http-equiv=content-type&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;h1&gt;在线编辑问卷设计文案，自动解析为模拟问卷&lt;/h1&gt;

&lt;%# 最简单的方式将实际处理脚本包含到页面中适当的位置
Include("qdesign.py")
%&gt;

&lt;%"""
#可以随意包含测试输出哪！
# 嗬嗬也可以随时进行方便的多行注释
print dir()
"""
%&gt;

&lt;/body&gt;

&lt;/html&gt;



</t>
<t tx="ZoomQuiet.20051222105247.3">&lt;FORM ENCTYPE="multipart/form-data" 
    ACTION="qpage.pih" 
    METHOD=POST&gt;

编辑问卷设计文本: &lt;br&gt;
&lt;textarea NAME="cfgfile" rows="27" COLS="80"&gt;
$cfgtxt
&lt;/textarea&gt;
&lt;br/&gt;

&lt;INPUT TYPE="submit" VALUE=" &gt;提交设计查看问卷效果&lt; " class="btn"&gt; 

&lt;/form&gt;
</t>
<t tx="ZoomQuiet.20051222105247.4">@ $Id: obpKwd2.leo 325 2005-12-30 04:23:49Z  $
qdesign.py 快捷问卷设计
@c

&lt;&lt; page declarations &gt;&gt;

@others


&lt;&lt; try &gt;&gt;
</t>
<t tx="ZoomQuiet.20051222105247.5">#!/usr/bin/env python
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

</t>
<t tx="ZoomQuiet.20051222105247.6">#初始化参数集中维护！
qpath = "q/"
pubq = qpath+"easy051201.cfg"
</t>
<t tx="ZoomQuiet.20051222105247.7">page = open("questionnaire.tmpl","r").read()
vPool = {}
vPool['cfgtxt'] = open(pubq,"r").read()
txp = ctTpl(page, searchList=[vPool])
print txp

#print dir()
qcfg = DictIni(pubq)
#print len(qcfg)
#print qcfg.desc.learn</t>
<t tx="ZoomQuiet.20051222105247.8">&lt;html&gt;
&lt;head&gt;
&lt;title&gt;
&lt;%
print "自由问卷 之 啄木鸟基本知晓 - Powered by Karrigell"
%&gt;
&lt;/title&gt;
&lt;meta content="text/html; charset=utf-8" http-equiv=content-type&gt;
&lt;/head&gt;
&lt;body&gt;

&lt;h1&gt;自动解析成的模拟问卷&lt;/h1&gt;

&lt;!--
# 咔咔咔！！Leo 支持中文节点定义的哪！
--&gt;
&lt;&lt;导航&gt;&gt;

&lt;%
Include("qpage.py")
%&gt;

&lt;&lt;导航&gt;&gt;

&lt;/body&gt;

&lt;/html&gt;

</t>
<t tx="ZoomQuiet.20051222105247.15">
&lt;h5&gt;
 |&gt; 
&lt;a href="mana.pih"&gt;
返回
[问卷设计页面]修改试题&lt;/a&gt; 
 |&gt; 
&lt;a href="qprint.pih"&gt;
 查看最终效果&lt;/a&gt;
 |&gt; 
&lt;/h5&gt;</t>
<t tx="ZoomQuiet.20051222105247.16">@ $Id: obpKwd2.leo 325 2005-12-30 04:23:49Z  $
qpage.py 快捷问卷模拟展示
@c

&lt;&lt; page declarations &gt;&gt;

@others

&lt;&lt; try &gt;&gt;
</t>
<t tx="ZoomQuiet.20051222105247.17">#!/usr/bin/env python
# coding:utf-8

import time,shutil
import sys,os,string,re

from dict4ini import DictIni</t>
<t tx="ZoomQuiet.20051222105247.18">#初始化参数集中维护！
## 又一个，看来要重构！
qpath = "q/"
pubq = qpath+"easy051201.cfg"

cfgf = pubq

tcode = time.strftime("%y%m%d%H%M%S", time.localtime())

# 先复制一下子
shutil.copy2(cfgf,cfgf+".%s"%tcode)
</t>
<t tx="ZoomQuiet.20051222105247.19">def expage(dict):
    """将dict 内容输出为问卷
    """
    exp = ""
    exp += "&lt;div id='qpage'&gt;"
    @others
    exp += "&lt;/div&gt;" # id=qpage
    return exp
    
    
    
    
    
    
    
</t>
<t tx="ZoomQuiet.20051222105247.20">exp += """&lt;h3&gt;%s —— 
    &lt;sup&gt;%s&lt;/sup&gt;
    &lt;sub&gt;%s&lt;/sub&gt;&lt;/h3&gt;"""%(dict.desc.pname
                            ,dict.desc.desc
                            ,dict.desc.learn)


</t>
<t tx="ZoomQuiet.20051222105247.21">#print dict.ask["1"]
exp +="&lt;ul&gt;"
# 将字串的字典键值依照数字方式排序
k = [int(i) for i in dict.ask.keys()]
k.sort()
for i in k:
    ask = dict.ask[str(i)]
    exp +="&lt;li&gt;%s"%ask["question"]
    exp +="&lt;SUP&gt;正确答案::%s&lt;/SUP&gt;"%ask["key"]
    #unicode(str(dict.ask[i]["question"]), "utf8").encode("utf8")
    exp +="&lt;ul&gt;"
    qk = [j for j in ask.keys()]
    qk.sort()
    #name="animal[]"
    for q in qk:
        if 1==len(q):
            exp +="&lt;li&gt;%s"%ask[q]
        else:
            pass
    exp +="&lt;/ul&gt;"
    exp +="&lt;/li&gt;"
exp +="&lt;/ul&gt;"

</t>
<t tx="ZoomQuiet.20051222105247.22">open(pubq,"w").write(QUERY["cfgfile"])
qcfg = DictIni(cfgf)
print expage(qcfg)
print "&lt;hr/&gt;"

# 测试...
print dir()
print QUERY["cfgfile"]


print qcfg.desc
</t>
<t tx="ZoomQuiet.20051222105247.23">&lt;html&gt;
&lt;head&gt;
&lt;title&gt;
&lt;%
print "自由问卷 之 啄木鸟基本知晓 - Powered by Karrigell"
%&gt;
&lt;/title&gt;
&lt;meta content="text/html; charset=utf-8" http-equiv=content-type&gt;
&lt;/head&gt;
&lt;body&gt;


&lt;&lt;backdesign&gt;&gt;

&lt;%
Include("qprint.py")
%&gt;

&lt;&lt;backdesign&gt;&gt;

&lt;/body&gt;

&lt;/html&gt;

</t>
<t tx="ZoomQuiet.20051222105247.24">
&lt;h4&gt;
 |&gt; 
&lt;a href="mana.pih"&gt;
返回
[问卷设计页面] 修改试题
&lt;/a&gt;
 |&gt; 
&lt;a href="index.ks/logout"&gt;
退出&lt;/a&gt; 
 |&gt; 
&lt;a href="index.ks/index"&gt;
进入回答&lt;/a&gt; 
&lt;/h4&gt;</t>
<t tx="ZoomQuiet.20051222105247.25">@ $Id: obpKwd2.leo 325 2005-12-30 04:23:49Z  $
qpage.py 快捷问卷模拟展示
@c

&lt;&lt; page declarations &gt;&gt;

@others

&lt;&lt; try &gt;&gt;
</t>
<t tx="ZoomQuiet.20051222105247.26">#!/usr/bin/env python
# coding:utf-8

import time,shutil
import sys,os,string,re

#sys.path.append("../../karriweb/src/core")
#from agentweb import *
#from agentsys import *

from dict4ini import DictIni
from Karrigell_QuickForm import Karrigell_QuickForm</t>
<t tx="ZoomQuiet.20051222105247.27">## 元模板对象 使用 Cheetah 系统
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
</t>
<t tx="ZoomQuiet.20051222105247.28">def qpubish(dict):
    """将dict 内容输出为回答问卷
    """
    exp = ""
    p = Karrigell_QuickForm('fm_kq','POST','#',dict.desc.desc)
    exp += "&lt;h1&gt;%s&lt;sup&gt;%s&lt;/sup&gt;&lt;/h1&gt;"%(dict.desc.pname
                                       ,dict.desc.learn)    
    
    p.addElement('node','&lt;ul&gt;','')
    # 深入数据
    @others    
    p.addElement('node','&lt;/ul&gt;','')
    
    p.addGroup(["submit","btn_submit","提交"]
               ,["reset","btn_reset","重写"])
    exp += p.export()
    exp += "&lt;p&gt;返回%s&lt;/p&gt;"%dict.desc.learn
    return exp
    
    
    
    
    
    
    
</t>
<t tx="ZoomQuiet.20051222105247.29">"""
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
            #exp +="&lt;li&gt;%s"%ask[q]
            qli[q] = ask[q]
        else:
            pass
    
    p.addRadioList("cr_ask%s"%i
               ,ask["question"]
               ,qli)


</t>
<t tx="ZoomQuiet.20051222105247.30">#open(qpath+pubq,"w").write(QUERY["cfgfile"])
#print dir()
#print QUERY["cfgfile"]
#p.addRule('cr_ask1','required','问题? is required!')
#p.addElement('text','telephone',{'size':100,'maxlength':40})
#p.addRule('telephone','required','telephone is required!')
#p.addCheckBox('fuda',{'a':'Letra A','b':'Letra B'})
print QUERY
qcfg = DictIni(cfgf)
print "&lt;div id='qpage'&gt;"
#print p.export()
print qpubish(qcfg)
print "&lt;/div&gt;"

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
</t>
<t tx="Zoomq.20050615144554"># 快速利用Karrigell 开发功能站点
# Karrigell.ini 中有如下约定:
# 如果Kariigell 运行在 D:\Karrigell\Karrigell-2.2\ 
# 则其下应该有 karriweb\obp\KwDay1\ 这样的目录，以便安置实例  
[Alias]
..
obp=%(base)s/karriweb/obp



</t>
</tnodes>
</leo_file>
