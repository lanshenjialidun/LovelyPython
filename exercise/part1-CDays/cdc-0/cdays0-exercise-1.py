#!/bin/python
#coding:utf-8
'''cdays0-exercise-1.py 使用类和对象
    @author: U{shengyan<mailto:shengyan1985@gmail.com>}
    @version:$Id$
'''

class MyStack(object):
	'''MyStack
		自定义栈，主要操作有put(), get() and isEmpty()
	'''
	def __init__(self, max):
		'''
		初始化栈：初始栈头指针和清空栈
		@param max: 指定栈的最大长度
		'''
		self.head = -1
		self.stack = list()
		self.max = max
		for i in range(self.max):
			self.stack.append(0)
	
	def put(self, item):
		'''
		将item压入栈中
		@param item: 所要入栈的项
		'''
		if self.head >= self.max:						#判断当前栈是否满了
			return 'Put Error: The Stack is Overflow!'	#提示栈溢出
		else:
			self.head += 1							#不满，则将item入栈，调整栈顶指针
			self.stack[self.head] = item
	
	def get(self):
		'''
		获得当前栈顶item
		@return: 栈顶item
		'''
		if self.head < 0:								#判断当前栈是否为空
			return 'Get Error: The Stack is Empty!'		#提示栈空
		else:
			self.head -= 1							#出栈，返回栈顶元素，并调整栈顶指针
			return self.stack[self.head+1]
	
	def isEmpty(self):
		'''
		获得当前栈的状态，空或者非空
		@return: True(栈空) or False(栈非空)
		'''
		if self.head < -1:
			return True
		return False

if __name__ == "__main__":
	mystack = MyStack(100)
	mystack.put('a')
	mystack.put('b')
	print mystack.get()
	mystack.put('c')
	print mystack.get()
	print mystack.get()
	print mystack.get()
