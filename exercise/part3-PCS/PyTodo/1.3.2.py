import urllib

def farideaHttp():

    page = urllib.urlopen("../Boards.asp";)

    body = page.readlines()

    page.close()



    return body

def anyHtml(line):

    import re

    regx = r"""<img\s*src\s*="?(\S+)"?"""

    match_obj = re.search(regx,line)

    if match_obj!=None:

        all_groups = match_obj.groups()

        for img in all_groups:print img#这个img就是图片的链接了

lines = farideaHttp()#读取全部内容  

for line in lines:

    anyHtml(line)
