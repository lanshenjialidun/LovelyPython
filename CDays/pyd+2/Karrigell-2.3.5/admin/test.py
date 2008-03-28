iso639 = "fr"
messages = {}
import gettext
outputEncoding = 'latin-1'
t=gettext.translation("messages",r"..\webapps\demo\forum_buzhug\translations",[iso639])
messages[iso639]=t._catalog # encapsulation, they say...
if not t._charset: # binary file without charset declaration
    for key in messages[iso639]:
        val = messages[iso639][key]
        # val is a utf-8 encoded string. We must convert it to outputEncoding
        encoded_val = unicode(val,'utf-8').encode(outputEncoding)
        messages[iso639][key] = encoded_val
        print key,encoded_val
