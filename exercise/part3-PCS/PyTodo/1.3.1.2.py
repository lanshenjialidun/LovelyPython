import SimpleXMLRPCServer



#定义自己的CMS类  

class MyCMS:

    def getVersion(self):#向外公开版本的方法  

        return "Powerd By Python 0.1a"



cms = MyCMS()

server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8888))

server.register_instance(cms)



print "Listening on port 8888"

server.serve_forever()#服务器执行，并监听8888端口
