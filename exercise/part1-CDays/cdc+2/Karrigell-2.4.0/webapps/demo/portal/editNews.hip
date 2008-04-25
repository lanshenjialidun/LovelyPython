# edits a news

Include ("header.hip")

from portalDb import db
so=Session()
news=db['news'][int(_id)]

print "<h3>%s</h3>" %_("Edit existing news")
Include("newsForm.pih",
    action="updateNews.py",
    news=news)
