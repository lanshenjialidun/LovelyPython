import md5

digest=open("../../../admin/admin.ini","rb").read()
userDigest=digest[:16]
passwordDigest=digest[16:]

def authTest():
    return (md5.new(AUTH_USER).digest()==userDigest \
        and md5.new(AUTH_PASSWORD).digest()==passwordDigest)

Authentication(authTest,realm=_("Administration"),errorMessage=_("Authentication error"))
