SET_COOKIE['jc1'] = "some text"
SET_COOKIE['jc1']['expires'] = 'Sat, 5 May 2006 10:00:00 GMT'
SET_COOKIE['jc2'] = "some other text"
SET_COOKIE['jc2']['max-age'] = 600        # i.e. in 10 minutes. 
print "cookies set"
