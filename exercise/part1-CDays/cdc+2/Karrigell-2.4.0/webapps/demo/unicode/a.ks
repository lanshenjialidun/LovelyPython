#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding directive is needed only if you write non-ascii
# values directly in text
import HIP

def index():

    print u"Simple ascii string<br>"
    print u"Re\u0165azec zap\u00edsan\u00fd unicode k\u00f3dmi<br>"
    print u"Немножко азбуки<br>"

    print "<hr>"
    print "HIP test:<br>"

    H = HIP.HTMLStream()
    H + u'Euro sign writen directly in utf-8 unicode string: €<br>' 
    H + u'Yen sign writen as unicode escape code: \u00a5<br>'
    H - u'This string is cgi-quoted: <€ & \u00a5>; &lt;≡< ∧ &gt;≡>'

