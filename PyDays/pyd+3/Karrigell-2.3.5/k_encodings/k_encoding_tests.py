#!/bin/env python
#  -*- coding: iso-8859-15 -*-
# File: k_encoding_tests.py
"""Tests for k_encoding module
"""

# k_encoding_charsets can be rebuilt dynamically (see k_encoding_makecharsets.py)
try :
    import k_encoding_charsets
except :
    import k_encoding_makecharsets
    k_encoding_makecharsets.make()
    import k_encoding_charsets

import k_encoding

# Base dictionnaries with encoding mappings.
# Note that dict indexs use normenc() to be normalized.
encoding2python_map = k_encoding_charsets.encoding2python_map
encoding2mime_map = k_encoding_charsets.encoding2mime_map


python_file1 = (u"""#!/bin/env python
# -*- coding: %(the_encoding)s -*-
# Hello you.
def donothing (x) : pass

""","PY")

python_file2 = (u"""<%%
#!/bin/env python
# -*- coding:  %(the_encoding)s -*-
# Hello you.
def donothing (x) : pass

%%><?xml version="1" encoding="UTF8" ?>
<!DOCTYPE html PUBLIC "//truc/machin" >
<html>
  <head>
  </head>
  <body>
  </body>
</html>
""","PIH")

xml_file1 = (u"""<?xml   version="1.0"  encoding="%(the_encoding)s"  standalone="yes" ?>
<!DOCTYPE shadock  />
<shadock mode='on'>
    <pompe>up</pompe>
    <pompe>down</pompe>
    <pompe>up</pompe>
    <pompe>down</pompe>
    <pompe>up</pompe>
    <pompe>down</pompe>
    <pompe>up</pompe>
    <pompe>down</pompe>
    <pompe>up</pompe>
    <pompe>down</pompe>
    <pompe>up</pompe>
    <pompe>down</pompe>
</shadock>
""",'XML')

html_file1 = (u"""<html>
<head>
    <title>A document title</title>
    <meta http-equiv="Content-Type" content="text/html; charset=%(the_encoding)s">
</head>
<body>pompe pompe pompe pompe pompe</body>
""","HTML")

css_file1 = (u"""


@charset  "%(the_encoding)s"

h1 { text-align: center;  font-size: 200%%; }
h2 { text-align: left; font-size:  150%%;padding-left: 2em; }
""","CSS")


tests_sets = [
    python_file1,
    python_file2,
    xml_file1,
    html_file1,
    css_file1
    ]

print "%-5s %-19s RESULT[%-6s]:%s"%("FORM","ENCODING","WHERE","RETURNED")

encoding_tests = [
    "ASCII",
    "US-ASCII",
    "ISO-8859-1",
    "UTF8"
    ]
    
for e in encoding_tests :
    p = encoding2python_map.get(k_encoding.normenc(e),None)
    assert p
    m = encoding2mime_map.get(k_encoding.normenc(e),None)

    # Test with each exemple.
    for text,comment in tests_sets :
        #  Make text containing encoding directive.
        t = text % { 'the_encoding' : e }

        # Encode it into the encoding to test.
        try :
            s = t.encode(p,"replace")
        except LookupError: # Unsupported encoding.
            continue

        # Tin tin tin tin....
        result = k_encoding.guess_buffer_encoding(s)
        if  result :
            foundin = result.directive
            print "%-5s %-20s    OK[%-6s]:"%(comment,e,result.directive),result
        else :
            foundin = "!found"
            print "%-5s %-20s ERROR[%-6s]:"%(comment,e,"!found"),(e,p)

        # By using command lines like:
        #        python k_encoding_tests.py | grep ERROR | grep XML
        # We can easily found problem cases.
        