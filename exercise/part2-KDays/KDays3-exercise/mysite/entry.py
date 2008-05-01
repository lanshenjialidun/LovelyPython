class Entry(object):
    def __init__(self, id, title, tag, content):
        self.id = id
        self.title = title
        self.tag = tag
        self.content = content
        #and other element...
        
    def __str__(self):
        return 'id: %s\ntitle: %s\ntags: %s\ncontent:%s' % (self.id, self.title, self.tag, self.content)
