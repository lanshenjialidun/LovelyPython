import urllib

import re



class MyUserAgent(urllib.FancyURLopener):

    def __init__(self, *args):

        self.version = "QingFengbot/0.1(Python;QingFengbot 0.1;zh-CN)"#定义自己的user_agent  

        urllib.FancyURLopener.__init__(self, *args)



def httpclient(url):

    urllib._urlopener = MyUserAgent()



    page = urllib.urlopen(url)

    body = page.read()#read? readlines?  

    page.close()



    return body

import qingfengbot

print qingfengbot.httpclient("http://www.faridea.com/bbs/Boards.asp")

