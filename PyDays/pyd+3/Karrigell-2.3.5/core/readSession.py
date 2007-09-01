import shelve

sessionDict=shelve.open("sessions.dat","c",writeback=True)
sessions = sessionDict.keys()
maxSessions = 1000

class SessionElement(object):
    """A SessionElement object has a sessionId attribute and a close() method 
    which erases the item in sessionDict and creates a Set-Cookie header to 
    erase the corresponding cookie
    When a new SessionElement is created a new item is appended to the sessions 
    list. If this list is bigger than the maximum (stored in the maxSessions 
    global variable) then the first element in the sessions list (that is, the 
    oldest recorded session) is deleted. This should avoid the risk of memory 
    overflow
    
    If the session is persistent, only built-in types are accepted as attributes
    of the session object
    """

    def __init__(self,sessionId):
        global sessions
        self.sessionId=sessionId
        self.value = {}
        sessions.append(sessionId)
        if len(sessions)>maxSessions:
            removeOldestSession()

    def __setattr__(self,name,value):
        if not name in ["sessionId","value"]:
            obj = sessionDict[self.sessionId]
            obj[name] = value
            sessionDict[sessionId] = obj
        object.__setattr__(self,name,value)

    def __getattribute__(self,name):
        if name in ["sessionId","value"]:
            return object.__getattribute__(self,name)
        else:
            print "lookup"
            obj = sessionDict[self.sessionId]
            return obj[name]

    def close(self):
        del sessionDict[self.sessionId]

print sessions
sessionId="blablabl"

res=SessionElement(sessionId)
print res
try:
    sessionDict[sessionId]=res.value
except:
    print "error"
print res
res.name = "essai"
print res.name
