
function change_sec(o)
{
	if (o.value == 'low')
	{
	 ch = '<p>'
	} else {
	 ch = '<table>'
	 ch += '<tr><td>Login</td><td><input name="login"></td></tr>'
	 ch += '<tr><td>Password</td><td><input type="password" name="passwd"></td></tr>'
	 ch += '</table>'
	}
	document.getElementById("adm_info").innerHTML = ch
}