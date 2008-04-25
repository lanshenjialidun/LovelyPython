from PyDbLite import Base
db = {}
try:
    db['chansons'] = Base('chansons.pdl').open()
except IOError:
    import createSongBase
    createSongBase.createBase()
    db['chansons'] = Base('chansons.pdl').open()

db['recueils'] = Base('recueils.pdl').open()
db['dialectes'] = Base('dialectes.pdl').open()
db['genres'] = Base('genres.pdl').open()
db['chansons_par_recueil'] = Base('chansons_par_recueil.pdl').open()
db['chansons_par_dialecte'] = Base('chansons_par_dialecte.pdl').open()
    