import os.path

for user in [ '', 'dhellmann', 'postgres' ]:
    lookup = '~' + user
    print lookup, ':', os.path.expanduser(lookup)