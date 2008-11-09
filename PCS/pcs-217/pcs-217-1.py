# -*- coding: utf-8 -*-
from Tkinter import *
#导入Tkinter模块

root = Tk()
#创建一个root Widget
w = Label(root,text = "Hello,world!")
#w是root的子窗口，而text是w的一个选项，表示w中要显示的内容
w.pack()
#在pack后，计算好Label的大小，最终显示在屏幕上
root.mainloop()
#mainloop()除里内部的widget的更新，和来自Windows Manager的通信
