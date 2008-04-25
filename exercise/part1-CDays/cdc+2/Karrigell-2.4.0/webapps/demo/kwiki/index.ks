import datetime
import re,posixpath
from kwikiBase import db
from HTMLTags import *

def index():
    print '<html>'
    print HEAD(TITLE('Kwiki - a wiki with wysiwyg text editor') +
                LINK(rel='stylesheet',href="../../../karrigell.css"))
    print '<body>'
    print TABLE(TR(
            TD(A(IMG(src="../../../doc/images/karrigell_skeudenn.png",border="0",width="50%"),
                href= "../../../")) +
            TD(H2('Welcome to Kwiki'))))
    print """Kwiki is a wiki server made with Karrigell and the 
        <a href="http://www.fckeditor.net" target="_blank">FCKEditor</a> wysiwyg 
        text editor
        <p>Browse the existing pages :"""

    names=[ (r['__id__'],r['name']) for r in db ]
    names.sort(lambda x,y: cmp(x[1].lower(),y[1].lower()))
    for (_id,name) in names:
        print '<br><a href="showPage?pageId=%s">%s</a>' %(_id,name)

    print P(H3("Add new page"))
    print FORM(TEXT('Page name ') +
               INPUT(size="20",name="pageName") +
               SMALL(TEXT(' Admin ')) +
               INPUT(type="checkbox",name="admin",value="admin") +
               INPUT(type="submit",value='Ok'),
               action = "editPage")
    print P(H3('Search'))
    print FORM(INPUT(size="20",name="words") +
               TEXT('Case sensitive ') +
               INPUT(Type="checkbox",name="caseSensitive") +
               TEXT('Full word ') +
               INPUT(Type="checkbox",name="fullWord") +
               BR() +
               INPUT(Type="submit",value="Search words"),
            action = "search")
    print P(FONT(A('Administrator',href="admin"),size="-1"))
    print "</body>\n</html>"

def editPage(pageName=None,pageId=-1,admin=False):
    print """<html><head><title>Editing %s</title>""" %pageName
    print """<style type="text/css">
        body, td  { font-family: arial; font-size: x-small; }
        a         { color: #0000BB; text-decoration: none; }
        a:hover   { color: #FF0000; text-decoration: underline; }
        .headline { font-family: arial black, arial; font-size: 28px; letter-spacing: -1px; }
        .headline2{ font-family: verdana, arial; font-size: 12px; }
        .subhead  { font-family: arial, arial; font-size: 18px; font-weight: bold; font-style: italic; }
        .backtotop     { font-family: arial, arial; font-size: xx-small;  }
        .code     { background-color: #EEEEEE; font-family: Courier New; font-size: x-small;
                  margin: 5px 0px 5px 0px; padding: 5px;
                  border: black 1px dotted;
                }

        font { font-family: arial black, arial; font-size: 28px; letter-spacing: -1px; }

        </style>
        <script type="text/javascript">
              window.onload = function()
              {
                var oFCKeditor = new FCKeditor( 'pageContent' ) ;
                oFCKeditor.Height=400;
                oFCKeditor.ReplaceTextarea() ;
              }
            </script>
        </head>
        <body>

        <script type="text/javascript" src="/fckeditor/fckeditor.js"></script>"""

    if int(pageId)>-1:
        rec = db[int(pageId)]
        pageContent = rec['content']
        pageName = rec['name']
        admin = rec['admin']
    else:
        pageContent=""

    if admin:
        Include('../AuthenticationTest.py')

    print A(IMG(src="../home.gif",border="0",alt="Home"),href="index")
    print "Editing %s""" %pageName
    print FORM(
            INPUT(Type="hidden",name="pageId",value=pageId) +
            INPUT(Type="hidden",name="pageName",value=pageName) +
            SMALL(TEXT(' Admin ')) +
            INPUT(type="checkbox",name="admin",checked=(admin != 0)) +
            INPUT(Type="submit",value="Save changes") +
            P() +
            TEXTAREA(pageContent,
                id="pageContent",name="pageContent",style="height:800px;"),
          method='POST',action="savePage")

    print "</body>\n</html>"

def savePage(pageName,pageContent,pageId,admin=0):

    if admin:
        admin = 1
        Include('../AuthenticationTest.py')

    if len(pageContent)>5000:
        print "Text too long"
        raise SCRIPT_END
    name=pageName
    pageContent=pageContent.rstrip()
    content=pageContent

    if int(pageId)>-1:
        rec = db[int(pageId)]
        db.update(rec,name=pageName, 
            admin=admin,
            content=pageContent,
            version=rec['version']+1,
            lastmodif=datetime.datetime.today()
            )
    else:
        pageId = db.insert(name=pageName,content=pageContent,
            admin=admin,nbvisits=0,
            created=datetime.datetime.today(),
            version=1,
            lastmodif=datetime.datetime.today()
            )
    db.commit()
    # show
    raise HTTP_REDIRECTION,"showPage?pageId=%s" %pageId

def showPage(pageId):
    try:
        rec = db[int(pageId)]
    except:
        print "Can't find the page"
        raise SCRIPT_END

    nbvisits = rec['nbvisits'] + 1
    db.update(rec,nbvisits=rec['nbvisits']+1)
    db.commit()

    print "<html>"
    print HEAD(TITLE(rec['name']) +
               LINK(rel="stylesheet",href="../k_wiki.css"))
    print '<body>'
    print A(IMG(src="../home.gif",border="0",alt="Home"), href="index")
    print A(IMG(src="../edit.gif",border="0",alt="Edit"),
            href="editPage?pageId=%s" %rec['__id__'])
    print BR()
    print rec['content']
    print HR()
    print SMALL(I(TEXT('Version : %s -- ' %rec['version']) +
                  TEXT('Last modified : %s '
                        %rec['lastmodif'].strftime("%d/%m/%y %H:%M")) +
                  TEXT(' Visited %s times' %nbvisits)
                  ))
    print '</body>\n</html>'

def search(words,fullWord="",caseSensitive=""):
    """Searching for the words in all pages"""
    
    if not words:
        print "No search words specified"
        raise SCRIPT_END
    s_words=words
    if fullWord:
        s_words=r"\W"+words+r"\W"

    sentence="[\n\r.?!].*"+s_words+".*[\n\r.?!]"

    if caseSensitive:
        sentencePattern=re.compile(sentence)
        wordPattern=re.compile(s_words)
    else:
        sentencePattern=re.compile(sentence,re.IGNORECASE)
        wordPattern=re.compile(s_words,re.IGNORECASE)

    occ=0   # number of occurences

    def replace(matchObj):
        return "<b>"+matchObj.string[matchObj.start():matchObj.end()]+"</b>"

    def linkToPage(recno,name):
        # returns a link to the page called name
        return '<a href="showPage?pageId=%s">%s</a>\n<br><blockquote>' %(recno,name)

    print "<h2>Searching [%s]</h2>" %words

    # browse all pages in base
    for page in db:
        content="\n"+page['content']+"\n"
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
                    print linkToPage(page['__id__'],page['name'])
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
        print "%s not found" %words

    print '<a href="index">Back</a>'

def admin():

    Include('../AuthenticationTest.py')

    # list of page names
    pages=[ (r['__id__'],r['name']) for r in db ]

    if not pages:
        print "No page to remove"
        print '<p><a href="index.pih">Back</a>'
        raise SCRIPT_END
    print """
        <form action="removePage">
        <table border="1">
        <tr><th>&nbsp;</th><th>Page</th></tr>"""
    for (_id,name) in pages:
        print '<tr><td><input type="checkbox" name="removed[]" value="%s">' %_id
        print '&nbsp;</td><td>%s</td></tr>' %name
    print """</table>
    <input type="submit" value="Remove selected pages">
    </form>"""

def removePage(removed=[]):
    # check authentication
    Include("../AuthenticationTest.py")
    
    if not QUERY.keys():
        print 'No page to remove<p><a href="index">Back</a>'
        return
            
    print "Deleting pages<p>\n"
    
    for removedPage in removed:
        del db[int(removedPage)]
    db.commit()
    
    print '<a href="index">Home</a>'
