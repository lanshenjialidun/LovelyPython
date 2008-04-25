# check if value is valid
try:
    exec('value = "%s"' %_value)
except:
    print "Invalid value %s" %_value
    print '<br><a href="importTest.hip">Back</a>'
    raise SCRIPT_END
f=file("importTest.py","w")
f.write('value = "%s"' %_value)
f.close()

raise HTTP_REDIRECTION,"importTest.hip"