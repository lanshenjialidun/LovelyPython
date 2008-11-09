# -*- coding: utf-8 -*-
from Tkinter import *

class App:
   def __init__(self, master):
       #Frame widget
       frame = Frame(master)
       frame.pack()

       self.button = Button ( frame, # master widget
                              text="QUIT",
                              fg="red",
                              command=frame.quit
                              )
       self.button.pack(side=LEFT)
       self.hi_there = Button(frame,
                              text="Hello",
                              command=self.say_hi
                              )
       self.hi_there.pack(side=LEFT)
   def say_hi(self):
       print "Welcome to the world of Python!"
root = Tk()
app = App(root)
root.mainloop()
