print "<table>"
for label,url in items:
    if url == selected :
        style = 'selected_item'
    else:
        style = 'menu_item'
    print "  <tr><td>"
    print "    <a href='%(url)s' class='%(style)s'>%(label)s</a>" % vars()
    print "  </tr></td>"
print "</table>"
    
