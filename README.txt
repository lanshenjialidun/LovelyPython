: 可爱的Python 原创图书工程说明:

= 版本 =
 - 080617::Zoomq 追加说明现行目录内容
 - 071215::Zoomq Creat
 
= 目标 =
 - 尝试使用图书的方式来传达我们的Python 学习应用体验 

== 工程资源 ==
 * 项目维基: http://wiki.woodpecker.org.cn/moin/ObpLovelyPython
  * 原始计划: http://wiki.woodpecker.org.cn/moin/ObpBroadview/timeline
 * 讨论列表: http://groups.google.com/group/openbookproject
 * 工程环境: http://code.google.com/p/openbookproject/
  * 版本仓库: http://openbookproject.googlecode.com/svn/trunk/LovelyPython/
  * 修订追踪: http://code.google.com/p/openbookproject/issues/list
 * 会议房间: 
  1. `#zeuux-press`  [http://code.google.com/p/openbookproject/wiki/ZeuuxIrc ZEUUX自有IRC快速使用教程]
  1. `#LovelyPython`  [http://code.google.com/p/openbookproject/wiki/UsageIrc IRC快速使用教程]

 使用 Everydo 进行项目管理:: http://everydo.com/logo.jpg'''[http://obp.everydo.com/projects/599264/todos  obp-Lovely Python 项目首页]'''
  * 来访用户: 帐户:`guest`;口令:`guest`
  * 进度協調: http://obp.everydo.com/projects/599264/@@dashboard

== 成员 ==
主创:
 * Zoom.Quiet
協从:
 * 清风
 * 盛艳
法人:
 * ZEUUX自由软件社区 http://www.zeuux.org/community/zeuux-press.cn.html

= 约定图书SVN结构 =
 同编辑讨论: http://wiki.woodpecker.org.cn/moin/ObpLovelyPyEditorRule
{{{
目录约定:
http://openbookproject.googlecode.com/svn/trunk/LovelyPython/
|-- CDays           (CDays 实例故事代码)
|   |-- cday-1      (按照章节对应分立子目录收集)
|   |   |-- ..
|   |-- ..
|-- KDays           (KDays 实例故事代码)
|   |-- js          (共同JS表单验证模块)
|   |-- kday1       (按照章节对应分立子目录收集)
|   |   `-- q
|   |-- ..
|-- PCS             (Python Cheat Sheet ~ Python 作弊条 内容)
|   |-- pcs-0       (按照章节对应分立子目录收集)
|   |   `-- png
|   |-- pcs-1
|   |   `-- ..
|   |-- ..
|-- exercise        (各章练习，按照章节对应收集)
|   |-- part1-CDays (CDays 实例故事练习，按照章节对应收集)
|   |   |-- cday-1  (按照章节对应收集)
|   |   |   |-- png
|   |   |   `-- script
|   |   |-- cday-2
|   |   |   +-- ..
|   |   +-- ..
|   |-- part2-KDays (KDays 实例故事练习，按照章节对应收集)
|   |   +-- ..
|   |-- part3-PCS   (PCS练习，按照章节对应收集)
|   |   +-- ..
|   `-- part4-Attach(附录练习，按照章节对应收集)
|       +-- ..
`-- pages           (图书主体正文 .moin 文本目录)
    |-- 4editor     (正文无关:图书编辑参考维基页面文本)
    |-- attachments (图书主体正文 对应各章附图/文)
    `-- reST        (正文无关:图书主体正文旧 reST格式文本)
}}}

