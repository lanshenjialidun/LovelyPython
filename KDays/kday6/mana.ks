##基础宣言
## mana.ks
# 文件名匹配模块
import os,fnmatch,glob
#页面间传递对象
import time,base64,pickle
# 文件高级对象，进行复制
import shutil
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
    /* $Id: questionnaire.leo,v 1.9 2005/12/13 03:43:43 zhouqi Exp $
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
        BACKGROUND-COLOR: #94DA3A}    BODY{font-size: 10px; color: #333333; 
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
    
    </style>    <!--
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



conf = DictIni("questionnaire.cfg")
qpagetpl = "qpagetpl.cfg"
# 使用 Session来记忆成员信息
sess = Session()


def edit(**var):
    """mana.pih 重构而来
    """
    #print var
    if not hasattr(sess, 'usr'):
        sess.usr = pickle.loads(
                    base64.urlsafe_b64decode(var["obj"]))
        sess.usr["qp"] = var["qp"] 
    if "qp" in QUERY.keys():
        if QUERY["qp"]==sess.usr["qp"]:
            pass
        else:
            #说明是新问卷的编辑
            sess.usr["qp"] = QUERY["qp"]
    
    
    print _htmhead("邮件技术部·项目管理·自学问卷管理 - Powered by Karrigell")
    
    
    
    
    
    
    print SPAN(A('退出', href="../index.ks/logout")
               ,id="mana")
    print SPAN(A('首页', href="../index.ks/index")
               ,id="mana")
    print SPAN(A('历史', href="historic")
               ,id="mana")
               
    print H1("在线编辑问卷设计文案，自动解析为模拟问卷")
    #print sess.usr
    #处理设计表单
    if "his" in QUERY.keys():
        #进入历史版本编辑
        qpage = "%s%s.cfg%s"%(conf.qpage.qpath
                    ,sess.usr["qp"]
                    ,"."+QUERY["his"])
    else:        
        qpage = "%s%s.cfg%s"%(conf.qpage.qpath
                    ,sess.usr["qp"]
                    ,"")
        #qpage = conf.qpage.qpath+sess.usr["qp"]+".cfg"
        
    #print open(qpage,"r").read()
    
    dict = DictIni(qpage)
    p = Karrigell_QuickForm('fm_qdesign'
                            ,'POST'
                            ,"page"
                            ,"问卷设计")
    p.addCntTextArea('qpage'
                  ,''
                  ,"%s"%open(qpage,"r").read()
                  ,'30','100')
    p.addGroup(["submit","btn_submit","提交","btn"])
    p.display()    
    
    print htmfoot
    
    
    
def page(**args):
    """qpage.pih 重构而来
    """
    
    print _htmhead("邮件技术部·项目管理·自学问卷管理 - Powered by Karrigell")
    
    
    
    
    
    #print QUERY["qpage"]
    #qcfg = DictIni(conf.qpage.qpath+QUERY["qp"]+".cfg")
    #print sess.usr
    # validation-framework 的对应支持
    #print A("",id="errorDiv")
    #print DIV("",id="errorMessage")
    
    print SPAN(A('退出', href="../index.ks/logout")
               ,id="mana")
    print SPAN(A('首页', href="../index.ks/index")
               ,id="mana")
    print SPAN(A('历史', href="historic")
               ,id="mana")
    print SPAN(A('返回设计', href="edit")
               ,id="mana")
                  
    
    
    qpage = conf.qpage.qpath+sess.usr["qp"]+".cfg"
    # 先复制一下子
    shutil.copy2(qpage,qpage+".%s"%time.strftime("%y%m%d%H%M%S"
                                                 , time.localtime())
                 )
    # 再写入文件
    open(qpage,"w").write(QUERY["qpage"])    
    #qcfg = DictIni(QUERY["qpage"])
    # 只能从文件对象理解！！bug!!!
    qcfg = DictIni(qpage)
    ## 好象有(value=str对象)的使用方式…………
    
    print _qshow(qcfg,"#")
    
    
    
    print htmfoot
    
    
    


def historic(**var):
    #print var
    
    
    print _htmhead("邮件技术部·项目管理·自学问卷管理 - Powered by Karrigell")
    
    
    
    
    
    
    #print sess.usr
    #处理设计表单
    #qpage = conf.qpage.qpath+sess.usr["qp"]+".cfg"
    #allq = os.listdir(conf.qpage.qpath)
    #qnow = fnmatch.fnmatch(allq, '*.cfg')
    
    #qnow = [fnmatch.filter(f, '*.cfg') for f in os.listdir(conf.qpage.qpath)]
    qnow = fnmatch.filter(os.listdir(conf.qpage.qpath)
                           , '%s.cfg.*'%sess.usr["qp"])
    
    print SPAN(A('退出', href="../index.ks/logout")
               ,id="mana")
    print SPAN(A('首页', href="../index.ks/index")
               ,id="mana")
    print SPAN(A('返回编辑', href="edit")
               ,id="mana")
    print H3("问卷过往版本:")
    print "<UL>"
    qnow.reverse()
    for l in qnow:
        s = l.split(".")
        print LI(A("""%s 
                 <sup>%s/%s/%s %s:%s:%s 版本</sup>
                 <sub>大小:%sb</sub>"""%(s[0]
                 ,s[-1][:2]
                 ,s[-1][2:4]
                 ,s[-1][4:6]
                 ,s[-1][6:8]
                 ,s[-1][8:10]
                 ,s[-1][10:]
                 ,os.stat(conf.qpage.qpath+l)[-4]
                 ),href="edit?his=%s"%s[-1]
                    )
                 )
        #print dir()
    print "</UL>"
            
    
    print htmfoot
    
    
    

def _qshow(dict,aim):
    """将dict 内容输出为回答问卷
    """
    exp = ""
    p = Karrigell_QuickForm('fm_kq','POST',aim,dict.desc.desc)
    #p.addElement('submit','btn_submit',{'value':'退出'})   
    
    exp += "<h1>%s</h1>"%(dict.desc.pname)
    exp += "<h6>自学资料: %s</h6>"%(dict.desc.learn)
    p.addElement('node','<ul>','')
    # 深入数据
    
    # 要根据平均值原则,生成不同的radio列表
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
        #print qk
        for q in qk:
            if 1==len(q):
                #exp +="<li>%s"%ask[q]
                qli[q] = ask[q]
            else:
                pass
        question = ask["question"]+"<sup>答案::%s</sup>"%ask["key"]
        #print qli.items()
        #051219 fixed rurn of dict
        liq = [q for q in qli.keys()]
        liq.sort()
        #print liq
        
              
        if i%2 == 0:        
            p.addRadioLi("cr_ask%s"%i
                   ,question
                   ,qli
                   ,liq
                   ,"even")
        else:        
            p.addRadioLi("cr_ask%s"%i
                   ,question
                   ,qli
                   ,liq)
        
        #print qli.items()
        """
        if 0==len(ctrl.keys()):        
            if i%2 == 0:        
                p.addRadioList("cr_ask%s"%i
                       ,question
                       ,qli
                       ,"even")
            else:        
                p.addRadioList("cr_ask%s"%i
                       ,question
                       ,qli)
        else:    
            if i%2 == 0:        
                #p.addRadioList("cr_ask%s"%i
                p.addVarRadioList("cr_ask%s"%i                        
                       ,question
                       ,qli
                       ,ctrl
                       ,"even")
            else:        
                #p.addRadioList("cr_ask%s"%i
                p.addVarRadioList("cr_ask%s"%i
                       ,question
                       ,qli
                       ,ctrl)
        """
        
        
        p.addJSRule("cr_ask%s"%i,"问题%s "%i)
    
    
    
    
    
    #p.addJSValidation()
    #p.saveJSRule("../js/validation-config.xml")
    
    p.addElement('node','</ul>','')
    
    #p.addGroup(["submit","btn_submit","提交","btn"]
    #           ,["reset","btn_reset","重写","btn"])
    exp += p.export()
    exp += "<h6>自学资料: %s</h6>"%(dict.desc.learn)
    #exp += "<p>返回%s</p>"%dict.desc.learn
    return exp
    
    
    
    
    
    
    
def _ctrl(dict):
    """将平均分计算模式转换为统一控制对象
    [grade]
    # key|point
    ctrl = point
    point=a->5;b->4;c->3;d->2;e->1
    """
    ctrl={}
    if "point" == dict.ctrl:
        for k in dict.point.split(";"):
           s=k.split("->")
           ctrl[s[0]]=s[1]
    else:
        pass
    #print len(ctrl.keys())
    return ctrl









