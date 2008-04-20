#!/bin/env python
#  -*- coding: iso-8859-15 -*-
# File: k_encoding_makecharsets.py
"""
From IANA character sets definitions, to have data in a Python usable form.

This module build k_encoding_charsets containing data about characters sets, 
Python encodings and preffered MIME types.

First, we download charsets description data from  official source:
    http://www.iana.org/assignments/character-sets

Then, we build a list of CharacterSet objects.
Each CharacterSet has four members:
    -*name*     the IANA charset name
    -*mib*      the IANA MIBenum (may be None)
    -*aliases*  a list of alias names for the charset (may be empty list)
    -*mime*     the preffered MIME name  if specified (may be None)


This module called with -g option download the character-sets file from IANA
into the current working directory.

And called with -p option, it prints charsets list.
"""

#============================================================================
__all__ = ["make"]
from os import path
import urllib2
import sys
import pprint
import encodings
from encodings.aliases import aliases as encoding_aliases
from sets import Set

#============================================================================
DEBUG = 0
# The dictionnary of  CharacterSet (indexed by IANA name).
charsets = {}
# List of CharacterSets (indexed by Python encodings).
pyenc_charsets = {}
# Correspondance of aliases and Python encoding.
aliases2python = {}
# Correspondance of aliases and MIME preffered types.
# Note: only aliases having a preffered type are stored.
aliases2mime = {}

#============================================================================
# Small tool function - Python aliases are lowercase... but normalize 
# function dont make names lowercase.
def normenc(e) :
    return encodings.normalize_encoding(e).lower()

#============================================================================
class CharacterSet (object) :
    def __init__(self,name,mib,aliases,mime,pyenc) :
        self.name = name
        self.mib = mib
        self.aliases = aliases
        self.mime = mime
        self.pyenc = pyenc
        self.normnames = [ normenc(n) for n in [name]+aliases]
        
        charsets[name] = self
        if pyenc :
            pyenc_charsets.setdefault(pyenc,[]).append(self)
    def __repr__(self) :
        return "<CharacterSet(name=%r,mib=%r,aliases=%r,mime=%r,pyenc=%r)>"%(self.name,self.mib,self.aliases,self.mime,self.pyenc)


#============================================================================
def upload_iana_file() :
    """Get IANA character sets definitions from its source site.
    
    Return a 
    
    @return: list of lines to iterate on.
    @rtype: [str,str,...]
    """
    f = urllib2.urlopen("http://www.iana.org/assignments/character-sets")
    data = f.read()
    f.close()
    return data.split("\n")

#============================================================================
def analyze_charset_data(iana_data) :
    """Extract data from the IANA character sets definitions.
    
    @param iana_data: definitions of characters.
    @type iana_data: line-iterable (file, list of string...)
    """
    global charsets
    
    # Note: All character sets definitions begin by Name: and finish by a
    # white line.
    NAMEKEYWORD     = "Name: "
    MIBKEYWORD      = "MIBenum: "
    ALIASKEYWORD    = "Alias: "

    in_setdef = False
    name = None
    mib = None
    aliases = []
    mime = None
    pyenc = None

    for line in iana_data :
        line = line.strip()
        if not in_setdef :
            if line.startswith(NAMEKEYWORD) :   # Start of  an entry.
                # The name line can have extra characters:
                # Name:  xxxxx                            [ref1,ref2]
                # Name:  xxxxx (preffered MIME name)      [ref1,ref2]
                name = line.split()[1]
                if "preferred MIME name" in line : mime = name
                in_setdef = True
                if DEBUG : print "Found",name
            continue
        if not line.strip() :
            if not name : continue
            # End of an entry.
            # Search a Python correspondance from one of name/alias.
            for n in [name]+aliases :
                pyenc = encoding_aliases.get(normenc(n),None)
                if pyenc : break
            if DEBUG : print "End",name
            # Make object (it auto-register in dicts/lists).
            CharacterSet(name,mib,aliases,mime,pyenc)
            # Reset...
            name = None
            mib = None
            aliases = []
            mime = None
            pyenc = None
            in_setdef = False
            continue
        # Keep data in set definition.
        if line.startswith(MIBKEYWORD) :
            mib = int(line[len(MIBKEYWORD):])
        elif line.startswith(ALIASKEYWORD) :
            alias = line[len(ALIASKEYWORD):]
            if alias == "None" : continue
            # ... yes, there are lines with "Alias: None" ...
            if "preferred MIME name" in alias :
                alias = alias.split()[0]
                mime = alias
            aliases.append(alias.strip())

#============================================================================
def build_dicts() :
    """Build dictionnaries usable for encoding identification.
    """
    global charsets,aliases2python,aliases2mime
    
    # Make some missing links.
    charsets['UTF-8'].mime = 'UTF-8'
    
    # We build aliases2python from encoding.aliases.aliases dictionary - maybe
    # incomplete (if an encoding has no alias, is it in this dictionnary...).
    for alias in encoding_aliases :
        pyenc = encoding_aliases[alias]
        # Python use encoding for more than character sets conversions, 
        # so avoid storing these things.
        if pyenc in ['base64_codec','bz2_codec','hex_codec',
                            'idna','quopri_codec','rot_13','string_escape',
                            'unicode_escape','uu_codec','zlib_codec'] :
            continue
        # Fill aliases2python with Python known aliases.
        aliases2python[normenc(alias)] = pyenc
        aliases2python[normenc(pyenc)] = pyenc
    
    # Continue to fill aliases2python using IANA charsets.
    for clist in pyenc_charsets.itervalues() :
        for c in clist :
            for normname in c.normnames :
                if normname not in aliases2python :
                    aliases2python[normname] = c.pyenc
    
    # Now, set aliases2mime, but only for encodings supported by Python
    # where we have a corresponding MIME information.
    for clist in pyenc_charsets.values() :
        for c in clist :
            if not c.mime : continue
            for n in [c.name]+c.aliases :
                    aliases2mime[normenc(n)] = c.mime


#============================================================================
def make_k_encoding_charsets() :
    """
    """
    global aliases2python,aliases2mime
    fname = path.join([path.dirname(path.abspath(__file__)),"k_encoding_charsets.py"])
    f = open(fname,"wU")
    f.write("#!/bin/env python\n")
    f.write("# -*- coding: ascii -*-\n")
    f.write("# file: k_encoding_charsets - automatically generated!!!\n")
    f.write("encoding2python_map = ")
    pprint.pprint(aliases2python,f,indent=4)
    #f.write(repr(aliases2python))
    f.write("\n")
    f.write("encoding2mime_map = ")
    pprint.pprint(aliases2mime,f,indent=4)
    #f.write(repr(aliases2mime))
    f.write("\n")

#============================================================================
def make() :
    """Do our job: build k_encoding_charsets module.
    """
    global charsets
    
    if not charsets :
        iana_data = upload_iana_file()
        analyze_charset_data(iana_data)
    build_dicts()
    make_k_encoding_charsets()

#============================================================================
if __name__ == "__main__" :
    import getopt

    if len(sys.argv)<2 or '-h' in sys.argv or '--help' in sys.argv  :
        print "Usage: python k_ianacharset [-g] [-p] [-m]"
        print "  -b make k_encoding_charsets.py module" 
        print "  -g store character-sets file (from http://www.iana.org/assignments/)."
        print "  -p print identified charsets"
        print
        sys.exit()

    
    print "Loading http://www.iana.org/assignments/character-sets"
    iana_data = upload_iana_file()
    analyze_charset_data(iana_data)
    
    if '-g' in sys.argv :
        print "Writing",path.abspath("character-sets")
        f = open("character-sets","wU")
        for l in iana_data : f.write(l+"\n")
        f.close()

    if '-p' in sys.argv :
        p = pprint.PrettyPrinter()
        print "Charsets from IANA:"
        p.pprint(charsets)

    if '-m' in sys.argv :
        make()
