# coding:utf-8
import random, string
#打印随机生成的字符、字符串

print '随机生成的字符(a~z)：%c' %random.choice('abcdefghijklmnopqrstuvwxyz')
print '随机生成的字符串(春、夏、秋、冬)：%s' %random.choice(['spring', 'summer', 'fall', 'winter'])
print '随机生成的字符串：%s' %string.join(random.sample('abcdefghijklmnopqrstuvwxyz', 4), '')
