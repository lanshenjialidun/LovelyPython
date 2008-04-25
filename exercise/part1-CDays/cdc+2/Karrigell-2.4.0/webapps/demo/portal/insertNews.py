# insert a news 
if len(_newsBody)>255:
    print _("Body must not exceed 255 characters")
    raise SCRIPT_END
    
import datetime
from portalDb import db

so=Session()
db['news'].insert(so.login,_newsTitle,_newsBody,datetime.datetime.today())
db['news'].commit()

raise HTTP_REDIRECTION,"index.pih"
