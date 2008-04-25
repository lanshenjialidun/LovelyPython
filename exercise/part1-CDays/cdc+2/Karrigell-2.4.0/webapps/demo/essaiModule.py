my_url = None

def set_url(url):
    global my_url
    my_url = url

def info():
    return "The url is [%s]" %my_url