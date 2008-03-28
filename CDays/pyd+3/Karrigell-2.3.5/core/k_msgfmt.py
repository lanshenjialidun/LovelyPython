#! /usr/bin/env python

# msgfmt Written by Martin v. Loewis <loewis@informatik.hu-berlin.de>
# interface modified for use by Karrigell


import sys
import os
import getopt
import struct
import array
from cStringIO import StringIO

__version__ = "1.1"

MESSAGES = {}

def usage(code, msg=''):
    print >> sys.stderr, __doc__
    if msg:
        print >> sys.stderr, msg
    sys.exit(code)

def add(id, str, fuzzy):
    "Add a non-fuzzy translation to the dictionary."
    global MESSAGES
    if not fuzzy and str:
        MESSAGES[id] = str

def generate():
    "Return the generated output."
    global MESSAGES
    keys = MESSAGES.keys()
    # the keys are sorted in the .mo file
    keys.sort()
    offsets = []
    ids = strs = ''
    for id in keys:
        # For each string, we need size and file offset.  Each string is NUL
        # terminated; the NUL does not count into the size.
        s = MESSAGES[id]
        if isinstance(s, unicode):
            s = s.encode('utf-8')
        offsets.append((len(ids), len(id), len(strs), len(s)))
        ids += str(id) + '\0' # this will intentionally fail if id is not ascii,
                              # because we want to catch these cases
        strs += s + '\0'
    output = ''
    # The header is 7 32-bit unsigned integers.  We don't use hash tables, so
    # the keys start right after the index tables.
    # translated string.
    keystart = 7*4+16*len(keys)
    # and the values start after the keys
    valuestart = keystart + len(ids)
    koffsets = []
    voffsets = []
    # The string table first has the list of keys, then the list of values.
    # Each entry has first the size of the string, then the file offset.
    for o1, l1, o2, l2 in offsets:
        koffsets += [l1, o1+keystart]
        voffsets += [l2, o2+valuestart]
    offsets = koffsets + voffsets
    output = struct.pack("Iiiiiii",
                         0x950412de,        # Magic
                         0,                 # Version
                         len(keys),         # # of entries
                         7*4,               # start of key index
                         7*4+len(keys)*8,   # start of value index
                         0, 0)              # size and offset of hash table
    output += array.array("i", offsets).tostring()
    output += ids
    output += strs
    return output

def generate_po():
    "Return .po content"
    keys = MESSAGES.keys()
    # let's sort the keys for nicer output
    keys.sort()
    
    out = StringIO()

    # header
    out.write(r"""# This file was automatically saved by Karrigell's k_msgfmt.py script
# You can however safely edit the file in a text editor.
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2006-01-20 21:01+0100\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"


""")
    
    
    
    for key in keys:
        if key: # do not write first empty key
            out.write('\nmsgid "%s"\n' % key)
            if isinstance(MESSAGES[key],unicode):
                out.write('msgstr "%s"\n' % MESSAGES[key].encode('utf-8'))
            else:
                out.write('msgstr "%s"\n' % MESSAGES[key])
        
    return out.getvalue()

def make(filename):
    ID = 1
    STR = 2

    # Compute .mo name from .po name and arguments
    if filename.endswith('.po'):
        infile = filename
    else:
        infile = filename + '.po'

    try:
        lines = open(infile).readlines()
    except IOError, msg:
        print >> sys.stderr, msg
        sys.exit(1)
    
    section = None
    fuzzy = 0

    # Parse the catalog
    lno = 0
    for l in lines:
        lno += 1
        # If we get a comment line after a msgstr, this is a new entry
        if l[0] == '#' and section == STR:
            add(msgid, msgstr, fuzzy)
            section = None
            fuzzy = 0
        # Record a fuzzy mark
        if l[:2] == '#,' and l.find('fuzzy'):
            fuzzy = 1
        # Skip comments
        if l[0] == '#':
            continue
        # Now we are in a msgid section, output previous section
        if l.startswith('msgid'):
            if section == STR:
                add(msgid, msgstr, fuzzy)
            section = ID
            l = l[5:]
            msgid = msgstr = ''
        # Now we are in a msgstr section
        elif l.startswith('msgstr'):
            section = STR
            l = l[6:]
        # Skip empty lines
        l = l.strip()
        if not l:
            continue
        # XXX: Does this always follow Python escape semantics?
        l = eval(l)
        if section == ID:
            msgid += l
        elif section == STR:
            msgstr += l
        else:
            print >> sys.stderr, 'Syntax error on %s:%d' % (infile, lno), \
                  'before:'
            print >> sys.stderr, l
            sys.exit(1)
    # Add last entry
    if section == STR:
        add(msgid, msgstr, fuzzy)

    return MESSAGES

def write(outfile):
    # Compute output
    output = generate()

#    if isinstance(output, unicode):
#        output = output.encode('utf-8')
        
    try:
        outstream=open(outfile,"wb")
        outstream.write(output)
        outstream.close()
    except IOError,msg:
        print >> sys.stderr, msg

def write_po(outfile):
    # Compute output
    output = generate_po()

    try:
        outstream=open(outfile,"wb")
        outstream.write(output)
        outstream.close()
    except IOError,msg:
        print >> sys.stderr, msg
      
                      
if __name__=="__main__":
    print make("../webapps/demo/translations/fr/LC_MESSAGES/messages.po")
