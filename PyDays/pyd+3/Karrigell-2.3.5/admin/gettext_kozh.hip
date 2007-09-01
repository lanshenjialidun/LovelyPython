
import sys,os,cStringIO,gettext,cgi
import k_pygettext
import k_config
import k_utils
from k_encodings import k_encoding

def alphaSort(x,y):
	return cmp(x.lower(),y.lower())

path=_fullname
strings=[]
isFile=os.path.isfile(path)
if isFile:
	file=path
	dirname=os.path.dirname(file)
	ext=os.path.splitext(file)[1]
	if ext==".py":
		pyCode=open(file).read()
	elif ext==".pih":
		import PythonInsideHTML
		pyCode=PythonInsideHTML.PIH(file).pythonCode()
	elif ext==".hip":
		import HIP
		pyCode=HIP.HIP(file).pythonCode()
	try:
		kpg=k_pygettext.Gettext(pyCode)
		strings=kpg.extracts()
	except:
		pass
else:
	dirname=path

if isFile and not strings:
	print _("No string marked for translation")
	raise SCRIPT_END
	
messages={}	# for each language, messages[language] is a dictionary mapping a string to its translation
# searches existing translations
for iso639 in ACCEPTED_LANGUAGES:
	localedir=os.path.join(dirname,"translations")
	try:
		t=gettext.translation("messages",localedir,[iso639])
		messages[iso639]=t._catalog	# encapsulation, they say...
		if not t._charset: # binary file without charset declaration
			for key in messages[iso639]:
				val = messages[iso639][key]
				# val is a utf-8 encoded string. We must convert it to outputEncoding
				encoded_val = unicode(val,'utf-8').encode(k_config.outputEncoding)
				messages[iso639][key] = encoded_val
				print key
	except:
		t=gettext.NullTranslations()
		messages[iso639]={}

if not isFile:
	for l in messages.keys():
		for st in messages[l].keys():
			if not st in strings:
				strings.append(st)
	strings.sort(alphaSort)

# a session object will keep the messages for next step
sessionObj=Session()
sessionObj.messages=messages
sessionObj.strings=strings
sessionObj.dirname=dirname

print _("Translation of strings in")

"<b>%s</b>" %_shortname
"<p>"
"<table border=1>"
"<tr>"
"<th>%s</th>" %_("String")
for l in ACCEPTED_LANGUAGES:
	print '<th>%s</th>' %l
"</tr>"
'<form action="internat.pih" method="POST">'
'<input type="hidden" name="script" value="modifTrans.hip">'
 
# language of strings to translate
print _('The strings to translate are in')
for l in ACCEPTED_LANGUAGES:
	'<input type="radio" name="defaultLanguage" value="'+l+'">'+l+'\n'
'<input type="radio" name="defaultLanguage" value="(other)">'+_("other")+'\n'

for ixs in range(len(strings)):
	item=strings[ixs]
	print '<tr>'
	print '<td>%s</td>' %item.replace("<","&lt;")
	for i in range(len(ACCEPTED_LANGUAGES)):
		iso639=ACCEPTED_LANGUAGES[i]
		if messages.has_key(iso639) and messages[iso639].has_key(item):
			txt=messages[iso639][item]
			txt=cgi.escape(txt,1)
			print '<td><input name="%s" value="%s"></td>' %(iso639+str(ixs),txt)
		else:
			print '<td><input name="%s"></td>' %(iso639+str(ixs))
	print '</tr>'
"""
</table>
<br>
<input type="submit" value="Ok">
</form>
"""
