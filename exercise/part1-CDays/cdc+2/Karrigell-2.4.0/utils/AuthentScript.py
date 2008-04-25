import md5

digest=open("admin.ini","rb").read()
userDigest=digest[:16]
passwordDigest=digest[16:]

def authTest():
    if COOKIE.has_key("admin"):
        if COOKIE["admin"].value == passwordDigest:
            return True
    return False

if not authTest():
    raise HTTP_REDIRECTION,THIS.baseurl+"login.ks"