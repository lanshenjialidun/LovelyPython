'<head><link rel="stylesheet" href="k_base.css"></head>'

selected=int(QUERY.get("selected",0))

labels = ["Rights","Configuration"]

'<div id="navcontainer">'
'<ul id="navlist">'
for i,label in enumerate(labels):
	if i==selected:
		'<li id="active"><a href="menu.pih?selected=%s" id="current" target="_top">%s</a></li>' %(i,label)
	else:
		'<li><a href="menu.pih?selected=%s" target="_top">%s</a>' %(i,label)
'</ul>'
'</div>'
