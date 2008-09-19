#coding:utf-8
class Concept(object):
	conceptNUM = 0   # 定义类变量

	def __init__(self, extent=set(), intent=set()):
		Concept.conceptNUM += 1
		self.conceptID = Concept.conceptNUM  # 以下三个变量是该类的数据成员
		self.extent = extent
		self.intent = intent

	def addIntent(self, intentSet): # 以下2个自定义方法
		self.intent = self.intent.union(intentSet)

	def addExtent(self, extentSet): 
		self.extent = self.extent.union(extentSet)

	def __str__(self):
		return 'Concept %d: (%s), (%s)\n' % (self.conceptID, self.extent, self.intent)

if __name__ == '__main__':
    cpt = Concept()   
    print 'Create: ', cpt
    cpt.addIntent(set([1, 2, 3]))
    print 'Add Intent: ', cpt
    cpt.addExtent(set(['a', 'b']))
    print 'Add Extent: ', cpt
    print cpt.conceptID