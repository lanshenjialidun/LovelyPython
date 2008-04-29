import base64

basestr = base64.encodestring("yanxu 123")
print "base64 encodestring:",basestr
print "base64 decodestring:",base64.decodestring(basestr)