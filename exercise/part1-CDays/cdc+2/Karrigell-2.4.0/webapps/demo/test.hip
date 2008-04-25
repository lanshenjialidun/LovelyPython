# HIP test

import Cookie,os,HTML

"<html>\n"

print HTML.head({"title":"HTML Inside Python test",
	'style type="text/css"':"TD {color: blue}"})

"<body>\n"

Include("hipHeader.htm")

if HEADERS.has_key("cookie"):
	ck=Cookie.BaseCookie(HEADERS["cookie"])
	print "COOKIES<br>"
	for k in ck.keys():
		print '%s : %s<br>' %(k,ck[k].value)

liste=["un",
	"deux",
		"trois"]

"<p>List : "+str(liste)

"""<p>
<font face="Verdana">
If you want to include HTML code inside a HIP document, include it between triple quotes
</font>"""

"<h2>HTTP headers</h2>"
print HTML.table(HEADERS,border="1",cellpadding="4")

"<p><b>Current directory : </b>"+os.getcwd()+"\n<p>"

capitals={'France':'Paris','Germany':'Berlin','Spain':'Madrid','Italy':'Rome'}
print HTML.table(capitals,border="1",cellpadding="4")

def square(x):
	return x*x
for i in range(10):
	"Square of ",i," : <b>",square(i),"</b>"
	"<br>"

SET_COOKIE["name"]="proust"
SET_COOKIE["firstname"]="marcel"

"</html>"