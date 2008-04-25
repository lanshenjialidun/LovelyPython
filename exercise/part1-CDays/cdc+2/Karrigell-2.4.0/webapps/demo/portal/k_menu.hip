# Vertical menu
# Parameters :
# - labels : a list with menu items labels
# - urls : the list of matching urls to display when a menu item is selected
# - targetUrl : the url to call to reload the page
# - _selected : the selected item, if specified

try:
	selected=int(_selected)
except:
	selected=0

'<table cellpadding="3" cellspacing="0" width="100%">\n'
'<tr>'
'<td valign="top"><table cellpadding="3" cellspacing="0">'
for i in range(len(labels)):
	label=labels[i]
	if i==selected:
		'\t<tr><td bgcolor="#D0D0D0">'
		'\n\t\t<a class="tab" href="%s?selected=%s">%s</a>' %(targetUrl,i,label)
		'\n\t</td></tr>'
	else:
		'\t<tr><td bgcolor="#808080">'
		'\n\t\t<a class="tab" href="%s?selected=%s">%s</a>' %(targetUrl,i,label)
		'\n\t</td></tr>'
"\n</table></td>"
'<td valign="top">'
Include('poems/'+urls[selected])
"</td></tr></table>"