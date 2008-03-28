# functions that generate HTML code in current cases

import cStringIO
import urllib

def head(args):
    """Generates the <head> code with the arguments as dictionary"""
    if len(args.keys())==0: return ''
    res=cStringIO.StringIO()
    res.write('<head>\n')
    for item in args.keys():
        res.write('<'+item+'>\n')
        res.write(args[item]+'\n')
        res.write('</'+item.split()[0]+'>\n')
    res.write('</head>\n')
    return res.getvalue()

def table(dico,**attrs):
    """Generates the <table> code from a dictionary. The lines are dico's item
    attrs is a dictionary with the table attributes, for instance 
    {border:2,cellpadding:3}
    """
    res=cStringIO.StringIO()
    res.write("<table")
    for item in attrs.keys():
        res.write(' %s="%s"' %(item,attrs[item]))
    res.write(">\n")
    for item in dico.keys():
        res.write("<tr>\n")
        res.write("<td>"+str(item)+"</td>\n")
        if str(dico[item]):
            res.write("<td>"+str(dico[item])+"</td>\n")
        else:
            res.write("<td>&nbsp;</td>\n")      
    res.write("</table>\n")
    return res.getvalue()

def tabs(options,script,selectedItem=0,selectedColor="lightgrey",unselectedColor="white"):
    """Generates tabs from a list of items
    The item at index selectedItem is put forward
    script is the script to call if user clicks on the tab, it will
    receive a query string with a "selectedTab" key"""
    res=cStringIO.StringIO()
    res.write("<table><tr>\n")
    for i in range(len(options)):
        if str(i)==str(selectedItem):
            res.write('<td bgColor="%s"><a href="%s?selectedTab=%s">%s</a></td>' \
                %(selectedColor,script,i,options[i]))
        else:
            res.write('<td bgColor="%s"><a href="%s?selectedTab=%s">%s</a></td>' \
                %(unselectedColor,script,i,options[i]))
    res.write("</tr></table>")
    return res.getvalue()

def select(name,options,selected=None,**args):
    """Generates a SELECT widget from a list of (value,name) options
    args are used as key="value" attributes of the SELECT tag
    The option for which value==selected is selected
    """
    res=cStringIO.StringIO()
    res.write('<select name="%s" ' %name)
    for i in args.keys():
        res.write('%s="%s" ' %(i,args[i]))
    res.write('>\n')
    for value,name in options:
        res.write('\t<option value="%s"' %value)
        if value==selected:
            res.write(' selected')
        res.write('>%s\n' %name)
    res.write("</select>\n")
    return res.getvalue()

def link(url,**data):
    return url+"?"+urllib.urlencode(data)

def a(href,text,**args):
    res=cStringIO.StringIO()
    res.write('<a href="%s"' %href)
    for k,v in args.items():
        res.write(' %s="%s"' %(k,v))
    res.write('>%s</a>' %text)
    return res.getvalue()