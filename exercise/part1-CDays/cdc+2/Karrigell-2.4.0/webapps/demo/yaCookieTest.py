from HTMLTags import *

text1 = ""
text2 = ""

# Create Session object
#so = Session()

# Use cookie set on client
try :
    CookieValue = COOKIE["Test"].value
    text2 = "Cookie ok"
except KeyError :
    CookieValue = None
    text2 = "Cookie init"

# Create or update cookie on client
SET_COOKIE["Test"] = 1
#SET_COOKIE["Test2"] = 1

# Generate page
header = HEAD(TITLE("Cookie test"))
body = BODY(TEXT(text1)+BR()+TEXT(text2))
print HTML(header+body) 