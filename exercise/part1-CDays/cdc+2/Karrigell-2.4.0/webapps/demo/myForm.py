HEADERS['accept-charset'] = 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
print """
<html>

<body>

<form action="myScript.py?aValue=blabla" acceptcharset="utf-8" method="post">
  Spam
  <br><input name="spam">
  <br>Animal
  <br><select multiple name="animal[]">
  <option value="dog">Dog
  <option value="cat">Cat
  <option value="frog">Frog
  </select>
  <br><input type="submit" value="Ok">
</form>

</body>
</html>
"""