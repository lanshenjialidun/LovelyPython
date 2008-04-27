import re

regx = "\d\d\d\d-\d\d-\d+"

for str in open("c:\stdout.log","r"):

    if re.search(regx,str):

        pintr str
