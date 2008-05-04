== 目录结构说明 ==
|-- Karrigell-description-all-in-one.txt    所有问题KDays0~KDaysN的描述
|-- README.txt                                        本说明
|-- KDays0-exercise                                KDays第0章对应练习目录
|   |-- KDays0-description.txt                  KDays0的问题描述
|   |-- KDays0-answer.txt                         KDays0的问题答案
|   |-- png                                                    相关截图
|   |-- mysite                                                站点目录, 所对应章节的具体源代码, 注意, 每个章节的mysite都是在之前章节的基础上渐增开发的, 并每个mysite都是独立运行;
|-- KDays1-exercise
|-- ......
|-- KDaysN-exercise


== Karrigell 环境部署说明 ==
(1) 下载并安装Karrigell, 具体可参见KDays0的练习;
(2) 待Karrigell运行成功后, 即在浏览器地址栏中输入localhost:8081能够进入Karrigell文档页面后, 进行以下步骤, 部署习题项目mysite;
(3) 进入Karrigell目录, 有个webapps目录, 该目录是Karrigell默认的web应用根(root)目录, 把mysite直接拷贝到webapps目录下;
(4) 在浏览器地址栏中输入localhost:8081/mysite就可以显示mysite首页;完毕.


== 一些注意 ==
在浏览器地址栏中输入localhost:8081/mysite, 
(1) 若显示无法连接, 则表示未开启Karrigell服务器, 所以应在终端下, 进入Karrigell目录, 运行python Karrigell.py; 
(2) 若出现如下错误:
Error response
Error code 404.
表示未找到对应URL, 这时应查看地址栏中的URL路径有没写错, 再尝试是否可以访问, 若还有404错误, 则应该查找webapps/mysite/下是否有对应名字的文件;
(3) 若出现如下错误:
Error response
Error code 505.
表示内部服务器错误, 即表示Karrigell服务器有问题, 首先应该重新启动一下, 看是否能解决, 若不能解决, 则应该查看Karrigell配置是否有问题, 具体配置(主要是Karrigell.ini的设置)见下;


== Karrigell.ini文件详解 ==
conf/Karrigell.ini文件是Karrigell服务的配置文件, 具体字段含义如下(来自http://www.cnblogs.com/czh-liyu/archive/2008/04/22/1165208.html):

[Directories]
root
设置root选项为根目录的完整路径，你从那里发布文档。初始安装这一项没有设定，默认为服务器目录，即指向为Karrigell/webapps/，这个选择你大可不必设置，因为是默认的。

protected
受保护目录列表；对于这些目录中的每个脚本，执行前都会先执行一个叫AuthentScript.py的脚本。这个AuthentScript.py必须由管理员创建并放进目录。
默认，只有admin目录是受保护的。用“;”分割来添加更多的目录。

allow_directory_listing
如果一个url对应的目录没有index文件，由本项来决定谁可以看这个目录的内容：
all = 所有人
none = 没有人
admin = 只有管理员 - 它的登录密码由admin目录中的k_password.py来配置。
默认值是“admin”。

[Applications]
映射扩展名的MIME类型；据我所知这可以在Netscape上工作，但IE上不行。

[Alias]
你可以为某个目录指定一个别名。例如，如果你创建这个别名：scripts = /home/shengyan/mysite，那么http://localhost/scripts/index.htm这个url就会访问/home/shengyan/mysite/index.htm这个文件。
这一功能很有意思，可以将你的服务器目录与开发目录分开，同时又不至于影响你的工作。

[Server]
port
设置服务器端口（默认为80），建议使用这个选择，如果你的系统里还安装了Apache，如果直接运行python Karrigell.py，就是不能不启动服务器了，Karrigell.ini使用这个port设置功能后，会指向一个8081的服务器端口。
当然，你也可以不开启，但在启动服务器后，要指明端口：
python Karrigell.py -P 8081

debug
这个选项指定debug级别。如果设置为1，所有被导入的模块在每次导入时都会被重置，所以如果你改动了某个被导入的脚本你也不必重启服务器。

silent
如果这个选项被设置为1，控制台窗口就不打印任何消息。

zip
如果这个选项被设置为1，并且用户代理支持gzip编码（大多数浏览器支持），服务器压缩发送给用户代理的数据。这减少用户网络负荷，但多少会增加一点服务器的负荷。

global
这个选项指定所有脚本运行时需要导入的模块的路径。如果有这样一行：
   global = %(base)s/myScript.py; %(base)s/myScript.py
则myScript和myScript模块都可以在所有脚本的名称空间中可用。

ignore
如果找不到就忽略的url列表（返回HTTP代码204而不是404）。默认忽略/favicon.ico。

[Translation]
指定应用程序使用的语言，无论浏览器的该选项是什么。如果不想做任何转译，就设置为lang=default，如果想使用英语，设置为lang=en，以此类推。
装载配置文件前karrigell设定了一个基本变量，它的值是服务器目录。参考默认配置文件Karrigell.ini中的%(base)s/。


== 相关学习资料 ==
(1) Karrigell官方网站: http://karrigell.sourceforge.net/, Karrigell官方文档: http://karrigell.sourceforge.net/en/front.htm, Karrigell官方入门教程: http://en.wikibooks.org/wiki/Karrigell_Tutorial
(2) Karrigell中文版官方文档: http://blog.csdn.net/ChumpKlutz/archive/2007/10/02/1809776.aspx
(3) Karrigell初步安装及运行: http://hi.baidu.com/newtype/blog/item/132be0fe67e6db325d6008c1.html
(4) Karrigell.ini配置详细参考: http://www.cnblogs.com/czh-liyu/archive/2008/04/22/1165208.html