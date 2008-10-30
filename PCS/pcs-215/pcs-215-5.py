# coding:utf-8
import random
#打印随机排序结果

items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
print '%s' %items
random.shuffle(items)
print '随机排序结果为：\n%s' %items
