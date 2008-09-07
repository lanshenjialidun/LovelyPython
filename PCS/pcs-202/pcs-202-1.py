import urllib
from chardet.universaldetector import UniversalDetector

usock = urllib.urlopen('http://www.baidu.com')
detector = UniversalDetector()
for line in usock.readlines():
    detector.feed(line)
    if detector.done: break
detector.close()
usock.close()
print detector.result