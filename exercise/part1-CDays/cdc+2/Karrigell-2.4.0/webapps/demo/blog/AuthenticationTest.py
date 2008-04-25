import md5

digest=open("../../../admin/admin.ini","rb").read()
userDigest=digest[:16]
passwordDigest=digest[16:]

if (md5.new(_login).digest()==userDigest \
        and md5.new(_password).digest()==passwordDigest):
    Session().blog_admin = True
    raise HTTP_REDIRECTION,'index.ks'
else:
    print 'Administrator login failed'