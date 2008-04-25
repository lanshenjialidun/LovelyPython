import k_config
import k_translation

# searches existing translations for specified folder
messages = {}
for iso639 in ACCEPTED_LANGUAGES:
    messages[iso639] = k_translation.get_translations(_dirname,iso639) or {}

orig = {}
new_transl = {}

for attr in QUERY.keys():
    if attr in ["dirname","script","defaultLanguage"]:
        continue
    iso639 = attr[:2]
    ix = int(attr[2:])
    if k_config.encode_form_data:
        transl = QUERY[attr] # unicode
    else:
        transl = unicode(QUERY[attr],k_config.output_encoding)

    if not iso639 in new_transl:
        new_transl[iso639] = {}
    new_transl[iso639][ix] = transl

langs = [ k for k in new_transl if k != "_o" ]
for ix in new_transl["_o"]:     #original strings
    orig = new_transl["_o"][ix]
    print orig.encode(k_config.output_encoding)
    for iso639 in langs:
        transl = new_transl[iso639][ix]
        print new_transl[iso639][ix],"[%s]" %iso639

        if messages.has_key(iso639):
            messages[iso639][orig]=transl
        else:
            messages[iso639]={orig:transl}

    print "<br>"

# default language
if not QUERY.has_key('defaultLanguage'):
    raise SCRIPT_ERROR,_("You must specify the default language")

if _defaultLanguage=="(other)":
    pass
else:
    for s in new_transl["_o"].values():
        messages[_defaultLanguage][s]=s

for language in messages:
    k_translation.save_translations(_dirname,language,
        messages[language],'utf-8')
"<p><b>"
print _("New translations have been registered")
"</b>"
