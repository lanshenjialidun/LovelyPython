# insert a news 

if len(_newsBody)>255:
    print _("Body must not exceed 255 characters")
    raise SCRIPT_END

import datetime
from portalDb import db

# update values
db['news'].update(db['news'][int(_id)],
    title=_newsTitle, body=_newsBody, date=datetime.datetime.today())
db['news'].commit()
    
raise HTTP_REDIRECTION,"index.pih"
