#!/bin/python
# -*- coding: utf-8 -*-

class MyStack(object):
	def __init__(self, max):
		self.head = -1
		self.stack = list()
		self.max = max
		for i in range(self.max):
			self.stack.append(0)
	
	def put(self, item):
		if self.head >= self.max:
			return 'Put Error: The Stack is Overflow!'
		else:
			self.head += 1
			self.stack[self.head] = item
	
	def get(self):
		if self.head < 0:
			return 'Get Error: The Stack is Empty!'
		else:
			self.head -= 1
			return self.stack[self.head+1]
	
	def isEmpty(self):
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
