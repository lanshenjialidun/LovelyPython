"""BuanBuan, simple implementation of Wiki"""

import cStringIO,string,os,re,sys,time,cPickle,cgi
import sets

bolds=re.compile("'''(.+?)'''")
italics=re.compile("''(.+?)''")
superscripts=re.compile(r"\^(.+?)\^")  # caret for superscripted
hr = re.compile("^[\-]+.*",re.MULTILINE)
header = re.compile("^(!+)(.*)",re.MULTILINE)
wikiLink=re.compile(r"\b[A-Z][a-z]+[A-Z][a-z]+.*?\b")
noWikiLink=re.compile(r"\b_[A-Z][a-z]+[A-Z]+[a-z]+.*?\b")
anchor = re.compile('\[(.+)\|(.+)\]')
href_patt = re.compile('<\s*?[Aa]\s+?')
style = re.compile('^\{\s*(\w*)')
line = re.compile('(^.*)',re.MULTILINE)
olist = re.compile('^(\d)+\.(.*)')
ulist = re.compile('^([\*]+)(.*)')
protocols=["http:","ftp:","mailto:"]

def isLinkName(word):
    """Returns true if word is a valid Wiki link"""
    return wikiLink.match(word)

class BuanDoc:

    def __init__(self, name, text):
        self.wikiNames = sets.Set() # new pages (words as valid Wiki names)
        self.pageName = name
        self.text = cgi.escape(text)
        self.make_html()
    
    def make_html(self):
        # wiki names
        self.text = wikiLink.sub(self.handle_wikiLink,self.text)
        # anchors
        self.text = anchor.sub(self.handle_anchor,self.text)
        # non wiki names : remove first character _
        self.text = noWikiLink.sub(self.handle_nowiki,self.text)
        # bold, italic, superscript
        self.text=bolds.sub(self.handle_bold,self.text)
        self.text=italics.sub(self.handle_italic,self.text)
        self.text=superscripts.sub(self.handle_superscript,self.text)
        # horizontal rule, header
        self.text = hr.sub(self.handle_hr,self.text)
        self.text = header.sub(self.handle_header,self.text)
        # css style
        self.in_style = False
        #self.text = style.sub(self.handle_style,self.text)
        # ordered and unordered lists
        self.ol_depth = 0
        self.ul_depth = 0
        self.text = line.sub(self.handle_line,self.text)
    
    def handle_wikiLink(self,mo):
        link = mo.group()
        self.wikiNames.add(link)
        return '<a href="BuanShow.pih?pageName=%s">%s</a>' % (link,link)

    def handle_nowiki(self,mo):
        link = mo.group()
        return link[1:]

    def handle_anchor(self,mo):
        txt,href = mo.groups()
        if href.startswith('<a href="BuanShow.pih?pageName'):
            href = href[:href[:-4].rfind('>')+1]
            return href + txt + '</a>'
        else:
            return '<a href="%s">%s</a>' %(href,txt)

    def handle_style(self,mo):
        style = mo.groups()[0]
        text = mo.groups()[1].lstrip()
        return '<pre class = "%s">%s</pre>' %(style,text)

    def handle_hr(self,mo):
        return '<hr>\n'

    def handle_header(self,mo):
        level = len(mo.groups()[0])
        return '<h%s>%s</h%s>' %(level,mo.groups()[1].rstrip(),level)

    def handle_line(self,mo):
        text = mo.groups()[0]
        res = ''
        # ordered list ?
        mo = olist.match(text)
        if mo:
            depth = int(mo.groups()[0])
            text = mo.groups()[1]
            if depth > self.ol_depth:
                self.ol_depth = depth
                res = '<ol>\n'
            else:
                while depth < self.ol_depth:
                    res += '</ol>\n'
                    self.ol_depth -= 1
            res += '<li>'
        else:
            while self.ol_depth:
                res += '</ol>\n'
                self.ol_depth -= 1
        # unordered list ?
        mo = ulist.match(text)
        if mo:
            depth = len(mo.groups()[0])
            text = mo.groups()[1]
            if depth > self.ul_depth:
                self.ul_depth = depth
                res = '<ul>\n'
            else:
                while depth < self.ul_depth:
                    res += '</ul>\n'
                    self.ul_depth -= 1
            res += '<li>'
        else:
            while self.ul_depth:
                res += '</ul>\n'
                self.ul_depth -= 1
        # style ?
        mo = style.match(text)
        if mo:
            stylename = mo.groups()[0]
            res = '<pre class = "%s">' %stylename
            text = text[mo.end():].lstrip()
            self.in_style = True
        # end of style ?
        if text.startswith('}'):
            res = '</pre>'
            text = text[1:]
            self.in_style = False
        br = ''
        if not res and not self.in_style:
            br = '<p>'
        return br + res + text

    def handle_bold(self,mo):
        return "<b>%s</b>" %mo.groups()[0]

    def handle_italic(self,mo):
        return "<i>%s</i>" %mo.groups()[0]

    def handle_superscript(self,mo):
        return "<sup>%s</sup>" %mo.groups()[0]

def test():
    txt = """[prvious|blabla.pih?jjj]
!!!New features
1. refactoring of the Template module : execution of scripts is passed to modules mod_(extension)
1.a new option if .ini file specifies the supported extensions
1. added ^Cheetah^ support
1. replaced gadfly by [_KirbyBase|http://www.netpromi.com/kirbybase.html], removed dbStorage
2. exception '''SCRIPT_ERROR''' : raise SCRIPT_ERROR,msg prints the message msg and stops the script execution
{ python print
}
WiKi _NoWiKi
!!!To do
* document ''virtual'' hosts
** first
** second
* other point
--
!!! salut
1. ca va etre dur
2. de trouver
2. quelque chose
1. de special
{ html <br>
<ll>
}
* a dire
[essai de lien|AvecLienWiki]
"""
    b = BuanDoc('test',txt)
    print b.text

if __name__=="__main__":
    test()
    print isLinkName('LineWiki')
    print isLinkName('_LienWiki')