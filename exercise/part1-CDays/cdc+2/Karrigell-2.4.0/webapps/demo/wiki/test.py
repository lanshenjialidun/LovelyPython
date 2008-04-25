from wikiBase import db

print len(db)

names=db.select_for_update(None,name='PourVoir')
for name in names:
    print name

    
