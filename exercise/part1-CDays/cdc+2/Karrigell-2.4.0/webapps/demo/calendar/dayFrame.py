# searches events recorded for the day
import datetime
from HTMLTags import *
import agendaDb

db=agendaDb.db
evtsByHour={}
startTime=datetime.datetime(Session().year,Session().month,Session().day)
endTime=startTime + datetime.timedelta(days=1)

evtsOfTheDay= [ r for r in db if startTime <= r['begin_time'] < endTime ]
for evt in evtsOfTheDay:
    if evtsByHour.has_key(evt['begin_time'].hour):
        evtsByHour[evt['begin_time'].hour].append(evt)
    else:
        evtsByHour[evt['begin_time'].hour]=[evt]
print '<table>'
for h in range(24):
    if h % 2:
        print '<tr class="odd">'
    else:
        print '<tr class="even">'
    print TD('%s:00' %h)
    print '<td>'
    if evtsByHour.has_key(h): 
        for ev in evtsByHour[h]:
            print """<table cellspacing="0" cellpadding="0" width="100%">
            <tr>
            <td align="left" style="font-family:sans-serif; font-size: 8pt">
            <%= ev['content'] %>
            </td>
            <td align="right">
            <a href="removeEntry.py?entryId=<%= ev['__id__'] %>">
            <img src="delete.gif" border="0" alt="Remove entry"></a>
            </tr>
            </table>"""
    else:
        print '&nbsp;'
    print '</td></tr>'
print '</table>'