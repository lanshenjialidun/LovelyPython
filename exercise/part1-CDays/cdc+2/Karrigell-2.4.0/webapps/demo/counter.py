try:
    visits = int(open(counter_file).read())
except IOError:
    # first visit : the file does not exist
    visits = 0
if not hasattr(Session(),"user"):
    visits += 1
    out = open(counter_file,'w')
    out.write(str(visits))
    out.close()
    Session().user = None   # create attribute user
print "%s visits" %visits
