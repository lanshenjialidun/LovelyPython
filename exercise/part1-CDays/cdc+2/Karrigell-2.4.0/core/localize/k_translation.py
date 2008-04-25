# -*- coding: latin-1 -*-

"""Translation engine, alternative to gettext

When a string must be translated, instead of writing this in a script :
    print "hello world"
the line can be written :
    print _("hello world")

This module provides a function install() that will make _() a built-in
function, available in all scripts. This function will take strings as
arguments, and return their translation into the language specified in
install()

The translation dictionary is defined for a folder. It is stored in a file
called translation_x.kt where x is the iso639 code for the language ('en' for
English, 'fr' for French, etc.), in a subfolder called 'translations'

Suppose you want to define the translations into French for the folder 'dummy'.
Here are the steps you would follow :

- create a Python dictionary mapping original text to its translation into
  French. The keys and values must be bytestrings using the same encoding
  For instance : fr_transl = { 'Answer':'Réponse' }

- call the function save_translations :
      save_translations('dummy','fr',fr_transl)

- then, to install the translation engine with this dictionary :
      install('dummy','fr')

Encodings
---------
By default, the dictionary is supposed to have latin-1 encoded keys and 
values ; for the non-unicode-aware programmer this limits the risks of having
problems with encodings

If dictionaries are provided in another encoding, it must be specified in
save_translations :
   save_translations('dummy','f',fr_transl,'utf-8')

If the translation function arguments and result are in another encoding than
latin-1 they must be specified in install :
   install('dummy','fr','utf-8')
"""

import os
import k_config
import PyDbLite

def get_trans_db():
    """Create or open the translation database"""
    path = os.path.join(k_config.serverDir,"data","translations.pdl")
    db = PyDbLite.Base(path)
    db.create("original","iso639","translation",mode="open")
    return db

def get_translations(folder,language):
    """Return the translation dictionary found in the folder for the
    specified language
    If no dictionary is found, an empty dictionary is returned
    """
    db = get_trans_db()
    res = db(iso639=language)
    if res:
        return dict([(r["original"],r["translation"]) for r in res])
    else:
        return None

def save_translations(folder,language,transl_dict,encoding='latin-1'):
    """Save the translations in a file
    folder : the folder where the translations will be used
    language : the iso639 code of the language
    transl_dict : the dictionary mapping original text to its translation
    encoding : the encoding used for the keys and values in transl_dict
    
    The dictionary is saved in a file with one line per text, the
    original text on one line and its translation on the following line
    
    If encoding is not specified, all the keys and values in the
    translation dictionary are supposed to be utf-8 encoded. If an encoding
    is supplied, these keys and values are supposed to be in this encoding
    
    In all cases, the values are stored on file as utf-8 encoded bytestrings
    """

    # check encoding
    db = get_trans_db()
    for orig,trans in transl_dict.iteritems():
        res = db(original=orig,iso639=language)
        if res:
            db.update(res,translation=trans)
        else:
            db.insert(orig,language,trans)
    db.commit()

def install(folder,languages,encoding='latin-1'):
    """Installs the translation engine : a built-in function _() will be
    available ; _(text) will return the translation of text into the
    specified language, according to the dictionary valid for the
    specified folder
    This function uses the translation dictionary, in which keys and
    values are unicode strings. The argument to the function is a string
    encoded in the specified encoding
    The steps to find the translation of a text and return it in the specified
    encoding are :
    - build the unicode string matching the text : us = unicode(text,encoding)
    - see if us is a key of the translation dictionary
       . if true : uv is the matching value (a unicode string)
       . if false : uv = us (still unicode)
    - the translation is this unicode string encoded in the specified
      encoding : v = uv.encode(encoding)
    """

    def _translate(text):
        return text
    for language in languages:
        # if no dictionary was found, no translation will be made
        dico = get_translations(folder,language)
        if dico:
            def _translate(text):
                s8 = unicode(text,encoding)
                return dico.get(s8,s8).encode(encoding)
            break
    # set __builtin__._ to this function
    import __builtin__
    __builtin__.__dict__['_'] = _translate
    