try:
	selected=int(_selected)
except:
	selected=0

'<div id="navcontainer">'
'<ul id="navlist">'
for i in range(len(labels)):
	label=labels[i]
	if i==selected:
		'<li id="active"><a href="%s?selected=%s" id="current">%s</a></li>' %(targetUrl,i,label)
	else:
		'<li><a href="%s?selected=%s">%s</a>' %(targetUrl,i,label)
'</ul>'
'</div>'

Include(urls[selected])
