so = Session()
if not hasattr(so, 'x'):
    so.x = 0

def index():
    print "x = %s" %so.x
    print '<br><a href="increment">Increment</a>'
    print '<br><a href="decrement">Decrement</a>'
    print '<br><a href="reset">Reset</a>'
    
def increment():
    so.x = _private(so.x)
    raise HTTP_REDIRECTION,"index"

def decrement():
    so.x -= 1
    raise HTTP_REDIRECTION,"index"

def reset():
    so.x = 0
    raise HTTP_REDIRECTION,"index"

def bold(txt):
    print '<b>%s</b>' %txt

def _private(x):
    """The function name begins with _ : internal function, 
    can't be call by a url"""
    return x+1