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

def get_translations(folder,language):
    """Return the translation dictionary found in the folder for the
    specified language
    If no dictionary is found, an empty dictionary is returned
    """
    res = {}
    try:
        t_file = file(os.path.join(folder,"translations",
            "translation_%s.kt" %language),'rb')
        while True:
            orig = t_file.readline()[:-1]
            if not orig:
                break
            res[orig] = t_file.readline()[:-1]
        return res
    except IOError:
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
    _dictionary = {} # dictionary with keys and values utf-8 encoded
    for k,v in transl_dict.iteritems():
        # these functions will raise an exception if k or v are not
        # strings encoded in the specified encoding
        uk = unicode(k,encoding)
        uv = unicode(v,encoding)
        _dictionary[uk.encode('utf-8')] = uv.encode('utf-8')

    # save into file
    transl_folder = os.path.join(folder,"translations")
    if not os.path.exists(transl_folder):
        os.mkdir(transl_folder)
    t_file = file(os.path.join(transl_folder,
        "translation_%s.kt" %language),"wb")
    for k,v in _dictionary.iteritems():
        t_file.write(str(k)+'\n')
        t_file.write(str(v)+'\n')
    t_file.close()

def install(folder,languages,encoding='latin-1'):
    """Installs the translation engine : a built-in function _() will be
    available ; _(text) will return the translation of text into the
    specified language, according to the dictionary valid for the
    specified folder
    This function uses the translation dictionary, in which keys and
    values are utf-8 encoded. The argument to the function is a string
    encoded in the specified encoding
    The steps to find the translation of a text and return it in the specified
    encoding are :
    - build the utf-8 encoding of the text
       . the unicode string matching text is us = unicode(text,encoding)
       . the utf-8 encoding of this unicode string is s8 = us.encode('utf-8')
    - see if s8 is a key of the translation dictionary
       . if true : v8 is the matching value (an utf-8 encoded string)
       . if false : v8 = s8 (still utf-8 encoded)
    - v8 is the utf-8 encoding of the unicode string uv = unicode(v8,'utf-8')
    - the translation is this unicode string encoded in the specified
      encoding : v = uv.encode(encoding)
    """
    def _translate(text):
        return text
    for language in languages:
        res = get_translations(folder,language)
        # if no dictionary was found, no translation will be made
        if res is not None:
            def _translate(text):
                s8 = unicode(text,encoding).encode('utf-8')
                v8 = res.get(s8,s8)
                return unicode(v8,'utf-8').encode(encoding)
            break
    # set __builtin__._ to this function
    import __builtin__
    __builtin__.__dict__['_'] = _translate
    