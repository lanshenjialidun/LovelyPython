import datetime
from agendaDb import db

if _subm=="Ok" and _content:
    bh,bm = _begin_time[:-2],_begin_time[-2:]
    eh,em = _end_time[:-2],_end_time[2:]
    msg=db.insert(content=_content,
        begin_time = datetime.datetime(Session().year,Session().month,
            Session().day,int(bh),int(bm)),
        end_time = datetime.datetime(Session().year,Session().month,
            Session().day,int(eh),int(em)))
    db.commit()

raise HTTP_REDIRECTION,"index.pih"
