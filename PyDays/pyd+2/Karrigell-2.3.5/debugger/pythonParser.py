# -*- coding: iso-8859-1 -*-
"""
    Partly copied for Karrigell from :

    MoinMoin - Python Source Parser

    Copyright (c) 2001 by Jürgen Hermann <jh@web.de>
    All rights reserved, see COPYING for details.

    $Id: pythonParser.py,v 1.3 2003/12/07 21:35:06 quentel Exp $
"""

# Imports
import cgi, string, sys, cStringIO
import keyword, token, tokenize


#############################################################################
### Python Source Parser (does Hilighting)
#############################################################################

_KEYWORD = token.NT_OFFSET + 1
_TEXT    = token.NT_OFFSET + 2

_colors = {
    token.NUMBER:       '#0080C0',
    token.OP:           '#0000C0',
    token.STRING:       '#004080',
    tokenize.COMMENT:   '#008000',
    token.NAME:         '#000000',
    token.ERRORTOKEN:   '#FF8080',
    _KEYWORD:           '#C00000',
    _TEXT:              '#000000',
}


class Parser:
    """ Send colored python source.
    """

    def __init__(self, raw, request, **kw):
        """ Store the source text.
        """
        self.raw = string.rstrip(string.expandtabs(raw))
        self.request = request
        #self.form = request.form
        #self._ = request.getText

        self.out = kw.get('out', sys.stdout)

    def format(self, showLineNums=0):
        """ Parse and send the colored source.
        """
        # store line offsets in self.lines
        self.lines = [0, 0]
        pos = 0
        while 1:
            pos = string.find(self.raw, '\n', pos) + 1
            if not pos: break
            self.lines.append(pos)
        self.lines.append(len(self.raw))

        # write line numbers
        if showLineNums:
            self.lineNums=cStringIO.StringIO()
            self.lineNums.write('<pre>')
            for idx in range(1, len(self.lines)-1):
                self.lineNums.write('%3d \n' % idx)
            self.lineNums.write('</pre>')

        #self.out.write('<pre>')

        # parse the source and write it
        self.pos = 0
        text = cStringIO.StringIO(self.raw)
        try:
            tokenize.tokenize(text.readline, self)
        except tokenize.TokenError, ex:
            pass
            msg = ex[0]
            line = ex[1][0]
            self.out.write('[ERROR: %s]<font color="red">%s</font>\n' % (
                msg, self.raw[self.lines[line]:]))
        #self.out.write('</pre>')


    def __call__(self, toktype, toktext, (srow,scol), (erow,ecol), line):
        """ Token handler.
        """
        if 0: print "type", toktype, token.tok_name[toktype], "text", toktext, \
                    "start", srow,scol, "end", erow,ecol, "<br>"

        # calculate new positions
        oldpos = self.pos
        newpos = self.lines[srow] + scol
        self.pos = newpos + len(toktext)

        # handle newlines
        if toktype in [token.NEWLINE, tokenize.NL]:
            self.out.write('\n')
            return

        # send the original whitespace, if needed
        if newpos > oldpos:
            self.out.write(self.raw[oldpos:newpos])

        # skip indenting tokens
        if toktype in [token.INDENT, token.DEDENT]:
            self.pos = newpos
            return

        # map token type to a color group
        if token.LPAR <= toktype and toktype <= token.OP:
            toktype = token.OP
        elif toktype == token.NAME and keyword.iskeyword(toktext):
            toktype = _KEYWORD
        color = _colors.get(toktype, _colors[_TEXT])

        style = ''
        if toktype == token.ERRORTOKEN:
            style = ' style="border: solid 1.5pt #FF0000;"'

        # send text
        self.out.write('<font color="%s"%s>' % (color, style))
        self.out.write(toktext)
        self.out.write('</font>')


if __name__ == "__main__":
    import os
    print "Formatting..."

    # open own source
    source = open('python.py').read()

    # write colorized version to "python.html"
    Parser(source, None, out = open('python.html', 'wt')).format(None)

    # load HTML page into browser
    if os.name == "nt":
        os.system("explorer python.html")
    else:
        os.system("netscape python.html &")

