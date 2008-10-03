# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

# 创建一个根节点root,并设置其标签为"html"
root = ET.Element("html")
# 创建根节点的一个子节点head,并设置其标签为"head"
head = ET.SubElement(root, "head")
# 创建节点head的一个子节点title,并设置其标签为"title",设置其内容为"Title"
title = ET.SubElement(head, "title")
title.text = "Title"

# 创建根节点的一个子节点body,并设置其标签为"body",设置bgcolor属性为#ffffff,设置其内容为"Hello, World!"
body = ET.SubElement(root, "body")
body.set("bgcolor", "#ffffff")
body.text = "Hello, World!"

# 将这个根节点包裹在ElementTree对象中,并且保存为XML格式文件
tree = ET.ElementTree(root)
tree.write("hello.xhtml")