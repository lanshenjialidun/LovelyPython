capitals={'France':'Paris','Germany':'Berlin','Spain':'Madrid','Italy':'Rome'}
#html - a table for the title
<table>
<tr bgcolor="#A0A0A0">
<td>Here are the capitals of some European countries</td>
</tr>
</table>
<table border=1>
#/html
for item in capitals.keys():
	print "<tr><td><b>%s</b></td><td>%s</td></tr>" %(item,capitals[item])

"</table>"