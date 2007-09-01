#! /usr/bin/env python
# -*- coding: UTF-8 -*-

# Customized version of pygettext
# 
# The Gettext class constructor takes a *Python code string* (not a file name) as argument
# Method extracts() returns a list of the strings to translate
#
# Originally written by Barry Warsaw <barry@zope.com>
#
# Minimally patched to make it even more xgettext compatible 
# by Peter Funk <pf@artcom-gmbh.de>


import os
import sys
import time
import getopt
import tokenize
import operator
import cStringIO

# for selftesting
try:
    import fintl
    _ = fintl.gettext
except ImportError:
    def _(s): return s

__version__ = '1.4'

default_keywords = ['_']
DEFAULTKEYWORDS = ', '.join(default_keywords)

EMPTYSTRING = ''

# The normal pot-file header. msgmerge and Emacs's po-mode work better if it's
# there.
pot_header = ''

escapes = []

def make_escapes(pass_iso8859):
    global escapes
    if pass_iso8859:
        # Allow iso-8859 characters to pass through so that e.g. 'msgid
        # "Höhe"' would result not result in 'msgid "H\366he"'.  Otherwise we
        # escape any character outside the 32..126 range.
        mod = 128
    else:
        mod = 256
    for i in range(256):
        if 32 <= (i % mod) <= 126:
            escapes.append(chr(i))
        else:
            escapes.append("\\%03o" % i)
    escapes[ord('\\')] = '\\\\'
    escapes[ord('\t')] = '\\t'
    escapes[ord('\r')] = '\\r'
    escapes[ord('\n')] = '\\n'
    escapes[ord('\"')] = '\\"'


def escape(s):
    global escapes
    s = list(s)
    for i in range(len(s)):
        s[i] = escapes[ord(s[i])]
    return EMPTYSTRING.join(s)


def safe_eval(s):
    # unwrap quotes, safely
    return eval(s, {'__builtins__':{}}, {})


def normalize(s):
    # This converts the various Python string types into a format that is
    # appropriate for .po files, namely much closer to C style.
    lines = s.split('\n')
    if len(lines) == 1:
        s = '"' + escape(s) + '"'
    else:
        if not lines[-1]:
            del lines[-1]
            lines[-1] = lines[-1] + '\n'
        for i in range(len(lines)):
            lines[i] = escape(lines[i])
        lineterm = '\\n"\n"'
        s = '""\n"' + lineterm.join(lines) + '"'
    return s

class TokenEater:
    def __init__(self, options):
        self.__options = options
        self.__messages = {}
        self.__state = self.__waiting
        self.__data = []
        self.__lineno = -1
        self.__freshmodule = 1
        self.__curfile = None

    def __call__(self, ttype, tstring, stup, etup, line):
        # dispatch
##        import token
##        print >> sys.stderr, 'ttype:', token.tok_name[ttype], \
##              'tstring:', tstring
        self.__state(ttype, tstring, stup[0])

    def __waiting(self, ttype, tstring, lineno):
        opts = self.__options
        # Do docstring extractions, if enabled
        if opts.docstrings and not opts.nodocstrings.get(self.__curfile):
            # module docstring?
            if self.__freshmodule:
                if ttype == tokenize.STRING:
                    self.__addentry(safe_eval(tstring), lineno, isdocstring=1)
                    self.__freshmodule = 0
                elif ttype not in (tokenize.COMMENT, tokenize.NL):
                    self.__freshmodule = 0
                return
            # class docstring?
            if ttype == tokenize.NAME and tstring in ('class', 'def'):
                self.__state = self.__suiteseen
                return
        if ttype == tokenize.NAME and tstring in opts.keywords:
            self.__state = self.__keywordseen

    def __suiteseen(self, ttype, tstring, lineno):
        # ignore anything until we see the colon
        if ttype == tokenize.OP and tstring == ':':
            self.__state = self.__suitedocstring

    def __suitedocstring(self, ttype, tstring, lineno):
        # ignore any intervening noise
        if ttype == tokenize.STRING:
            self.__addentry(safe_eval(tstring), lineno, isdocstring=1)
            self.__state = self.__waiting
        elif ttype not in (tokenize.NEWLINE, tokenize.INDENT,
                           tokenize.COMMENT):
            # there was no class docstring
            self.__state = self.__waiting

    def __keywordseen(self, ttype, tstring, lineno):
        if ttype == tokenize.OP and tstring == '(':
            self.__data = []
            self.__lineno = lineno
            self.__state = self.__openseen
        else:
            self.__state = self.__waiting

    def __openseen(self, ttype, tstring, lineno):
        if ttype == tokenize.OP and tstring == ')':
            # We've seen the last of the translatable strings.  Record the
            # line number of the first line of the strings and update the list 
            # of messages seen.  Reset state for the next batch.  If there
            # were no strings inside _(), then just ignore this entry.
            if self.__data:
                self.__addentry(EMPTYSTRING.join(self.__data))
            self.__state = self.__waiting
        elif ttype == tokenize.STRING:
            self.__data.append(safe_eval(tstring))
        # TBD: should we warn if we seen anything else?

    def __addentry(self, msg, lineno=None, isdocstring=0):
        if lineno is None:
            lineno = self.__lineno
        if not msg in self.__options.toexclude:
            entry = (self.__curfile, lineno)
            self.__messages.setdefault(msg, {})[entry] = isdocstring

    def set_filename(self, filename):
        self.__curfile = filename
        self.__freshmodule = 1

    def write(self, fp):
        strings = []			# list of strings to translate
        options = self.__options
        timestamp = time.ctime(time.time())
        # The time stamp in the header doesn't have the same format as that
        # generated by xgettext...
        print >> fp, pot_header % {'time': timestamp, 'version': __version__}
        # Sort the entries.  First sort each particular entry's keys, then
        # sort all the entries by their first item.
        reverse = {}
        for k, v in self.__messages.items():
            keys = v.keys()
            keys.sort()
            reverse.setdefault(tuple(keys), []).append((k, v))
        rkeys = reverse.keys()
        rkeys.sort()
        for rkey in rkeys:
            rentries = reverse[rkey]
            rentries.sort()
            for k, v in rentries:
                isdocstring = 0
                # If the entry was gleaned out of a docstring, then add a
                # comment stating so.  This is to aid translators who may wish
                # to skip translating some unimportant docstrings.
                if reduce(operator.__add__, v.values()):
                    isdocstring = 1
                # k is the message string, v is a dictionary-set of (filename,
                # lineno) tuples.  We want to sort the entries in v first by
                # file name and then by line number.
                v = v.keys()
                v.sort()
                if not options.writelocations:
                    pass
                # location comments are different b/w Solaris and GNU:
                elif options.locationstyle == options.SOLARIS:
                    for filename, lineno in v:
                        d = {'filename': filename, 'lineno': lineno}
                        print >>fp, _(
                            '# File: %(filename)s, line: %(lineno)d') % d
                elif options.locationstyle == options.GNU:
                    # fit as many locations on one line, as long as the
                    # resulting line length doesn't exceeds 'options.width'
                    locline = '#:'
                    for filename, lineno in v:
                        d = {'filename': filename, 'lineno': lineno}
                        s = _(' %(filename)s:%(lineno)d') % d
                        if len(locline) + len(s) <= options.width:
                            locline = locline + s
                        else:
                            print >> fp, locline
                            locline = "#:" + s
                    if len(locline) > 2:
                        print >> fp, locline
                if isdocstring:
                    print >> fp, '#, docstring'
                #print >> fp, 'msgid', normalize(k)
                #print >> fp, 'msgstr ""\n'
                strings.append(k)
        return strings

# for holding option values
class Options:
	# constants
	GNU = 1
	SOLARIS = 2
	# defaults
	extractall = 0 # FIXME: currently this option has no effect at all.
	escape = 0
	keywords = []
	outpath = ''
	outfile = 'messages.pot'
	writelocations = 0
	locationstyle = GNU
	verbose = 0
	width = 78
	excludefilename = ''
	docstrings = 0
	nodocstrings = {}
	toexclude = []

class Gettext:

	def __init__(self,pythonCode):
		global default_keywords
		self.pythonCode=cStringIO.StringIO(pythonCode)
		self.options = Options()
		self.locations = {'gnu' : self.options.GNU,
					 'solaris' : self.options.SOLARIS,
					 }

		# output file = standard output
		self.options.outfile = "-"

	def extracts(self):
		# calculate escapes
		make_escapes(self.options.escape)

		# calculate all keywords
		self.options.keywords.extend(default_keywords)

		# slurp through all the files
		eater = TokenEater(self.options)
		fp = self.pythonCode
		closep = 1
		try:
			# eater.set_filename(self.filename)
			try:
				tokenize.tokenize(fp.readline, eater)
			except tokenize.TokenError, e:
				print >> sys.stderr, '%s: %s, line %d, column %d' % (
					e[0], filename, e[1][0], e[1][1])
		finally:
			if closep:
				fp.close()

		# write the output
		fp = sys.stdout
		closep = 0
		res=[]
		try:
			res=eater.write(fp)
		finally:
			if closep:
				fp.close()
		return res

if __name__ == '__main__':
	kpg=Gettext(open("bidon.py").read())
	print kpg.extracts()