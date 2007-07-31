##language:zh
##OBP项目图书reST通用文章模板
#format rst
:status: 草稿 ;ZoomQuiet; 90%;

.. contents::
  :depth: 3


-5 PyDay 目标和初次体验
===============================
**Use it! do not learnning** -- 用之,不学!


剧本背景
--------------------

嗯嗯嗯,所谓实例故事,就是设计一个具体情景,让代表读者的菜鸟,跟着代表作者的老鸟,完成一件事儿,在过程中引导式的学习Python;

当然读者不一定菜,作者可能也鸟不过读者,但是,有个具体的事儿,也好说起来不是?就象说书的,也得先来个定场诗什么的活跃一下气氛不是?
那么...


人物
````````````````````
小白:
  读者一方,没有或是仅有一点编程体验的好奇宝宝,想使用Python 解决一个实际的问题


行者:
  嗯嗯嗯!啄木鸟社区的一个或是一群热心的先行学习过Python 的好人,说话可能有些颠三倒四,但是绝对是好心人哪


事件
````````````````````
小白忽然间厌烦了不断的下载安装，破解，却总是找不到称心的软件的生活：“MD!怒了! 什么破软件这么不好使，还要150$!!! 我自个儿写! 用一个丢一个!”


需求开始
--------------------
怎么回事儿呢? 小白到列表中一说,原来是买了台刻录机,这一下, eMule 的下载更加是没日没夜了,但是才一个月刻录出来的光盘就有上百张了,结果想找回一个专辑的MP3,简直不可能了...

想要一种工具:

**可以不用插入光盘就可以搜索所有光盘的内容**


就这么简单的一个愿望,乍就是找不到好用的软件?!


Python!
````````````````````
OK!你们都说Python 好用,那么来尝试一下吧! 我是菜鸟我怕谁?!

运行环境:
  推荐 `ActivePython`_ --一个商业产品,但是有自由使用版权的,一个完善的Python 开始应用环境,关键是文档齐备;
  GNU/Linux 环境中,当然是原生的 `python.org`_


好了,下载,安装,没什么说的,这再不会,先进行电脑扫盲,再来学习编程吧您...


Hello World!
````````````````````
灰常灰常,著名的,但凡是编程语言,第一课都要玩的例程,如果你也想看一看Python 的?

截屏1-1 |snapHelloWorld|

再Show 一个类似的,但是推荐的体验环境 [#]_

截屏1-2 |snapiPyHelloWorld|

是也乎,就是这么简单,告诉Python 打印"Hello World!" 就好.

所以说,对于Python, 勿学,即用就好!



文档
````````````````````
*但是丰富的文档还是可以安抚我们面对未知的恐惧的*,推荐以下深入阅读资料,但是不推荐现在就全面阅读

* DiPy -- `Dive Into Python`_ **深入Python5.4 中文版本**
* `Abyte Of Python`_ -- **简明 Python 教程**
* ASPN -- `Python Reference`_ Python 参考资料汇编
* `woodpecker.org.cn doc`_ -- 啄木鸟社区分享文档库


需求继续
--------------------

嗯嗯嗯!安装好了Python环境,在行者的指点下又收集了一批资料的链接,那么小白想真正开始软件的创造了,
但是,行者又告戒:

 - **明晰你的问题,当问题真正得到定义时,问题已经解决了一半**

  + 因为,程序不过是将人的思想转述为机器可以理解的操作序列而已
  + 对于寻求快速解决问题,而不是研究问题的小白和Pythoner们,精确,恰当的描述问题,就等于写好了程序框架,余下的不过是让程序可以运行罢了

好的,于是小白将直觉的软件需求细化了一下:

* *可以不用插入光盘就可以搜索所有光盘的内容*, 等于说...

 - 可以将光盘内容索引自动储存到硬盘上
 - 可以根据储存到硬盘上的光盘信息进行搜索


-5 PyDay 小结 
===============================

作为开始,今天小白决定使用Python 来解决光盘内容管理,这一实际问题;
安装了python 环境,运行了 "Hello World!" 实例.

OK!轻松的开始,但是,你知道,你同时获得了免费的绝对强大的科学计算器?


练习
--------------------

* 计算今年是闰年嘛?
* 计算...






.. ActivePython:http://www.activestate.com/Products/ActivePython/
.. python.org:http://www.python.org/download/
.. Dive Into Python:http://www.woodpecker.org.cn/diveintopython/index.html
.. Abyte Of Python:http://www.woodpecker.org.cn:9081/doc/abyteofpython_cn/chinese/index.html
.. Python Reference:http://aspn.activestate.com/ASPN/Python/Reference/
.. woodpecker.org.cn doc:http://www.woodpecker.org.cn:9081/doc/Python/
.. |snapHelloWorld| image:: cmd.PNG
.. |snapiPyHelloWorld| image:: ipython.PNG


.. [#] iPython 环境,是个融合了N多Unix Shell 环境特质的Python 交互式命令行环境，推荐使用，你会爱上 TAB 键的;-)
   http://ipython.scipy.org/moin/.


.. macro:: [[PageComment2(nosmiley=1, notify=1)]]

.. macro:: -- ZoomQuiet  [[DateTime(2007-02-20T06:12:54Z)]] 

