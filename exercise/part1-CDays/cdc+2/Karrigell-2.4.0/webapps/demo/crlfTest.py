RESPONSE["Content-type"] = "text/plain"
import os
for k in os.environ:
    print "[%s] %s" %(k,os.environ[k])