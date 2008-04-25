SET_COOKIE['LOGGED']='logged'
SET_COOKIE['LOGGED'].value = 'unlogged'
SET_COOKIE['LOGGED']['path'] = "/"+_baseurl.rstrip('/')
SET_COOKIE['LOGGED']['expires'] = 0

print '<a href="%s">Back</a>' %_path