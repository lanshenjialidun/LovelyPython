"""Session management
New in version 2.1 : sessions can be persistent, if the
persistentSession in section [Server] of the configuration file
is set to 1
In this case, session information is stored in a shelve file, indexed
by the sessionId (a unique 8-characters string). In this case, only 
built-in types are accepted as attributes to the session object
"""

import os
import cgi
import marshal
import datetime

import PyDbLite

import k_utils, k_config

# structure holding session info
# a dictionary or a shelve file according to the persistentSession option
if k_config.persistentSession:
    sessionFile=os.path.join(k_config.rootDir,"sessions.pdl")
    sessionDb=PyDbLite.Base(sessionFile).create("sessionId","__modif__",
        "values", mode="open")
    sessionDb.create_index("sessionId")
    sessions = sessionDb._sessionId.keys()
else:
    sessionDict={}
    sessions=[]         # list held to avoid overflow
maxSessions=1000    # maximum number of simultaneous sessions

Errors=k_utils.LimitedDict(100) # used for IO errors in karrigellRequestHandler

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
        sessions.append(sessionId)
        if len(sessions)>maxSessions:
            removeOldestSession()

    def close(self):
        del sessionDict[self.sessionId]
        sessions.remove(self.sessionId)

class PersistentSessionElement(object):
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

    def __init__(self,sessionId,values={}):
        global sessions
        self.sessionId = sessionId
        self.__values__ = values
        self.__modif__ = datetime.datetime.now()
        sessions.append(sessionId)
        if len(sessions)>maxSessions:
            removeOldestSession()

    def __setattr__(self,name,value):
        """Override setattr
        Check that the session object is only made of built-in types"""
        if not name in ["sessionId","__values__","__modif__"]:
            try:
                marshal.dumps(value)
                self.__values__[name] = value
                self.__modif__ = datetime.datetime.now()
            except:
                errMsg="In persistent sessions, the session object "
                errMsg+="can only contain built-in types, not %s" %value
                raise TypeError, errMsg
        else:
            object.__setattr__(self,name,value)

    def __getattribute__(self,name):
        if name in ["sessionId","__values__","__modif__","close"]:
            return object.__getattribute__(self,name)
        else:
            return self.__values__[name]

    def __getattr__(self,name):
        return __getattribute__(self,name)

    def close(self):
        del sessionDb[sessionDb._sessionId[self.sessionId][0]["__id__"]]
        sessionDb.commit()
        sessions.remove(self.sessionId)

def removeOldestSession():
    oldestId=sessions.pop(0)
    if k_config.persistentSession:
        r = sessionDb._sessionId[oldestId][0]
        del sessionDb[r["__id__"]]
    else:
        del sessionDict[oldestId]

def getSessionObject(sessionId):
    if k_config.persistentSession:
        res = sessionDb._sessionId[sessionId]
        if res:
            res = PersistentSessionElement(sessionId,res[0]["values"])
        else:
            res = PersistentSessionElement(sessionId)
            sessionDb.insert(sessionId,{})
            sessionDb.commit()
    else:
        try:
            res=sessionDict[sessionId]
        except KeyError:
            res=SessionElement(sessionId)
            sessionDict[sessionId]=res
    return res

def store(sessionId,sessionObject):
    if k_config.persistentSession:
        obj = sessionDb._sessionId[sessionId][0]
        sessionDb.update(obj,values=sessionObject.__values__)
        sessionDb.commit()

if __name__=="__main__":
    pass
    