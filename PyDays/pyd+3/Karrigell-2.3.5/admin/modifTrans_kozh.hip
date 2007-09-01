Include("header.htm")
sessionObj=Session()	# has messages and strings attributes
messages=sessionObj.messages	# state before modification
for attr in QUERY.keys():
	if attr in ["script","defaultLanguage"]:
		continue
	iso639=attr[:2]
	ix=int(attr[2:])
	transl=QUERY[attr]
	orig=sessionObj.strings[ix]
	print "%s [%s] <i>%s</i><br>" %(orig,iso639,transl)
	if messages.has_key(iso639):
		messages[iso639][orig]=transl
	else:
		messages[iso639]={orig:transl}

# default language
if not QUERY.has_key('defaultLanguage'):
	raise SCRIPT_ERROR,_("You must specify the default language")

if _defaultLanguage=="(other)":
	pass
else:
	for s in sessionObj.strings:
		messages[_defaultLanguage][s]=s

import k_msgfmt
for language in messages.keys():
	k_msgfmt.MESSAGES=messages[language]
	translationsDir=os.path.join(sessionObj.dirname,"translations")
	if not os.path.isdir(translationsDir):
		os.mkdir(translationsDir)
	languageDir=os.path.join(translationsDir,language)
	if not os.path.isdir(languageDir):
		os.mkdir(languageDir)
		os.mkdir(os.path.join(languageDir,"LC_MESSAGES"))
	outfile=os.path.join(languageDir,"LC_MESSAGES","messages.po")
	k_msgfmt.write_po(outfile)
	outfile=os.path.join(languageDir,"LC_MESSAGES","messages.mo")
	k_msgfmt.write(outfile)
"<p><b>"
print _("New translations have been registered")
"</b>"