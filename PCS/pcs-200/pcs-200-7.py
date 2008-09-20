import os.path

for user in [ '', 'root', 'mysql' ]:
    lookup = '~' + user
    print lookup, ':', os.path.expanduser(lookup)
