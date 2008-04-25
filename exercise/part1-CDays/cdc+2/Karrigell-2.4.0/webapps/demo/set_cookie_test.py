import time

SET_COOKIE["user"] = _user_name
#SET_COOKIE["user"]["max-age"] = "'Wed, 19 Feb 2020 10:00:00 GMT'"
SET_COOKIE["user"]["domain"] = "www.a.com "
#SET_COOKIE["user"]["path"] = "/"
#SET_COOKIE["user"]["expires"] = 'Wed, 19 Feb 2020 10:00:00 GMT'
SET_COOKIE["userid"] = "user_id"
#SET_COOKIE["userid"]["domain"] = " www.a.com"
SET_COOKIE["userid"]["path"] = "/"
SET_COOKIE["userid"]["max-age"] = time.time()+31536000
SET_COOKIE["userid"]["expires"] = 'Wed, 19 Feb 2020 10:00:00 GMT'

import k_utils
#k_utils.trace(SET_COOKIE)
