# Displays the news ordered by deposit date

from portalDb import db

all_news= [ news for news in db["news"] ]
all_news.sort(lambda x,y : cmp(x["date"],y["date"]))

'<table cellpadding="0" cellspacing="3" width="100%" bgcolor="#D0D0D0">'
'<tr><td bgcolor="#808080">%s</td></tr>' %_("News")
for news in all_news:
    timestring=news["date"].strftime("%d/%m/%y %H:%M")
    '<tr><td bgcolor="#D0D0D0">'
    '<b>%s</b>' %news["title"]
    '<br>%s' %news["body"]
    '<br><font size="-2">%s - %s</font>' %(news["login"],timestring)
    '</td></tr>'

print '</table>'
