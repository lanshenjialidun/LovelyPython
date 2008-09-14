# coding:utf-8
import xml.etree.ElementTree as ET

# 使用parse()将XML文档加载并返回ElementTree对象
tree = ET.parse("hello.xhtml")

# 寻找head节点下title节点的值
print tree.findtext("head/title")

# 使用getroot()函数返回根节点
root = tree.getroot()

# ...接下来可以做些其他操作

# 保存为本地XML文档
tree.write("out.xml")