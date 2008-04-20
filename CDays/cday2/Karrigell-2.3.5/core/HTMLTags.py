"""Classes to generate HTML in Python

The HTMLTags module defines a class for all the valid HTML tags, written in
 uppercase letters. To create a piece of HTML, the general syntax is :

    t = TAG(innerHTML, key1=val1,key2=val2,...)

so that "print t" results in :

    <TAG key1="val1" key2="val2" ...>innerHTML</TAG>

For instance :

    print A('bar', href="foo") ==> <A href="foo">bar</A>

To generate HTML attributes without value, give them the value True :

    print OPTION('foo',SELECTED=True,value=5) ==> 
            <OPTION value="5" SELECTED>

For non-closing tags such as <IMG> or <BR>, the print statement does not 
generate the closing tag

The innerHTML argument can be an instance of an HTML class, so that you can nest 
tags, like this :

    print B(I('foo')) ==> <B><I>foo</I></B>

Instances of the HTML classes support the addition :

    print B('bar')+INPUT(name="bar") ==> <B>bar</B><INPUT name="bar">

and also repetition :

    print TH('&nbsp')*3 ==> <TD>&nbsp;</TD><TD>&nbsp;</TD><TD>&nbsp;</TD>

If you have a list (or any iterable) of instances, you can't concatenate the items with 
sum(instanceList) because sum takes only numbers as arguments. So there is a 
function called Sum which will do the job :

    Sum( TR(TD(i)+TD(i*i)) for i in range(100) )

generates the rows of a table showing the squares of integers from 0 to 99

The innerHTML argument can be a string, but you can't concatenate a string and 
an instance of an HTML class, like in :

    H1('To be or ' + B('not to be'))

For this, use a class called TEXT, which will not generate any tag :

    H1(TEXT('To be or ') + B('not to be'))


A simple document can be produced by :

    print HTML( HEAD(TITLE('Test document')) +
        BODY(H1('This is a test document')+
             TEXT('First line')+BR()+
             TEXT('Second line')))

This will produce :

    <HTML>
    <HEAD>
    <TITLE>Test document</TITLE>
    </HEAD>
    <BODY>
    <H1>This is a test document</H1>
    First line
    <BR>
    Second line
    </BODY>
    </HTML>

If the document is more complex it is more readable to create the elements 
first, then to print the whole result in one instruction. For example :

stylesheet = LINK(rel="Stylesheet",href="doc.css")

head= HEAD(TITLE('Record collection')+stylesheet)
title = H1('My record collection')
rows = Sum ([TR(TD(rec.title,Class="title")+TD(rec.artist,Class="Artist")) 
    for rec in records])
table = TABLE(TR(TH('Title')+TH('Artist')) + rows)

print HTML(head + BODY(title + table))
"""

import cStringIO

class TAG:
    """Generic class for tags"""
    def __init__(self, innerHTML="", **attrs):
        self.tag = [self.__class__.__name__]
        self.innerHTML = [innerHTML]
        self.attrs = [attrs]
    
    def __str__(self):
        res=cStringIO.StringIO()
        w=res.write
        for tag, innerHTML, attrs in zip(self.tag, 
            self.innerHTML, self.attrs):
            if not tag=='TEXT':
                if tag in _WS_INSENSITIVE:
                    w('\n')
                w("<%s" %tag)
                # attributes which will produce arg = "val"
                attr1 = [ k for k in attrs if not isinstance(attrs[k],bool) ]
                w("".join([' %s="%s"' %(k,attrs[k]) for k in attr1]))
                # attributes with no argument
                # if value is False, don't generate anything
                attr2 = [ k for k in attrs if attrs[k] is True ]
                w("".join([' %s' %k for k in attr2]))
                w(">")
            w(str(innerHTML))
            if tag in ClosingTags:
                w("</%s>" %tag)
        return res.getvalue()

    def __add__(self,other):
        """Concatenate another tag to self"""
        self.tag += other.tag
        self.innerHTML += other.innerHTML
        self.attrs += other.attrs
        return self

    def __mul__(self,n):
        """Replicate self n times"""
        return Sum([self]*n)

# list of tags, from the HTML 4.01 specification

ClosingTags =  ['A', 'ABBR', 'ACRONYM', 'ADDRESS', 'APPLET',
            'B', 'BDO', 'BIG', 'BLOCKQUOTE', 'BUTTON',
            'CAPTION', 'CENTER', 'CITE', 'CODE',
            'DEL', 'DFN', 'DIR', 'DIV', 'DL',
            'EM', 'FIELDSET', 'FONT', 'FORM', 'FRAMESET',
            'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
            'I', 'IFRAME', 'INS', 'KBD', 'LABEL', 'LEGEND',
            'MAP', 'MENU', 'NOFRAMES', 'NOSCRIPT', 'OBJECT',
            'OL', 'OPTGROUP', 'PRE', 'Q', 'S', 'SAMP',
            'SCRIPT', 'SELECT', 'SMALL', 'SPAN', 'STRIKE',
            'STRONG', 'STYLE', 'SUB', 'SUP', 'TABLE',
            'TEXTAREA', 'TITLE', 'TT', 'U', 'UL',
            'VAR', 'BODY', 'COLGROUP', 'DD', 'DT', 'HEAD',
            'HTML', 'LI', 'OPTION', 'P', 'TBODY',
            'TD', 'TFOOT', 'TH', 'THEAD', 'TR']

NonClosingTags = ['AREA', 'BASE', 'BASEFONT', 'BR', 'COL', 'FRAME',
            'HR', 'IMG', 'INPUT', 'ISINDEX', 'LINK',
            'META', 'PARAM']

# create the classes
for tag in ClosingTags + NonClosingTags + ['TEXT']:
    exec("class %s(TAG): pass" %tag)
    
def Sum(iterable):
    """Return the concatenation of the instances in the iterable
    Can't use the built-in sum() on non-integers"""
    it = [ item for item in iterable ]
    if it:
        return reduce(lambda x,y:x+y, it)
    else:
        return ''

# whitespace-insensitive tags, determines pretty-print rendering
_WS_INSENSITIVE = NonClosingTags + ['HTML','HEAD','BODY',
    'FRAMESET','FRAME',
    'TITLE','SCRIPT',
    'TABLE','TR','TD','TH','SELECT','OPTION',
    'FORM']