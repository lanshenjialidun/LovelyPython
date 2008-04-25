### myScript.py ### 
#RESPONSE["Content-Type"] = 'text/plain'
print '<html><body>MyScript<br>' 
for key in QUERY: 
    print '"%s" -> "%s"<br>' % (key, QUERY[key].replace('\n','<br>')) 
print '</body></html>' 
### 