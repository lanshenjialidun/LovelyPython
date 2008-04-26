#!/bin/python
#coding:utf-8
'''cdays0-exercise-1.py using class and object
    @author: U{shengyan<mailto:shengyan1985@gmail.com>}
    @version:$Id$
'''

class MyStack(object):
	'''MyStack
		user-defined stack, has basic stack operations, such as put(), get() and isEmpty()
	'''
	def __init__(self, max):
		'''
		init the stack: the head of stack and empty the stack
		@param max: specify the max length of stack
		'''
		self.head = -1
		self.stack = list()
		self.max = max
		for i in range(self.max):
			self.stack.append(0)
	
	def put(self, item):
		'''
		put item into the stack
		@param item:  anything want to put the current stack
		'''
		if self.head >= self.max:						#判断当前栈是否满了
			return 'Put Error: The Stack is Overflow!'	#提示栈溢出
		else:
			self.head += 1							#不满，则将item入栈，调整栈顶指针
			self.stack[self.head] = item
	
	def get(self):
		'''
		get the top item of current stack
		@return: the top item
		'''
		if self.head < 0:								#判断当前栈是否为空
			return 'Get Error: The Stack is Empty!'		#提示栈空
		else:
			self.head -= 1							#出栈，返回栈顶元素，并调整栈顶指针
			return self.stack[self.head+1]
	
	def isEmpty(self):
		'''
		get the state of current stack
		@return: True(the stack is empty) or False(else)
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
