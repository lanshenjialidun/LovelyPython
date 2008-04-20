import os

def translations(folder,language):
    """returns a dictionary mapping the translations of the strings marked
    for translation in the folder into the language"""
    # the file holding the translations is "translations_language.kt"
    res = {}
    try:
        t_file = file(os.path.join(folder,"translations",
            "translation_%s.kt" %language)).readlines()
        while True:
            orig = t_file.readline()
            if not orig:
                break
            res[transl[:-1]] = t_file.readline()[:-1]
    except IOError:
        return {}
        