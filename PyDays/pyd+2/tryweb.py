import web
urls = ('/(.*)', 'hello')
class hello:        
    def GET(self, name):
        i = web.input(times=1)
        if not name: name = 'world'
        for c in xrange(int(i.times)): print 'Hello,', name+'!'
if __name__ == "__main__": web.run(urls, globals())
