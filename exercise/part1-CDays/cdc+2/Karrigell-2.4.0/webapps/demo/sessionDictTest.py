import k_session
sessions = k_session.sessionDict

RESPONSE['Content-Type'] = 'text/plain'
for k,v in sessions.iteritems():
    print "session key",k
    for x in dir(v):
        print '[%s] %s' %(x,getattr(v,x))
    print
