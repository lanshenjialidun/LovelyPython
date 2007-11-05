import xmlrpclib



server = xmlrpclib.ServerProxy("http://localhost:8888";)



version = server.getVersion()



print "version:"+version
