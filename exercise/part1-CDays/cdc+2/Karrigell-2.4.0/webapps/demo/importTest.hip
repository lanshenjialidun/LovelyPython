import k_config
import importTest
'<html>'
'<body>'
'<h3>Import test</h3>'
'Debug mode is %s' %k_config.reload_modules
'<br>Value found in importTest.py : '+ importTest.value
'<form action="changeValueInImported.py">'
'New value <input name="value">'
'<input type="submit" value="Ok">'
'</form>'
'</body>'
'</html>'