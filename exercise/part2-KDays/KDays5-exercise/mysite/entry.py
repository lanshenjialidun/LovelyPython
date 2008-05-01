# -*- coding: utf-8 -*-

class Entry(object):
    '''类Entry
    '''
    def __init__(self, id, title, tag, content):
        '''主要有文章id, 标题, 标签, 内容, 或其他元素
        '''
        self.id = id
        self.title = title
        self.tag = tag
        self.content = content
        #and other element...
    
    def has_keywords(self, keywords):
        '''查找该文章是否含有关键字, 有返回True, 否则返回False
        @note: 只是简单匹配, 读者可以根据需要扩展
        '''
        if keywords in self.title or keywords in self.content:
            return True
        return False
        
    def __str__(self):
        return 'id: %s\ntitle: %s\ntags: %s\ncontent:%s' % (self.id, self.title, self.tag, self.content)
