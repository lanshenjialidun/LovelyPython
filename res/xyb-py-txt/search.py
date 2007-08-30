#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from urllib import quote
import re

RE_LINK = r'<div class=g[^>]*>(?:<link [^>]*>)?<h2 class=r><a href="([^"]+)"[^>]*>(.+?)</a></h2>'

def search(keyword):
    request = urllib2.Request('http://www.google.com/custom?q=' + quote(keyword))
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20061201 Firefox/2.0.0.6 (Ubuntu-feisty)')
    opener = urllib2.build_opener()
    html = opener.open(request).read()

    for link, title in re.findall(RE_LINK, html):
        title = re.sub('</?b>', '', title)
        yield link, title

def search2(keyword):
    request = urllib2.Request('http://www.google.com/custom?q=' + quote(keyword))
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20061201 Firefox/2.0.0.6 (Ubuntu-feisty)')
    opener = urllib2.build_opener()
    html = opener.open(request).read()

    html = html.replace('<div class=g', '\n<div class=g')
    html = html.replace('</h2>', '</h2>\n')
    results = [s for s in html.split('\n') if s.startswith('<div class=g')]
    for s in results:
        s = s[s.find('href="'):]
        s = s.replace('href="', '')
        link = s[:s.find('"')]
        t = s[s.find('>')+1:]
        t = t[:t.find('</a>')]
        t = t.replace('<b>', '')
        t = t.replace('</b>', '')
        title = t[t.rfind('>')+1:]
        yield link, title

if __name__ == '__main__':
    import sys
    for link, title in search(sys.argv[1]):
        print link, title
