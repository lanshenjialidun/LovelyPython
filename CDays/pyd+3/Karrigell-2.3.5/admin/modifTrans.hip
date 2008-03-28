import k_config
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

	# if an encoding is used, the value must be utf-8 encoded
	if k_config.encodeFormData:
		transl = transl.encode('utf-8')
	# else, the bytestring is the encoded with k_config.outputEncoding :
	# we must make it an utf-8 encoding
	else:
		transl = unicode(transl,k_config.outputEncoding).encode('utf-8')

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

import k_translation
for language in messages.keys():
	k_translation.save_translations(sessionObj.dirname,language,
		messages[language],'utf-8')
"<p><b>"
print _("New translations have been registered")
"</b>"