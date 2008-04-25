from agendaDb import db

del db[int(_entryId)]
db.commit()

raise HTTP_REDIRECTION,"index.pih"
