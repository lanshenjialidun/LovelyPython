##基础宣言
## questionnaire.ks
# 文件名匹配模块
import os,fnmatch
#页面间传递对象
import time,base64,pickle
# XML 处理模块
from elementtree import ElementTree
# Karrigell 提供支持模块
from HTMLTags import *
from dict4ini import DictIni
from Karrigell_QuickForm import Karrigell_QuickForm

## HTML 代码准备
def _htmhead(title):
    """基础复用页面元素控制
    """
    htm = """<html><head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>"""
    htm += title
    htm += """</title>
    <style>
    /* $Id: obpKwd6.leo 325 2005-12-30 04:23:49Z  $
    Karrigell 使用的CSS
    Django 颜色！*/
    /*esp for 问卷::自动居中！margin: 0 auto;*/

    DIV#qpage{width: 700px;
        font-size: 12px;
        margin: 0 auto;}
    fieldset{background-color: #ffffff;
        margin:.5em auto;}
    legend{font-size: 12px;}
    #qpage ul{width: 650px;}
    #qpage ul li{list-style-type :decimal;}
    DIV#qlist{}
    #qpage ul ul li{list-style-type :none;
        display :inline ;
        }
    LI UL#staff li{list-style-type :circle;}
    LI#even{BACKGROUND-COLOR: #EEF3F5;}

    SPAN#mana {font-size: 12px;
        float:right;text-align : center; 
        BACKGROUND-COLOR: #930;
        background-color: whitesmoke; 
        border-bottom: 2px solid #234F32;
        border-left: 2px solid #487858;
        margin:0px;padding: 0px;}
    SPAN#mana A{
        padding: 2px 5px 0px 2px;}
    SPAN#mana A:hover{BACKGROUND-COLOR: #E0FFB8;}
    DIV#errorMessage{font-size: 14px;color: #333;
        font-weight: bold;border: 0px solid #930;
        BACKGROUND-COLOR: #94DA3A}
    BODY{font-size: 10px; color: #333333; 
        text-indent: 1em; 
        background-color: whitesmoke; 
        margin: .5em;    
        font-family: Tahoma;
        scrollbar-face-color:#99CC99;
        scrollbar-shadow-color: #ffffff;
        scrollbar-highlight-color: #99CC99;
        scrollbar-3dlight-color: #ffffff; 
        scrollbar-darkshadow-color:#99CC99; 
        scrollbar-track-color: #E6E6E6;
        scrollbar-arrow-color: #ffffff;
    }
    P,UL,OL,DL,TABLE,TR,TH,TD,A,FONT {font-family: Tahoma,Arial,Helvetica}
    HR {font-size: 1px; color: #99CC99}

    BODY A{color: #002000; text-decoration: none}
    A{font-size: 1em; }
    A:hover{color:#993300; text-decoration: underline;}

    HR{
        margin: 0px;
    	padding: 0px;
        }
    /*Dganjo green theater
    #092E20 #234F32 #99CC99 #487858  #E0FFB8
    亮边 #94DA3A*/
    H1{	font-size: 16px;font-family: SimHei,Arial,Helvetica;
    	font-weight: lighter;letter-spacing:4px;
    	color: #FFFFFF;
    	text-align: left;
    	background-color: #092E20;	
    	border: 2px solid #234F32;
    	margin: 0px;
    	padding: 6px;
        }
    H1 A{color:#94DA3A;}
    H2{ font-size: 14px; font-family: SimHei,Arial,Helvetica;
        font-weight: lighter; letter-spacing:4px;
        color: whitesmoke;     
        text-align: left;
        background-color: #234F32;
    	border: 2px solid #487858;
        margin: 0px;
    	padding: 5px;
        }
    H2 A{ font-size: 14px;font-family: SimHei,Arial,Helvetica; 
        font-weight: lighter; color: #FFCC80;
        }
    H2 A:hover{ }	
    H3{ font-size: 14px; font-family: SimHei,Arial,Helvetica;
        font-weight: lighter; letter-spacing:4px;
        color:whitesmoke;    
        text-align: left;
        background-color: #326342;
    	border: 2px solid #234F32;    
        margin: 0px;	
    	padding: 5px;
        }
        /*亮底#FDEACC 警边#FFCC80*/
    H4{ font-size: 14px; font-family: SimHei,Arial,Helvetica;
        font-weight: lighter;letter-spacing:4px;
        color: #406040;
        text-align: left; 
        background-color: #FFFFE1;
        border: 2px solid #94DA3A;
        margin: 0px;
    	padding: 5px;
        }
    H5{ font-size: 12px; font-family: SimHei,Arial,Helvetica;
        font-weight: lighter; 
        color: whitesmoke; 
        background-color: #487858;
        border: 2px solid #234F32; 
        margin: 0px;
    	padding: 4px;
        }
    H5 A{color: #FFE761; }	
    H5 A:hover{color: #FFE761; }	

    H6{	font-size: 12px;	font-family: SimHei,Arial,Helvetica;
    	font-weight: lighter;
    	color: #FF6633;
    	background-color: #E0FFB8;
    	border: 2px solid #234F32;
        margin: 0px;
    	padding: 2px;
        }


    UL{ font-size: 13px;
    	color:#283E28;
    	list-style-position;
    	margin: 0px 0px 0px 25px;
    	padding: 0px 0px 10px 0px;
    	list-style-type: square;
    	line-height: 130%;		
    }
    LI A{font-weight: lighter;
        color:#283E28;
        }
    LI A:hover{}
    P{  font-size: 12px;  text-indent: 15px; 
        word-wrap: break-word;
        line-height: 120%;
        margin: 5px 5px 5px 15px;
    	padding: 2px ;
        }
    P A{}
    P A:hover{}

    /*表单设计*/

    TABLE { border-collapse: collapse ; font-size: 12px; color: #333333;}

    FORM{
        margin: 0px;
    	padding: 0px;
        }

    TEXTAREA { font-family: "Arial", "Helvetica";
        font-size: 14px; font-weight: light; color: #993300; 
    	background-color: transparent; 
    	border-width: 1px;border-style: solid; border-color: #CCCCCC ;
    	width: 100%}
    SELECT{WIDTH: 100%;
    	font-size: 12px; font-weight: bold;color: #E0F3E0;
    	font-family: "Arial", "Helvetica", "sans-serif"; 
    	background-color: #8DB48D; 
    	border-width: 1px ;border-color: #CCCCCC;}

    INPUT{ font-family: "Arial", "Helvetica";
        font-size: 14px;font-weight: light; color: #993300; 
    	background-color: transparent; 
    	border: 1px solid #838A9E;}

    INPUT.btn { font-size: 13px; 
        font-weight: light; color: whitesmoke; 
    	background-color: #487858; 
    	border-width: 2px; 
        border-color: #E0F3E0 #679265 #333333 #CCCCCC;
    	height: 20px;	
    	padding:0px 1em 2px 1em;}

    INPUT.chkrd { background-color: transparent; border: 0px}
    /*颜色准备*/

    .deep0{
        color: #E0F3E0;
    	background-color: #002000;
    	border: 1px solid #74BADC;
    }
    .deep1{
        color: #E0F3E0;
        background-color: #003300;
        margin:0px 1px 1px 1px;
        }
    .deep2{
        color: #E0F3E0;
        background-color: #283E28;
        }
    .deep3{
        color: #E0F3E0;
        background-color: #314A31;
        }

    .light0{
        color: #406040;
    	background-color: #FFFFFF;
    	margin:0px 1px 1px 1px;
    }

    .light1{
        color: #406040;
        background-color: #E0F3E0;
        }

    .light2{
        color: #002000;
        background-color: #FDEACC;
        }
    .light2 A
        { color: #679265;   }
    .light2 A:hover
        {color: #FF6633;    }
    /*特殊效果*/

    .odd  {
    	font-size: 13px;
    	text-align: center;
    	color:#333333;
    	background-color: #FDEACC;

        }
    .odd A{
        font-size: 13px; text-align: center;
        color:#333333;
        background-color: #FDEACC;        
        }
    .odd A:hover{color:#333333;}   

    .action {
    	font-size: 12px;
    	color:#E6E6E6;	
    }
    .action A{
    	font-size: 12px;
    	color: #406040;

    }
    .action A:hover{
    	font-size: 12px;
    	color: #ffffff;
    	background-color: #CC0000;
    }


    .icon {
    	font-family: "Webdings";
    	font-size: 16px;
    	color:#C9E9C9;
    	background-color: #99CC99;
    	filter: glow(color=red,strength=5);
    	margin: 0px;
    	padding: 0px;
    	vertical-align: baseline;
    	cursor: hand;
    }


    .Webdings{
    	font-family: "Webdings";

    }

    </style>
    <!--
    <script language="javascript" src="/k/js/validation-framework.js"></script>
    -->

    </head>
    <body>    
    <div id='qpage'>
    """
    return htm

htmfoot="""
<br/><br/><br/>
<h5>design by:
    <a href="http://wiki.woodpecker.org.cn/moin/ZoomQuiet">
    Zoom.Quiet</a>
 powered by :

 <a href="http://python.org">
 Python</a>
 ::
 <a href="http://karrigell.sourceforge.net">
 KARRIGELL 2.2</a>
 +
 <a href="http://effbot.org/zone/element.htm">
 ElementTree</a>
</h5>

</div><!--id='qpage'-->

</body>
</html>
"""



# 使用 Session来记忆成员信息
sess = Session()

if not hasattr(sess, 'usr'):
    sess.usr = {"name":"NULL"}

conf = DictIni("questionnaire.cfg")
qpath = conf.qpage.qpath    #"q/"
pubq = conf.qpage.pubq
cfgf = qpath+pubq

## 问卷信息的字典化信息对象
qcfg = DictIni(cfgf)


def index():
    """首先实现的页面
    """
    # 八股化的页面函式组织... clone 统一的页头输出章节！

    print _htmhead("CPyUG·啄木鸟社区·自学问卷管理 obpKwDay6- Powered by Karrigell")






    # 测试/印证外部专用处理页面对象的引入
    #
    #print sess.usr

    if sess.usr["name"]=="NULL":
        raise HTTP_REDIRECTION,"login"
    else:
        # 清理问卷指定
        try:
            if ""!=sess.usr["qp"]:
                sess.usr["qp"] = ""
            else:
                pass
        except:
            pass
        ## 可以随时打印当前 session 值来印证自个儿的想法
        #print sess.usr
        print SPAN(A('退出', href="logout"),id="mana")
        print SPAN(A('首页', href="index"),id="mana")
        print H1("啄木鸟问卷 之 自学问卷集")
        print "<DIV id='cntarea'>"
        qcfglist = []
        #print conf.qpage.qpath
        for f in os.listdir(conf.qpage.qpath):
            if fnmatch.fnmatch(f, '*.cfg'):
                if ("__init__" in f):
                    pass
                else:
                    qcfglist.append(f)
        #print qcfglist
        # 识别问卷发布情况::
        qdone = {}
        qdoing = {}
        qdesign = {}
        for p in qcfglist:
            cfgp = DictIni(conf.qpage.qpath+p)
            if 0==cfgp.desc.done:
               qdesign[p]=cfgp
            elif 1==cfgp.desc.done:
               qdoing[p]=cfgp
            elif 2==cfgp.desc.done:
               qdone[p]=cfgp
            else:
                qdesign[p]=cfgp

        #分别列表显示问卷

        print H4("发表中的问卷::")

        print UL("".join([str(LI(
         B(A(qdoing[i].desc.pname
             ,href="page?qpname=%s&do=doing"%i.split(".")[-2])
             ## Zoomq::051220 slide show
             #,href="issue?qpname=%s&do=doing"%i.split(".")[-2])
             )+             
             SUB(A("回答统计",href="stat?qp=%s"%i))
                     )
                    ) for i in qdoing.keys()
                ])
                ,id="qplist")

        print H3("已发布的问卷::")
        print UL("".join([str(LI(
                    B(A(qdone[i].desc.pname
                        ,href="page?qpname=%s&do=done"%i.split(".")[-2])
                        )+
                         SUB(A("回答统计",href="stat?qp=%s"%i))
                                 )
                                ) for i in qdone
                            ])
                            )

        print H5("准备中的的问卷::")
        print UL("".join([str(LI(
                    B(A(qdesign[i].desc.pname
                        ,href="page?qpname=%s&do=design"%i.split(".")[-2])
                        )+
                        SUP("自学资料::"+qdesign[i].desc.learn)
                                 )
                                ) for i in qdesign
                            ])
                            )
        print "</DIV>"

    """快速设计CSS时可以方便的列印出主要页面元素来看效果
    print H1("H1")
    print H2("H2")
    print H3("H3")
    print H4("H4")
    print H5("H5")
    print H6("H6")
    """

    # 八股化的页面函式组织... clone 统一的页脚输出章节！

    print htmfoot















def login():
    """实际最先完成的页面
    """
    print sess.usr

    print _htmhead("CPyUG·啄木鸟社区·自学问卷管理 obpKwDay6- Powered by Karrigell")





    # 实际活动
    print H1("啄木鸟问卷 之 自学问卷集")

    p = Karrigell_QuickForm('fm_login'
                            ,'POST'
                            ,'chkusr'
                            ,"登录自学问卷")
    p.addHtmNode('text','uname'
                 ,"CPyUG名号"
                 ,{'size':40,'maxlength':37})
    p.addGroup(["submit","btn_submit","提交","btn"]
               ,["reset","btn_reset","重写","btn"])

    p.addRule('uname','required'
              ,"成员名是必须的!Login name is required!")
    #p.addRule('password','required',"Password is required!")
    p.display()


    print htmfoot



    #print QUERY
    #raise HTTP_REDIRECTION,"index"




def logout():
    """完成 login 时顺手就创立的页面
    """
    sess.close()

    #sess.usr = {}
    #sess.usr["name"] ="NULL"
    #print QUERY
    raise HTTP_REDIRECTION,"index"




def chkusr(**args):
    """从login 自然引发的页面
        检查用户登录情况
    """    
    print QUERY
    print "<hr/>"
    print sess.usr
    sess.usr["name"] = QUERY["uname"]
    print sess.usr
    # 不自动跳转页面，打印session 观察……
    raise HTTP_REDIRECTION,"index"
def page(qpname,do):
    """从原 mana.pih 重构过来 统一的问卷管理 .ks
    """

    print _htmhead("CPyUG·啄木鸟社区·自学问卷管理 obpKwDay6- Powered by Karrigell")





    # 序列化对象以便页面间传递
    pisess = pickle.dumps(sess.usr)
    #print pisess
    #print "<br/>尝试URL 安全序列化-->  "
    sessurl = base64.urlsafe_b64encode(pisess)
    #print sessurl
    #print "尝试load 回来--> <br/> "
    #print pickle.loads(base64.urlsafe_b64decode(sessurl))
    #print QUERY
    #base64.urlsafe_b64encode(pickle.dumps(obj))
    #pickle.loads(base64.urlsafe_b64decode(obj))

    qcfg = DictIni(conf.qpage.qpath+qpname+".cfg")

    if sess.usr["name"]=="NULL":
        raise HTTP_REDIRECTION,"login"
    else:
        sess.usr["qp"] = qpname
        # 051224 加入问卷状态
        sess.usr["do"] = do

        print SPAN(A('退出', href="logout"),id="mana")
        print SPAN(A('首页', href="index"),id="mana")
        print SPAN(A("编辑管理问卷"
                     ,href="../mana.ks/edit?qp=%s&obj=%s"%(sess.usr["qp"]
                        ,base64.urlsafe_b64encode(pickle.dumps(sess.usr))
                                )
                        )
                    ,id="mana")


        # 整理原问卷解析为标准函式
        print _qpublish(qcfg,"bye",do,qpname)        
        """将dict 内容输出为回答问卷
            - dict 问卷设计字典
            - aim 提交目标
            - type 统计模式
            - qpname 问卷名
        """


    print htmfoot




def stat(**args):
    """平均成绩快速统计
    """

    print _htmhead("CPyUG·啄木鸟社区·自学问卷管理 obpKwDay6- Powered by Karrigell")





    print SPAN(A('退 出', href="logout")
               ,id="mana")
    print SPAN(A('首 页', href="index")
               ,id="mana")

    print "<DIV id='cntarea'>"
    #print sess.usr
    crtqp = ""
    qpname = ""
    #print QUERY
    if "qp" in QUERY.keys():
        #print "无登录？"
        crtqp = conf.qpage.qpath+QUERY["qp"]
        qpname = QUERY["qp"].split(".")[0]
    else:
        crtqp = conf.qpage.qpath+sess.usr["qp"]+".cfg"
        qpname = sess.usr["qp"]

    # 准备好正确答案
    crtqp = DictIni(crtqp)
    # 发现问题..字典的无序和回答的有序!
    #print crtqp.ask.keys()
    # 字典排序技巧
    ak = crtqp.ask.keys()
    ak.sort()
    #print ak
    crtright = [crtqp.ask[i]["key"] for i in ak]
    #print crtright

    # 包含mm 处理脚本,以引入组织成员信息
    Include("../xslmm/deptorg.py")    

    ali = fnmatch.filter(os.listdir(conf.qpage.apath)
                           , '%s.*.aq'%qpname)
    aed = []
    for f in ali:
        a = open(conf.qpage.apath+f
                   ,"r").read()
        aed.append(f.split(".")[-2])

    done = []       # 有效回答容器
    unknow = []     # 未知成员容器
    stat = []       # 总均成绩容器
    for a in aed:
        if a in sess.usr["dept"].keys():
            done.append(a)
        else:
            unknow.append(a)
    print H4("部门成员问答统计:<sup>以帐号字母顺序排列</sup>")
    print "<ul id='stat'>"

    mem = sess.usr["dept"].keys()
    mem.sort()
    #print mem
    for a in mem:
        if a in done:
            fn = conf.qpage.apath+'%s.%s.aq'%(qpname,a)
            print LI(B(sess.usr["dept"][a])+
                     I(" %s 已答！ 分数::%s"%(
                                time.strftime("%y/%m/%d %H:%M:%S"
                                    ,time.localtime(os.path.getmtime(fn))
                                    )
                                ,"%.2f"%(_grade(crtright
                                        ,open(fn,"r").read().split())
                                        )
                                )
                        )
                    )
            stat.append(_grade(crtright
                               ,open(fn,"r").read().split())
                               ) 
        else:
            print LI(I(sess.usr["dept"][a])+
                       B("  未答")
                       )

    print "</ul>"


    if len(stat)==0:
        pass
    else:
        print H4(" %d名成员完成问卷， 总均分值:: %.2f"%(len(stat)
                                           ,sum(stat)/len(stat)))
    #reduce(lambda a,b:a+b, s)
    #print H5("%.2f%%"%(reduce(lambda a,b:a+b, stat)/len(stat)))


    if len(unknow)==0:
        pass
    else:
        print BR()+B("未知成员回答情况:")
        print UL(Sum([LI(i+"") for i in unknow])
                 ,id='stat')

    print "</DIV>"

    print htmfoot






def bye(**args):
    """不使用客户端验证后替代的服务端检验页面
    """

    print _htmhead("CPyUG·啄木鸟社区·自学问卷管理 obpKwDay6- Powered by Karrigell")





    print H1("%s"%(qcfg.desc.pname))

    qk = QUERY.keys()

    if "btn_submit" in qk:
        #print QUERY
        qp = DictIni(conf.qpage.qpath+sess.usr["qp"]+".cfg")
        qli = [i for i in qp.ask.keys()]
        a = []
        as = ""
        # 扫描并记录设计问卷的所有题目
        for k in qk:
            if "btn_submit"==k:
                pass
            else:
                as+=QUERY[k]+"\n"
                a.append(k[6:])
        lost=[]
        qli.sort()
        # 对比,计数 已经回答的
        for q in qli:
            if q not in a:
                lost.append(q)

        if 0==len(lost):
            answer = "%s%s.%s.aq"%(conf.qpage.apath
                                  ,sess.usr["qp"]#pubq.split(".")[-2]
                                  ,sess.usr["name"])
            open(answer,'w').write(as)
            ## 正常跳转到统计页面

            raise HTTP_REDIRECTION,"stat"

        print BR()*2
        print H4("没有回答完全！")
        for l in lost:
            print LI("问题%s 没有回答!"%l)
        print """<h4><input type="button"
            value="点击返回重新回答"
            class="btn"
            onClick="history.back();"/>
        </h4>
        """




    else:
        raise HTTP_REDIRECTION,"index"


    print htmfoot




    #raise HTTP_REDIRECTION,"stat"
    #raise HTTP_REDIRECTION,"logout"



def _qpublish(dict,aim,type,qpname):
    """将dict 内容输出为回答问卷
        - dict 问卷设计字典
        - aim 提交目标
        - type 统计模式
        - qpname 问卷名
    """
    exp = ""
    qptitle = """<h6>
        <SPAN><B>%s</B></SPAN>
        (自学资料::%s)</h6>        
        """%(dict.desc.pname
             ,dict.desc.learn)
    if "doing" == type:
        pass
    elif "done" == type:
        aim="#"
    elif "design" == type:
        pass

    p = Karrigell_QuickForm(qpname,'POST',aim,dict.desc.desc)
    exp += "<h1>%s</h1>"%(dict.desc.pname)
    exp += "<h6>自学资料: %s</h6>"%(dict.desc.learn)
    #SPAN(B("问卷进行中::"),id="title")
    p.addElement('node',"<DIV id='qlist'><ul>","")
    # 深入数据
    # 题目循环输出
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
        #051219 fixed rurn of dict
        liq = [q for q in qli.keys()]
        liq.sort()    
        if i%2 == 0:
            p.addRadioLi("cr_ask%s"%i
                   ,ask["question"]
                   ,qli
                   ,liq
                   ,"even")
        else:
            p.addRadioLi("cr_ask%s"%i
                   ,ask["question"]
                   ,qli
                   ,liq)

        ## JVF 调试太复杂不用之！
        #p.addJSRule("cr_ask%s"%i,"问题%s "%i)



    # 由于JVF 的浏览器兼容问题，先放弃！
    #p.addJSValidation()
    #p.saveJSRule("../js/validation-config.xml")

    p.addElement('node','</ul></DIV>','')

    if "doing" == type:
        p.addGroup(["submit","btn_submit","提交","btn"]
                   ,["reset","btn_reset","重写","btn"])    
    elif "done" == type:
        pass
    elif "design" == type:
        pass


    exp += p.export()
    #exp += "<h6>自学资料: %s</h6>"%(dict.desc.learn)
    exp += qptitle
    #exp += "<p>返回%s</p>"%dict.desc.learn
    return exp



def _grade(right,answer):
    """根据问卷答案自动计算分数
    """
    grade = 0
    for i in range(0,len(right)):
        try:
            if right[i]==answer[i]:
                grade +=1
            else:
                pass
        except:
            # 默许没有回答的部分都是错的
            pass
            #grade +=1

    return 100*(float(grade)/len(right))











