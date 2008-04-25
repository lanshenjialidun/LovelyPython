#!/usr/bin/python
# -*- coding: iso8859_1 -*-

import HIP
H = HIP.HTMLStream()
H + u"Cette phrase est écrite en ISO8859-1 codage mais contient un caractère qui ne peut être représenté en ce codage:  c\u0153ur"


