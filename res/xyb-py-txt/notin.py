#!/usr/bin/env python
# -*- coding: GB2312 -*-

"""Print the lines in FILEA and not in FILEB.

notin.py FILEA FILEB
FILEA and FILEB must be sorted
"""

__revision__ = '1.0'

import sys

def notin(sorted_file_a, sorted_file_b):
    r"""compare two file

    >>> from StringIO import StringIO
    >>>
    >>> a = '\n'.join('abdfgh')
    >>> b = '\n'.join('bcef')
    >>> list(notin(StringIO(a), StringIO(b)))
    ['a', 'd', 'g', 'h']
    """
    fa = sorted_file_a
    fb = sorted_file_b
    fa = isinstance(fa, str) and open(fa) or fa
    fb = isinstance(fb, str) and open(fb) or fb

    sa = fa.readline()
    sb = fb.readline()
    while True:
        if not sa: break
        if not sb: break
        sa = sa.rstrip('\n')
        sb = sb.rstrip('\n')

        compare = cmp(sa, sb)
        if (compare < 0):
            # FILE A only
            yield sa
            sa = fa.readline()
        elif (compare == 0):
            # both
            sa = fa.readline()
            sb = fb.readline()
        else:
            # FILE B only
            sb = fb.readline()

    # print more FILEA
    if sa:
        yield sa.rstrip('\n')
        for sa in fa:
            yield sa

def test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'test':
        test()
        sys.exit()
    for i in notin(sys.argv[1], sys.argv[2]):
        print i


