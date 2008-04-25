import sys, os
sys.path.append(os.path.join(os.getcwd(),'../'))

from HTMLTags import *

# a few tests

# create 3 cells for a table
cells = TD("bla",Class="even") + TD("bli", Class="odd") + TD("blo",Class="even")
# the row holding these cells
row = TR(cells + TD('&nbsp;')*2)

print B(I(FONT("ggg",face="courier")))

print OPTION('blabla',SELECTED=True,value=5)

print HTML(
    HEAD('blabla') +
    BODY(
        A("link",href="http://jjj") +
        SELECT(Sum([ OPTION(i,value=i) for i in range(10) ]), name="foo") +
        TABLE(row)+TEXT('blabla')+BR())
    )

print Sum( [ TD(i) for i in range(5) ])

print Sum ([ TR(TD(i)+TD(i*i)) for i in range(10) ])

stylesheet = LINK(rel="Stylesheet",href="doc.css")

head= HEAD(TITLE('Record collection')+stylesheet)
title = H1('My record collection')
rows = Sum ([TR(TD(t,Class="title")+TD(a,Class="Artist")) 
    for a,t in [('You are the quarry','Morrissey'),('Buzzcocks','Love bites')] ])
table = TABLE(TR(TH('Title')+TH('Artist')) + rows)

print HTML(head + BODY(title + table))

print OPTION('blabla',SELECTED=False,value=5)
