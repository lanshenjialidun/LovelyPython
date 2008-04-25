# stores or updates user preferences 

from portalDb import db
so=Session()
db['users'].update(db['users'][so.user],bgcolor=_bgcolor,fontfamily=_fontfamily)
db['users'].commit()

raise HTTP_REDIRECTION,"index.pih"
