# removes a news from the database
# the news is identified by its id

from portalDb import db
del db['news'][int(_id)]
db['news'].commit()

raise HTTP_REDIRECTION,"index.pih"