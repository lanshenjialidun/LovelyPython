d = dict(("%s * %s"%(x, y), x * y) for x in range(1, 10) for y in range(1, 10))
for k, v in d.iteritems():
    print "%s = %s"%(k, v)