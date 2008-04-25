# search engine

import re
import posixpath

import BuanBuan
import wikiBase

db = wikiBase.db

caseSensitive=QUERY.has_key("caseSensitive")
fullWord=QUERY.has_key("fullWord")

words=_words
if fullWord:
    words=r"\W"+words+r"\W"

sentence="[\n\r.?!].*"+words+".*[\n\r.?!]"

if caseSensitive:
    sentencePattern=re.compile(sentence)
    wordPattern=re.compile(words)
else:
    sentencePattern=re.compile(sentence,re.IGNORECASE)
    wordPattern=re.compile(words,re.IGNORECASE)

occ=0   # number of occurences

def replace(matchObj):
    return "<b>"+matchObj.string[matchObj.start():matchObj.end()]+"</b>"

def linkToPage(name):
    # returns a link to the page called name
    return '<a href="BuanShow.pih?pageName=%s">%s</a>\n<br><blockquote>' %(name,name)

print "<h2>Searching [%s]</h2>" %(_words)

# gets all pages in base
for page in db:
    content = page['content']
    content="\n"+content+"\n"
    flag=0  # true if at least one match
    deb=0
    while 1:
        searchObj=sentencePattern.search(content,deb)
        if searchObj is None:
            if flag:
                print "\n</blockquote>\n"
            break
        else:
            if not flag:
                print linkToPage(page['name'])
                flag=1
            sentence=content[searchObj.start():searchObj.end()]
            sentence=sentence.lstrip()
            sentence=sentence[re.search("[^!]",sentence).start():]
            sentence=wordPattern.sub(replace,sentence)
            # eliminates leading char "!"
            print sentence+"<br>"
            deb=searchObj.end()-len(words)+1
            occ+=1
            flag=1

if not occ:
    print "%s not found" %_words
    
print '<a href="index.pih">Back</a>'