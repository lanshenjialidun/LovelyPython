SET_COOKIE["sessionId"] = COOKIE["sessionId"].value

from datetime import datetime,timedelta
exp = datetime.utcnow() + timedelta(minutes=1)
SET_COOKIE["sessionId"]["expires"] = exp.strftime("%a, %d %b %Y %H:%M:%S GMT")
