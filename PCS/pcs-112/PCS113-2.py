try:
    raise NameError, 'HiThere'
except NameError, a:
    print 'An exception flew by!'
    print type(a)