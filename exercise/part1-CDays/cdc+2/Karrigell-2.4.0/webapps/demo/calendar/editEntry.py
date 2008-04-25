import datetime
from agendaDb import db

y,m,d = Session().year,Session().month,Session().day

if _subm == "Add":
    if _content:
        begin_time = datetime.datetime(y,m,d,int(_begin_hour),int(_begin_minute))
        end_time = datetime.datetime(y,m,d,int(_end_hour),int(_end_minute))
        db.insert(_content,begin_time,end_time)
        db.commit()
elif _subm == "Delete":
    del db[int(_rec_id)]
    db.commit()
elif _subm == "Update":
    if _content:
        record = db[int(_rec_id)]
        bt = datetime.datetime(y,m,d,int(_begin_hour),int(_begin_minute))
        et = datetime.datetime(y,m,d,int(_end_hour),int(_end_minute))
        db.update(record,content=_content,begin_time=bt,end_time=et)
        db.commit()

raise HTTP_REDIRECTION,"index.pih"
