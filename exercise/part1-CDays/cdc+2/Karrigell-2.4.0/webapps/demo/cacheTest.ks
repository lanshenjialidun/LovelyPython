import time

def a():

    RESPONSE['Content-type'] = "application/vnd.mozilla.xul+xml"
    RESPONSE['Cache-Control'] = "must-revalidate"

    a =  """<?xml version="1.0"?>
<?xml-stylesheet href="chrome://global/skin/" type="text/css"?>

<window
id="findfile-window"
title="Find Files"
orient="horizontal"
xmlns="http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul">
"""
    b = '<vbox> <label value="' +  time.strftime('%c', time.localtime()) +\
'" /></vbox>'

    c = """</window>"""

    print a + b + c

def b():

    RESPONSE['Content-type'] = "application/vnd.mozilla.xul+xml"
    RESPONSE['Cache-Control'] = "must-revalidate"

    a =  """<?xml version="1.0"?>
<?xml-stylesheet href="chrome://global/skin" type="text/css"?>
<window

xmlns="http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul">
  <vbox datasources="xul_005.ks/rdf" ref="urn:root">
  </vbox>
</window>"""

    print a

def rdf():

    RESPONSE['Content-type'] = "application/rdf+xml"
    RESPONSE['Cache-Control'] = "must-revalidate"

    a = """<?xml version="1.0"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:nc="http://home.netscape.com/NC-rdf#">
<rdf:Description about="urn:root">
<nc:links>
<rdf:Seq>
"""
    b = '<rdf:li><rdf:Description nc:name="' + time.strftime('%c',
time.localtime()) + '" /></rdf:li> '

    c = """</rdf:Seq>
</nc:links>  
</rdf:Description> 
</rdf:RDF>"""

    print a+b+c

def x():
    print """<?xml version="1.0"?> 
    <?xml-stylesheet href="chrome://global/skin" type="text/css"?> 
    <window xmlns:html="http://www.w3.org/1999/xhtml" xmlns="http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul" align="vertical">  
    <vbox datasources="template-primer.rdf" ref="urn:root">  
    <template>  
    <rule>  
    <conditions>  
    <content uri="?uri" />  
    <triple subject="?uri" predicate="http://home.netscape.com/NC-rdf#links" object="?links" />  
    <member container="?links" child="?child" />  
    <triple subject="?child" predicate="http://home.netscape.com/NC-rdf#name" object="?name" />  
    </conditions>  
    <action>  
    <hbox>  
    <label uri="?child" value="?name" />  
    </hbox>  
    </action>  
    </rule>  
    </template>  
    </vbox> 
    </window>"""