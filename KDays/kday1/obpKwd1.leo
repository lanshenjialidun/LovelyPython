<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet ekr_stylesheet?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="760" clone_windows="0"/>
<globals body_outline_ratio="0.232421875">
	<global_window_position top="10" left="10" height="698" width="1024"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="Zoomq.20050615144554" a="E"><vh>KarrigellWebDev</vh>
<v t="ZoomQuiet.20051221222402"><vh>Kday1:尝试</vh></v>
<v t="Zoomq.20051111112921" a="ETV"><vh>尝试</vh>
<v t="Zoomq.20051111112932" a="E"><vh>@thin __init__.py</vh></v>
<v t="Zoomq.20051111112956" a="E" tnodeList="Zoomq.20051111112956"><vh>@nosent  try.pih</vh></v>
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
<t tx="ZoomQuiet.20051221222402">= K1日:品尝KarriGell =
'''快速根据PHP 的经验尝试Karrigell 的开发'''
 * 原先的问卷生成系统，其实就是利用从别处扒来的一组手工写的PHP 的问卷页面，利用Python 组织了一个从 ini 设置文本到PHP 页面的流程
 * 其实从txt -&gt; Python -&gt; PHP -&gt; DB -&gt; Python -&gt; 回答统计，这样的数据流程够傻的
 * 总算有了点儿时间，你又听说Python 有N多好的Web 开发平台就要来使用纯Python 的环境重构出一个可以快捷修改，统计简单问卷的小系统。
 
== 准备环境 ==
'''为什么选择KarriGell? 缘分吧…………哈哈哈！'''
 * 看了KarriGell 的介绍，感觉可以快捷开始，就它了
 * 下载KarriGell[[FootNote(现在是[http://karrigell.sourceforge.net/ Karrigell-2.2] )]]
 * 解开，然后：`python Karrigell.py`
 * bing! 你有了一个展示了各种应用的 KarriGell 站点了！就在 http://localhost/
 attachment:snap-KwDay00.png
  * 尝试了一下子在 M$ 和 FreeBSD 平台中，是完全一样的反应！
  * 意味着，只要有Python环境，你随时可以获得一个全功能的Web 应用环境！
 
== 动手动脚 ==
'''跟着教程走，随便动一动'''
 * http://localhost/demo/frame_tour_en.htm 是基础入门的教程，展示了KarriGell 进行 web 开发中最经常要面对的应用实现
 * 你看的懂Python， 当然的，对于 hello 这样的示例已经没有兴趣了，
 * 看过一些前人的体验文章，知道有种 `pih` 的页面交互方式，最象原先的 PHP 开发
 * 跟着教程，http://localhost/demo/test.pih 你直接修改了两下:{{{
&lt;h2&gt;HTTP headers&lt;/h2&gt;
&lt;%
a="Karrigell"
print dir(a)
%&gt;
}}}
  * 嗬嗬！！果然和命令行中的反应一样，看来就将KarriGell 想象为面向 Web 的Python 解释器好了！

== 组织开发环境 ==
'''OK！要可以随时看到教程，同时又有独立的站点空间……'''
 * 你好容易学习，掌握了 Leo ，而且感觉一切都应该由 Leo 组织才自然
 * 那未就按照直觉来定制KarriGell 一下子:
     * 看了其它人的体验……
     * 其实 KarriGell 的设置非常的简单的，由统一的 ini 文件来设定整体行为
     * 你想要的非常简单，就是将KarriGell 的默许教程站点和你的开发隔离开..{{{
[Alias]
# associates an alias to a path on the file system
# always use / as path separator, even on Windows
# if you create this alias : doc=c:/Program Files/Karrigell/doc 
# then the url htpp://host/doc/index.htm will match the file 
# c:\Program Files\Karrigell\doc\index.htm
# demo=%(base)s/demo
doc=%(base)s/doc
debugger=%(base)s/debugger
}}}
  * Yeah! 就是这里，非常直观，那未定义一个你自个儿开发的站点目录在 KarriGell 系统目录中就好
   * 嗯嗯……想念Unix 系统中的 link 了！M$ 中你只能真的在其中建立目录
  * Leo 中快速设立好自个儿的工程，组织一个最简单的 index.pih:{{{
&lt;html&gt;&lt;body&gt;
&lt;%
a="Kariigell"
print dir(a)
%&gt;
&lt;/body&gt;&lt;/html&gt;
}}}
  * 嗯嗯……为了方便使用 `@nosent` 操作符 `Ctrl+S` 就在计划中的目录里生成了文件
  attachment:snap-KwDay01.png
  
  * 对应的，Karrigell.ini 中设定一下{{{
[Alias]
...
k=%(base)s/karriweb
q=%(base)s/karriweb/questionnaire
...
}}}
  * OK! 重启一下子KarriGell : `Ctrl+C` 通用操作，让KarriGell 的Python 进程停止
  * 然后一样的 `python Karrigell.py`
  * 那未 http://localhost/k
   * 嗬嗬，一切如愿！ KarriGell 正如你想象的有了实时的反应，不象CherryPy 你的每次修改，都要重启服务
   * 在KarriGell 中，就象PHP开发那样，每次修改好后，刷一下子页面，立即你的修改就能显示出来

attachment:snap-KwDay02.png

== 规划目标 ==
 * 好了今天的任务，完成！'''评估KarriGell的可用性'''
  * 嗬嗬，其实就是简单的确定 KarriGell 的开发方式
  * 对于简单问卷？ 明天，先要完成的是怎么在KarriGell 中读人外部文件，并可以在页面中修改，然后提交保存...
  * 最终目标是利用 limodou 的 DictIni 类来理解问卷的设计，并将问答收集为一系列文件，最终仍由Python 进行统计成绩……

== 实例下载 ==
使用 [wiki:self/AllAboutSubversion SVN 下载]:
    [wiki:selfsvn/zqlib/trunk/zqlib/tangle/zoomq/Karrigell/obpKWD/KwDay1/ KwDay1实例]

== 讨论 ==
[[Include(/Discuss)]]

----
返回 KarrigellWebDev -- 快速体验K开发</t>
<t tx="Zoomq.20050615144554"># 快速利用Karrigell 开发功能站点
# Karrigell.ini 中有如下约定:
# 如果Kariigell 运行在 D:\Karrigell\Karrigell-2.2\ 
# 则其下应该有 karriweb\questionnaire\KwDay1\ 这样的目录，以便安置实例
[Alias]
..
k=%(base)s/karriweb
q=%(base)s/karriweb/questionnaire
...


</t>
<t tx="Zoomq.20051111112921"># 先快速尝试一下子Karrigell 开发Web功能站点的感觉……
</t>
<t tx="Zoomq.20051111112956">&lt;html&gt;&lt;body&gt;
&lt;%
# 可以将Karrigell 看作使用 web 输出的Python 脚本环境！
print dir()
%&gt;
&lt;!--
喜欢 pih 自由的两类代码的自然组织！
--&gt;
&lt;hr/&gt;
&lt;%
a="Kariigell 是也乎！"
print a # 没有对页面指定编码，默许的会有乱码现象……
print dir(a)
%&gt;
&lt;/body&gt;&lt;/html&gt;</t>
</tnodes>
</leo_file>
