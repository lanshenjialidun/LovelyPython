_song = 226

from songDb import db

song=db['chansons'][int(_song)]

# recueils et dialectes dans lesquels on trouve la chanson
recueils = db['chansons_par_recueil'].select(['recueil'],'chanson == v',v=song)
dialectes = db['chansons_par_dialecte'].select(['dialecte'],'chanson == v',v=song)

print 'recueils',recueils
print 'dialectes',dialectes

print song.breton
print song.francais

print "Recueil"
print ", ".join([r.recueil.nom for r in recueils])

print "Dialecte"
print ", ".join([d.dialecte.nom for d in dialectes])

print "Genre", song.genre.nom
print "Prix", round(float(song.prix)/100,2)
