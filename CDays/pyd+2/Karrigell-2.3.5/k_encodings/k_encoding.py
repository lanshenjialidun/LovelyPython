#!/bin/env python
#  -*- coding: iso-8859-15 -*-
# File: k_encoding.py
"""Management of input/output encodings forr Karrigell.

Currently (21/9/2005), Karrigell has no specific support for files encoding.

This module tries to give such a support:
- Identify served files encoding, load them with the right codec.
- Internally work with Unicode strings.
- Serve result back to identified encoding, specifying right MIME type.

Finding source file encoding
============================
We search encoding informations in the following order (first match win):
1 - Try to identify Unicode BOM (Byte Order Mark) indications.
2 - Try to find Python encoding directive.
    As it can come from a standard Python script, a HIP script or a PIH script,
    it can be have a <? before the directive.
3 - Try to find an XML encoding directive.
4 - Try to find an HTML HTTP-EQUIV encoding directive.
5 - Try to find a CSS encoding directive.
6 - Use a default encoding.

Links:
======
Python encoding:
    http://www.python.org/peps/pep-0263.html
    http://docs.python.org/lib/standard-encodings.html
XML encoding:
    http://www.w3schools.com/xml/xml_encoding.asp
    For XML, I used an ASPN script:
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/363841
HTML encoding:
    http://www.w3.org/TR/REC-html40/struct/global.html#adef-http-equiv
    http://vancouver-webpages.com/META/metatags.detail.html#equiv
CSS encoding:
    http://www.w3.org/International/questions/qa-css-charset
IANA character sets:
    http://www.iana.org/assignments/character-sets

"""

#============================================================================
__all__ = [
    "guess_file_encoding",      # fct, From a file name
    "guess_buffer_encoding",    # fct, From a (binary) string (may be BOM)
    "guess_encoding_directive", # fct, From directives in a (unicode) string.
    "normenc",                  # fct, Normalize name to use as key in dictionnaries.
    "encoding2python_map",      # dict, [encoding] --> python encoding
    "encoding2mime_map",        # dict, [encoding] --> preffered MIME name
    "any2unicode",              # fct, string,[list of encodings] --> unicode string
    ]

# k_encoding_charsets can be rebuilt dynamically (see k_encoding_makecharsets.py)
try :
    import k_encoding_charsets
except :
    import k_encoding_makecharsets
    k_encoding_makecharsets.make()
    import k_encoding_charsets

import pprint
import re
import encodings
import codecs

import iso8859_1_ncc
from k_utils import trace

codecs.register(iso8859_1_ncc._registry)

#============================================================================
def encode(s, encoding='ascii'):
    """
    'clever' encoding of a string s:
    if s is not unicode string, return it unchanged.
    else:
    encode s with encoding, using xmlcharrefreplace, but
    if encoding is not defined, use just ascii
    
    """
    if isinstance(s, str):
        return s
    elif isinstance(s, unicode):
        return s.encode(encoding or 'ascii', 'xmlcharrefreplace')
    else:
        # this should never happen
        raise TypeError, "Internal errorr in Karrigell"

#============================================================================
def try_encoding(s, encodings):
    "try to guess the encoding of string s, testing encodings given in second parameter"
    
    for enc in encodings:
        try:
            test = unicode(s, enc)
            return enc
        except UnicodeDecodeError, r:
            pass
            
    return None

#============================================================================
DEBUG = False

pp = pprint.PrettyPrinter()

# Base dictionnaries with encoding mappings.
# Note that dict indexs use normenc() to be normalized.
encoding2python_map = k_encoding_charsets.encoding2python_map
encoding2mime_map = k_encoding_charsets.encoding2mime_map

# List of encodings we will try to use for file interpretation and pattern
# matching, in the order we will try them.
# Note: several encodings has same mapping (ascii) for 0-127 first codes, so
# using ascii as first interpretation codec of the file should give
# good result in many cases. After that, i put one ebcdic directive  (seem
# they share common place for base chars).
# Maybe there are other encodings, with different positions for a-z0-9<#@.
# and so.
# TODO: make it modifiable by configuration file.
analyse_encodings = ["ascii","cp500"]

# List of BOM bytes patterns and corresponding encoding names.
# Sorted by decreasing BOM length !!!.
boms_list = [
    (codecs.BOM_UTF32_BE,"utf_32_be"),
    (codecs.BOM_UTF32_LE,"utf_32_le"),
    (codecs.BOM_UTF8,"utf_8"),
    (codecs.BOM_UTF16_BE,"utf_16_be"),
    (codecs.BOM_UTF16_LE,"utf_16_le")
    ]

#============================================================================
# Small tool function - Python aliases are lowercase... but normalize 
# function dont make names lowercase.
def normenc(e) :
    return encodings.normalize_encoding(e).lower()

#============================================================================
class EncodingResult (object) :
    """
    @ivar encoding: found encoding (cant be None).
    @ivar directive: where the encoding directive was found ('BOM', 'PYTHON',
                     'XLM', 'HTML', 'CSS', 'DEFAULT').
    @ivar pyencoding: corresponding Python encoding (or None).
    @ivar mime: corresponding MIME encoding (or None).
    """
    def __init__(self,e=None,d=None) :
        self.encoding = e
        self.directive = d
        self.pyencoding = encoding2python_map.get(normenc(e),None)
        self.mime = encoding2mime_map.get(normenc(e),None)
    def __repr__(self) :
        return "<EncodingResult(e=%r,p=%r,m=%r,d=%r)>"%(
                self.encoding,self.pyencoding,self.mime,self.directive)

#============================================================================
def guess_file_encoding(filename,default=None) :
    """Read file beginning to search for *encoding information*.

    We limit the part of the file to read to LOOK_AHEAD_SIZE, considering
    that more chars are unuseful (encoding directives generally come
    at beginning of  documents).

    @param filename: pathname of the file to guess encoding.
    @type filename: str
    @param default: default encoding to use if not found - default to None.
    @type default: str (or None)
    @return: found encoding (if found) or None (if nor found).
    @rtype: EncodingResult or None
    """
    f = open(filename,"rb")
    filehead = f.read(LOOK_AHEAD_SIZE)
    f.close()
    return guess_buffer_encoding(filehead,default)

#============================================================================
def guess_buffer_encoding(text,default=None) :
    """Search for encoding informations in a buffer of (binary) data.

    We DONT try to find encoding with strings analysis and tests to see
    if encoding x looks good.
    We try to search for encoding informations from different possible sources:
    python directive, xml directive, html HTTP-EQUIV directive, CSS directive.
    As the data encoding itself can make problem to find encoding directives,
    we try to interpret data using different basic encodings
    (see analyse_encodings global).

    BOMs: they are considered as encoding directives (and tested first).

    @param text: the text from where we must identify encoding.
    @type text: str
    @param default: default encoding to use if not found - default to None.
    @type default: str (or None)
    @return: in all case there is an EncodingResult at function return.
             You must check its members to get guest encoding.
    @rtype: EncodingResult
    """
    for bom,encoding in boms_list :
        if text[0:len(bom)] == bom :
            return EncodingResult(encoding,'BOM')

    for ae in analyse_encodings :
        try :
            s = unicode(text,encoding=ae,errors="replace")
            e = guess_encoding_directive(s)
            if e : return e
        except :
            continue

    if default :
        return EncodingResult(default,'DEFAULT')
    else :
        return None

#============================================================================
def guess_encoding_directive(text,default=None) :
    """Search for encoding directive in the string.

    We look for
        Python  # -*- coding: xxx -*-
        XML     <?xml ... encoding=xxx ?>
        HTML    <meta http-equiv="Content-type" content="....charset=xxx" >
        CSS     @charset "xxx"

    @param text: the (unicode) string to search for an encoding directive.
    @param default: the returned value if no encoding directive is found.
    @return: EncodingResult object
    """
    directive = None
    res = python_encoding_finder.search(text[:PYTHON_ENCODING_SIZE])
    if res : directive = "PYTHON"
    if not res :
        res = xml_encoding_finder.search(text[:XML_ENCODING_SIZE])
        if res : directive = "XML"
    if not res :
        res = html_encoding_finder.search(text[:HTML_ENCODING_SIZE])
        if res : directive = "HTML";
    if not res :
        # for CSS, directive must be on the first *line*.
        res = css_encoding_finder.search(text[:CSS_ENCODING_SIZE])
        if res : directive = "CSS"

    if directive :
        encoding = res.group('encstr')
        encoding = encoding.encode('ascii')
        return EncodingResult(encoding,directive)
    
    if default :
        return EncodingResult(default,'DEFAULT')
    else :
        return None

#============================================================================
# Note: code  was initially before functions... but my editor syntax
# coloring process seem to badly identify  triple  quotes... so I put this
# part of code at the end.
# Python directive identification:
# Example: # -*- coding: latin1 -*-
PYTHON_ENCODING_DIRECTIVE = r"""
    .*?                         # maybe a previous comment or a PIH <%
    \#\s*                       # in a comment line
    -\*-\s*                     # zibouiboui before
    (?:en)?coding\s*[:=]\s*     # encoding directive
    (?P<encstr>                 # what's matched in the brackets will be named encstr
     [-\w.:]+                   # words characters and . and - and : allowed
    )                           # closes the brackets pair for the named group
    \s+                         # at least one space because of '-'
    -\*-                        # zibouiboui after
    """
PYTHON_ENCODING_SIZE = 160  # Must be at first or second line in Python scripts
                            # (maybe third for HIP or PIH)
python_encoding_finder = re.compile(PYTHON_ENCODING_DIRECTIVE,re.VERBOSE)

# XML directive identification:
# Example: <?xml version="1.0" encoding="iso-8859-15" ?>
XML_ENCODING_DIRECTIVE = r"""
    ^<\?xml             # w/o BOM, xmldecl starts with <?xml at the first byte
    .+?                 # some chars (version info), matched minimal
    encoding=           # encoding attribute begins
    ["']                # attribute start delimiter
    (?P<encstr>         # what's matched in the brackets will be named encstr
        [-\w.:]+         # words characters and . and - and : allowed
    )                   # closes the brackets pair for the named group
    ["']                # attribute end delimiter
    .*?                 # some chars optionally (standalone decl or whitespace)
    \?>                 # xmldecl end
    """
XML_ENCODING_SIZE = 100     # Must be at start of file.
# We use re.DOTALL option as cr/lf are normal spaces for XML.
xml_encoding_finder = re.compile(XML_ENCODING_DIRECTIVE,re.VERBOSE|re.IGNORECASE|re.DOTALL)

# HTML directive identification:
# Example: <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=ISO-2022-JP">
HTML_ENCODING_DIRECTIVE = r"""
    .*?
    <meta\s+            # the  considered element
    http-equiv="Content-Type" # maybe allow spaces before/after quotes ?
    \s+
    content="           # maybe allow spaces before quotes ?
    .*?
    charset=            # the whish keyword
    (?P<encstr>         # what's matched in the brackets will be named encstr
        [-\w.:]+        # words characters and . and - and : allowed
    )                   # closes the brackets pair for the named group
    \s*                 # allow spaces after charset
    "                   # attribute value end delimiter
    \s* /?>             # / may be present in xhtml but not in html.
    """
HTML_ENCODING_SIZE = 2048   # May be after other <!DOCTYPE ...><head><meta> elements.
# We use re.DOTALL option as cr/lf are normal spaces for HTML.
html_encoding_finder = re.compile(HTML_ENCODING_DIRECTIVE,re.VERBOSE|re.IGNORECASE|re.DOTALL)

# CSS directive identification:
# Example: @charset "utf8"
# For CSS files, encoding directive must be at the beginning of the file.
CSS_ENCODING_DIRECTIVE = r"""
    ^@charset\s*        # encoding directive begin
    \"
    (?P<encstr>         # what's matched in the brackets will be named encstr
         [-\w.:]+       # words characters and . and - and : allowed
    )                   # closes the brackets pair for the named group
    \"
    \s*
    """
CSS_ENCODING_SIZE = 64      # Must be first in the file.
css_encoding_finder = re.compile(CSS_ENCODING_DIRECTIVE,re.VERBOSE|re.IGNORECASE|re.DOTALL|re.MULTILINE)

# Size of the data block to read from beginning of file.
LOOK_AHEAD_SIZE = max(PYTHON_ENCODING_SIZE,XML_ENCODING_SIZE,
                      HTML_ENCODING_SIZE,CSS_ENCODING_SIZE)



